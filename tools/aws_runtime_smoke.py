"""Run a real AWS control-plane multipart upload smoke through Lambda."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from collections.abc import Callable
from os import environ
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import boto3


TERMINAL_FAILURE_STATUSES = {"expired", "failed"}
DEFAULT_TIMEOUT_SECONDS = 1800
DEFAULT_POLL_INTERVAL_SECONDS = 10
SAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tests"
    / "samples"
    / "dlptest-name-dob-email.pdf"
)


def terragrunt_outputs(live_stack: Path) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["terragrunt", "output", "-json"],
        cwd=live_stack,
        text=True,
    )
    return json.loads(raw)


def output_value(outputs: dict[str, Any], name: str) -> str:
    value = outputs.get(name, {}).get("value")
    if not value:
        raise RuntimeError(f"missing Terragrunt output: {name}")
    return str(value)


def invoke_api(
    lambda_client: Any,
    function_name: str,
    *,
    owner_id: str,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    event = {
        "version": "2.0",
        "routeKey": f"{method} {path}",
        "rawPath": path,
        "rawQueryString": "",
        "headers": {"content-type": "application/json"},
        "requestContext": {
            "http": {
                "method": method,
                "path": path,
                "sourceIp": "127.0.0.1",
                "userAgent": "aws-runtime-smoke",
            },
            "authorizer": {"jwt": {"claims": {"sub": owner_id}}},
        },
        "isBase64Encoded": False,
    }
    if body is not None:
        event["body"] = json.dumps(body)
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(event).encode(),
    )
    payload = json.loads(response["Payload"].read())
    status_code = int(payload["statusCode"])
    response_body = json.loads(payload.get("body") or "{}")
    return status_code, response_body


def wait_for_job(
    fetch_job: Callable[[], dict[str, Any]],
    desired_status: str,
    *,
    timeout_seconds: int,
    poll_interval_seconds: int,
    monotonic: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Poll a job until the desired or a terminal state is reached."""

    deadline = monotonic() + timeout_seconds
    last_status = ""
    while True:
        job = fetch_job()
        status = str(job.get("status", "unknown"))
        if status != last_status:
            print(f"AWS runtime smoke job status: {status}", file=sys.stderr)
            last_status = status
        if status == desired_status:
            return job
        if status in TERMINAL_FAILURE_STATUSES:
            failure_code = job.get("failure_code") or "none"
            raise RuntimeError(
                f"job reached {status} while waiting for {desired_status}: "
                f"failure_code={failure_code}"
            )
        if monotonic() >= deadline:
            raise RuntimeError(
                f"timed out waiting for {desired_status}: last_status={status}"
            )
        time.sleep(poll_interval_seconds)


def open_presigned(
    operation: str,
    request: Request,
    *,
    opener: Callable[..., Any] = urlopen,
) -> Any:
    """Open a presigned request while keeping signed URLs out of errors."""

    try:
        return opener(request, timeout=30)
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        body = re.sub(r"https?://\S+", "[redacted-url]", body)
        body = " ".join(body.split())[:1000] or error.reason
        raise RuntimeError(
            f"presigned {operation} failed: HTTP {error.code}: {body}"
        ) from None


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: aws_runtime_smoke.py <live-stack> <aws-region>",
            file=sys.stderr,
        )
        return 2

    live_stack = Path(argv[1])
    aws_region = argv[2]
    owner_id = "runtime-smoke"
    sample = SAMPLE_PATH.read_bytes()
    timeout_seconds = int(
        environ.get("AWS_E2E_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)
    )
    poll_interval_seconds = int(
        environ.get(
            "AWS_E2E_POLL_INTERVAL_SECONDS",
            DEFAULT_POLL_INTERVAL_SECONDS,
        )
    )

    outputs = terragrunt_outputs(live_stack)
    function_name = output_value(outputs, "lambda_function_name")
    lambda_client = boto3.client("lambda", region_name=aws_region)

    status, created = invoke_api(
        lambda_client,
        function_name,
        owner_id=owner_id,
        method="POST",
        path="/jobs",
        body={"source_type": "pdf", "size_bytes": len(sample)},
    )
    if status != 201:
        raise RuntimeError(f"job creation failed: {status} {created}")

    upload = created["upload_parts"][0]
    request = Request(upload["upload_url"], data=sample, method="PUT")
    with open_presigned("upload", request) as response:
        etag = response.headers["ETag"]

    job_id = created["job"]["id"]
    status, completed = invoke_api(
        lambda_client,
        function_name,
        owner_id=owner_id,
        method="POST",
        path=f"/jobs/{job_id}/upload-complete",
        body={
            "upload_id": created["upload_id"],
            "parts": [{"part_number": upload["part_number"], "etag": etag}],
        },
    )
    if status != 200 or completed["status"] != "queued":
        raise RuntimeError(f"upload completion failed: {status} {completed}")

    def fetch_job() -> dict[str, Any]:
        status_code, job = invoke_api(
            lambda_client,
            function_name,
            owner_id=owner_id,
            method="GET",
            path=f"/jobs/{job_id}",
        )
        if status_code != 200:
            raise RuntimeError(f"job polling failed: {status_code} {job}")
        return job

    wait_for_job(
        fetch_job,
        "ready",
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )

    status, exporting = invoke_api(
        lambda_client,
        function_name,
        owner_id=owner_id,
        method="POST",
        path=f"/jobs/{job_id}/export",
        body={"acknowledged": True},
    )
    if status != 200 or exporting["status"] != "exporting":
        raise RuntimeError(f"export submission failed: {status} {exporting}")

    wait_for_job(
        fetch_job,
        "complete",
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )

    status, download = invoke_api(
        lambda_client,
        function_name,
        owner_id=owner_id,
        method="GET",
        path=f"/jobs/{job_id}/download",
    )
    if status != 200:
        raise RuntimeError(f"download authorization failed: {status} {download}")
    with open_presigned(
        "download",
        Request(download["download_url"], method="GET"),
    ) as response:
        result = response.read()
    if not result:
        raise RuntimeError("authorized result download was empty")

    print(
        json.dumps(
            {
                "job_id": job_id,
                "result_bytes": len(result),
                "status": "complete",
                "lambda_function": function_name,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
