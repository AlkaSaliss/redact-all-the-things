"""AWS Batch entrypoint for real worker jobs."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from datetime import UTC, datetime
from os import environ
from typing import Any

import boto3
from botocore.config import Config

from redact_api.aws import DynamoJobRepository, S3ObjectRepository
from redact_api.domain import Job, WorkerMode, WorkerSubmission
from redact_api.worker import (
    Gliner2PiiDetector,
    PaddleOcrEngine,
    analyze_source,
    render_redacted_output,
)


def build_repositories() -> tuple[DynamoJobRepository, S3ObjectRepository]:
    """Construct worker persistence repositories from environment settings."""

    region = environ.get("AWS_REGION", "eu-west-1")
    endpoint_url = environ.get("AWS_ENDPOINT_URL")
    client_options = {
        "region_name": region,
        "endpoint_url": endpoint_url,
    }
    dynamodb = boto3.resource("dynamodb", **client_options)
    s3 = boto3.client(
        "s3",
        config=Config(s3={"addressing_style": "path"}),
        **client_options,
    )
    return (
        DynamoJobRepository(dynamodb.Table(environ["JOBS_TABLE"])),
        S3ObjectRepository(s3, bucket=environ["FILES_BUCKET"]),
    )


def run_submission(
    submission: WorkerSubmission,
    *,
    jobs: DynamoJobRepository,
    objects: S3ObjectRepository,
    now: Callable[[], datetime],
) -> Job:
    """Run one validated worker submission against persistent job state."""

    job = jobs.get(submission.job_id)
    if job is None:
        raise RuntimeError(f"job not found: {submission.job_id}")
    if (
        job.owner_id != submission.owner_id
        or job.source_key != submission.source_key
        or job.output_key != submission.output_key
    ):
        raise RuntimeError("worker submission does not match persisted job")

    if submission.mode is WorkerMode.ANALYZE:
        source = objects.get_source_object(submission.source_key)
        return analyze_source(
            job,
            source,
            jobs=jobs,
            now=now(),
            raster_writer=objects,
            ocr_store=objects,
            ocr_engine=PaddleOcrEngine(),
            pii_detector=Gliner2PiiDetector(),
            manifest_writer=objects,
        )
    return render_redacted_output(job, jobs=jobs, store=objects, now=now())


def parse_args(argv: list[str] | None = None) -> WorkerSubmission:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=[mode.value for mode in WorkerMode])
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--owner-id", required=True)
    parser.add_argument("--source-key", required=True)
    parser.add_argument("--output-key", required=True)
    parser.add_argument("--idempotency-token", required=True)
    args = parser.parse_args(argv)
    return WorkerSubmission(
        job_id=args.job_id,
        owner_id=args.owner_id,
        source_key=args.source_key,
        output_key=args.output_key,
        mode=WorkerMode(args.mode),
        idempotency_token=args.idempotency_token,
    )


def main(argv: list[str] | None = None) -> int:
    submission = parse_args(argv)
    jobs, objects = build_repositories()
    result = run_submission(
        submission,
        jobs=jobs,
        objects=objects,
        now=lambda: datetime.now(UTC),
    )
    print(
        json.dumps(
            {
                "job_id": result.id,
                "mode": submission.mode.value,
                "status": result.status.value,
                "version": result.version,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
