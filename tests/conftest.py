from collections.abc import Iterator

import boto3
import pytest
from botocore.config import Config

from redact_api.aws import (
    DynamoJobRepository,
    RecordingBatchSubmitter,
    S3ObjectRepository,
)


LOCALSTACK_URL = "http://localhost:4566"
REGION = "eu-west-1"
TABLE_NAME = "redact-jobs"
BUCKET_NAME = "redact-files"


@pytest.fixture
def aws_clients() -> dict[str, object]:
    common = {
        "endpoint_url": LOCALSTACK_URL,
        "region_name": REGION,
        "aws_access_key_id": "test",
        "aws_secret_access_key": "test",
    }
    return {
        "dynamodb": boto3.resource("dynamodb", **common),
        "s3": boto3.client(
            "s3",
            config=Config(s3={"addressing_style": "path"}),
            **common,
        ),
    }


@pytest.fixture
def aws_resources(aws_clients: dict[str, object]) -> Iterator[dict[str, object]]:
    dynamodb = aws_clients["dynamodb"]
    s3 = aws_clients["s3"]

    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if TABLE_NAME in existing_tables:
        dynamodb.Table(TABLE_NAME).delete()
        dynamodb.meta.client.get_waiter("table_not_exists").wait(
            TableName=TABLE_NAME
        )
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "owner_id", "AttributeType": "S"},
            {"AttributeName": "created_sort", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "owner-created-index",
                "KeySchema": [
                    {"AttributeName": "owner_id", "KeyType": "HASH"},
                    {"AttributeName": "created_sort", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()

    existing_buckets = {
        bucket["Name"] for bucket in s3.list_buckets().get("Buckets", [])
    }
    if BUCKET_NAME not in existing_buckets:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": REGION},
        )
    else:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME).get("Contents", [])
        if objects:
            s3.delete_objects(
                Bucket=BUCKET_NAME,
                Delete={"Objects": [{"Key": item["Key"]} for item in objects]},
            )

    yield {
        "table": table,
        "s3": s3,
        "jobs": DynamoJobRepository(table),
        "objects": S3ObjectRepository(s3, bucket=BUCKET_NAME),
        "batch": RecordingBatchSubmitter(),
    }
