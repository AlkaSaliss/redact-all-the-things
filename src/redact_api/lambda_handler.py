"""AWS Lambda entry point."""

from datetime import UTC, datetime
from os import environ

import boto3
from botocore.config import Config
from mangum import Mangum

from redact_api.aws import (
    AwsBatchSubmitter,
    DynamoJobRepository,
    S3ObjectRepository,
)
from redact_api.http import create_app
from redact_api.services import ControlPlaneService


def build_service() -> ControlPlaneService:
    """Construct the production service from Lambda environment settings."""

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
    batch = boto3.client("batch", **client_options)
    return ControlPlaneService(
        DynamoJobRepository(dynamodb.Table(environ["JOBS_TABLE"])),
        S3ObjectRepository(s3, bucket=environ["FILES_BUCKET"]),
        AwsBatchSubmitter(
            batch,
            job_queue=environ["BATCH_JOB_QUEUE"],
            analyze_job_definition=environ["BATCH_ANALYZE_DEFINITION"],
            render_job_definition=environ["BATCH_RENDER_DEFINITION"],
        ),
        clock=lambda: datetime.now(UTC),
    )


def cors_allowed_origins() -> tuple[str, ...]:
    """Return configured browser origins allowed to call the API."""

    raw = environ.get("FRONTEND_ALLOWED_ORIGINS", "")
    return tuple(origin.strip() for origin in raw.split(",") if origin.strip())


app = create_app(build_service(), cors_allowed_origins=cors_allowed_origins())
handler = Mangum(app, lifespan="off")
