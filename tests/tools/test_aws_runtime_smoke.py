"""Tests for the deployed AWS runtime smoke helpers."""

from __future__ import annotations

from io import BytesIO
from urllib.error import HTTPError
from urllib.request import Request

import pytest

from redact_api import aws
from tools import aws_runtime_smoke


def test_runtime_s3_config_forces_signature_v4() -> None:
    s3_client_config = getattr(aws, "s3_client_config", None)
    assert s3_client_config is not None

    config = s3_client_config()

    assert config.signature_version == "s3v4"
    assert config.s3 == {"addressing_style": "path"}


def test_wait_for_job_returns_requested_status() -> None:
    wait_for_job = getattr(aws_runtime_smoke, "wait_for_job", None)
    assert wait_for_job is not None

    jobs = iter([{"status": "queued"}, {"status": "ready", "id": "job-1"}])
    result = wait_for_job(
        lambda: next(jobs),
        "ready",
        timeout_seconds=10,
        poll_interval_seconds=0,
    )

    assert result == {"status": "ready", "id": "job-1"}


def test_wait_for_job_reports_safe_failure_code() -> None:
    wait_for_job = getattr(aws_runtime_smoke, "wait_for_job", None)
    assert wait_for_job is not None

    with pytest.raises(RuntimeError, match="failed.*validation_failed"):
        wait_for_job(
            lambda: {
                "status": "failed",
                "failure_code": "validation_failed",
            },
            "ready",
            timeout_seconds=10,
            poll_interval_seconds=0,
        )


def test_wait_for_job_enforces_deadline() -> None:
    wait_for_job = getattr(aws_runtime_smoke, "wait_for_job", None)
    assert wait_for_job is not None

    times = iter([0.0, 1.0])
    with pytest.raises(RuntimeError, match="timed out waiting for ready"):
        wait_for_job(
            lambda: {"status": "analyzing"},
            "ready",
            timeout_seconds=1,
            poll_interval_seconds=0,
            monotonic=lambda: next(times),
        )


def test_open_presigned_reports_body_without_signed_url() -> None:
    open_presigned = getattr(aws_runtime_smoke, "open_presigned", None)
    assert open_presigned is not None

    signed_url = "https://example.test/source?X-Amz-Signature=secret"
    error = HTTPError(
        signed_url,
        403,
        "Forbidden",
        {},
        BytesIO(b"<Error><Code>SignatureDoesNotMatch</Code></Error>"),
    )

    def raise_error(_request: Request, *, timeout: int) -> None:
        assert timeout == 30
        raise error

    with pytest.raises(RuntimeError) as captured:
        open_presigned("upload", Request(signed_url), opener=raise_error)

    message = str(captured.value)
    assert "HTTP 403" in message
    assert "SignatureDoesNotMatch" in message
    assert signed_url not in message
    assert "X-Amz-Signature" not in message
