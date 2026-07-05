"""Run a real AWS control-plane multipart upload smoke through Lambda."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import boto3


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
    sample = b"%PDF-1.4\n% runtime smoke placeholder\n"

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
    with urlopen(request, timeout=30) as response:
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

    print(
        json.dumps(
            {
                "job_id": job_id,
                "status": completed["status"],
                "lambda_function": function_name,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
