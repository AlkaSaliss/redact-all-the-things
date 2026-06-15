"""Concrete DynamoDB/S3 integration and the local Batch recording fake."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from redact_api.domain import Job, PageManifest, WorkerSubmission


class PersistenceConflictError(RuntimeError):
    """Raised when an optimistic write loses a version race."""


@dataclass(frozen=True)
class StoredManifest:
    manifest: PageManifest
    etag: str


class DynamoJobRepository:
    def __init__(self, table: Any) -> None:
        self._table = table

    def create(self, job: Job) -> None:
        self._table.put_item(
            Item=self._serialize(job),
            ConditionExpression="attribute_not_exists(id)",
        )

    def get(self, job_id: str) -> Job | None:
        response = self._table.get_item(
            Key={"id": job_id},
            ConsistentRead=True,
        )
        item = response.get("Item")
        return self._deserialize(item) if item is not None else None

    def list_owner(self, owner_id: str) -> list[Job]:
        response = self._table.query(
            IndexName="owner-created-index",
            KeyConditionExpression=Key("owner_id").eq(owner_id),
            ScanIndexForward=False,
        )
        return [self._deserialize(item) for item in response.get("Items", [])]

    def save(self, job: Job, *, expected_version: int) -> None:
        try:
            self._table.put_item(
                Item=self._serialize(job),
                ConditionExpression="#version = :expected",
                ExpressionAttributeNames={"#version": "version"},
                ExpressionAttributeValues={":expected": expected_version},
            )
        except ClientError as error:
            if error.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise PersistenceConflictError("job version conflict") from error
            raise

    @staticmethod
    def _serialize(job: Job) -> dict[str, Any]:
        payload = job.model_dump(mode="json")
        payload["created_sort"] = job.created_at.isoformat()
        payload["ttl"] = int(job.expires_at.timestamp())
        return payload

    @staticmethod
    def _deserialize(item: dict[str, Any]) -> Job:
        payload = dict(item)
        payload.pop("created_sort", None)
        payload.pop("ttl", None)
        return Job.model_validate(payload)


class S3ObjectRepository:
    def __init__(
        self,
        client: Any,
        *,
        bucket: str,
        presign_expiry_seconds: int = 900,
    ) -> None:
        self._client = client
        self._bucket = bucket
        self._presign_expiry_seconds = presign_expiry_seconds

    def create_multipart_upload(self, key: str) -> str:
        response = self._client.create_multipart_upload(
            Bucket=self._bucket,
            Key=key,
        )
        return str(response["UploadId"])

    def presign_upload_part(
        self,
        key: str,
        *,
        upload_id: str,
        part_number: int,
    ) -> str:
        return str(
            self._client.generate_presigned_url(
                "upload_part",
                Params={
                    "Bucket": self._bucket,
                    "Key": key,
                    "UploadId": upload_id,
                    "PartNumber": part_number,
                },
                ExpiresIn=self._presign_expiry_seconds,
            )
        )

    def object_exists(self, key: str) -> bool:
        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as error:
            if error.response["Error"]["Code"] in {"404", "NoSuchKey", "NotFound"}:
                return False
            raise

    def complete_multipart_upload(
        self,
        key: str,
        *,
        upload_id: str,
        parts: tuple[dict[str, Any], ...],
    ) -> None:
        self._client.complete_multipart_upload(
            Bucket=self._bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": list(parts)},
        )

    def presign_download(self, key: str) -> str:
        return str(
            self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=self._presign_expiry_seconds,
            )
        )

    def get_manifest(
        self,
        owner_id: str,
        job_id: str,
        page_number: int,
    ) -> StoredManifest | None:
        key = self.manifest_key(owner_id, job_id, page_number)
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=key)
        except ClientError as error:
            if error.response["Error"]["Code"] in {"NoSuchKey", "404"}:
                return None
            raise
        body = response["Body"].read()
        return StoredManifest(
            manifest=PageManifest.model_validate_json(body),
            etag=str(response["ETag"]).strip('"'),
        )

    def create_manifest(
        self,
        owner_id: str,
        manifest: PageManifest,
    ) -> StoredManifest:
        key = self.manifest_key(owner_id, manifest.job_id, manifest.page_number)
        try:
            response = self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=manifest.model_dump_json().encode(),
                ContentType="application/json",
                IfNoneMatch="*",
            )
        except ClientError as error:
            if error.response["Error"]["Code"] in {
                "PreconditionFailed",
                "ConditionalRequestConflict",
            }:
                raise PersistenceConflictError("manifest already exists") from error
            raise
        return StoredManifest(
            manifest=manifest,
            etag=str(response["ETag"]).strip('"'),
        )

    def save_manifest(
        self,
        owner_id: str,
        manifest: PageManifest,
        *,
        expected_etag: str,
    ) -> StoredManifest:
        key = self.manifest_key(owner_id, manifest.job_id, manifest.page_number)
        try:
            response = self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=manifest.model_dump_json().encode(),
                ContentType="application/json",
                IfMatch=expected_etag,
            )
        except ClientError as error:
            if error.response["Error"]["Code"] in {
                "PreconditionFailed",
                "ConditionalRequestConflict",
            }:
                raise PersistenceConflictError("manifest version conflict") from error
            raise
        return StoredManifest(
            manifest=manifest,
            etag=str(response["ETag"]).strip('"'),
        )

    @staticmethod
    def manifest_key(owner_id: str, job_id: str, page_number: int) -> str:
        return (
            f"users/{owner_id}/jobs/{job_id}/manifests/pages/"
            f"{page_number}.json"
        )


class AwsBatchSubmitter:
    def __init__(
        self,
        client: Any,
        *,
        job_queue: str,
        job_definition: str,
    ) -> None:
        self._client = client
        self._job_queue = job_queue
        self._job_definition = job_definition

    def submit(self, submission: WorkerSubmission) -> WorkerSubmission:
        self._client.submit_job(
            jobName=(
                f"{submission.job_id}-{submission.mode.value}-"
                f"{submission.idempotency_token.rsplit(':', 1)[-1]}"
            ),
            jobQueue=self._job_queue,
            jobDefinition=self._job_definition,
            parameters={
                "job_id": submission.job_id,
                "owner_id": submission.owner_id,
                "source_key": submission.source_key,
                "output_key": submission.output_key,
                "mode": submission.mode.value,
                "idempotency_token": submission.idempotency_token,
            },
        )
        return submission


@dataclass
class RecordingBatchSubmitter:
    submissions: dict[str, WorkerSubmission] = field(default_factory=dict)

    def submit(self, submission: WorkerSubmission) -> WorkerSubmission:
        return self.submissions.setdefault(
            submission.idempotency_token,
            submission,
        )
