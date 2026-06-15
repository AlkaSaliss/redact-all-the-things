from datetime import UTC, datetime, timedelta

import pytest

from redact_api.aws import PersistenceConflictError
from redact_api.domain import (
    Job,
    JobStatus,
    PageManifest,
    RedactionRegion,
    RegionSource,
    SourceType,
    WorkerMode,
    WorkerSubmission,
)


pytestmark = pytest.mark.localstack
NOW = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


def make_job(job_id: str = "job-123", owner_id: str = "user-456") -> Job:
    prefix = f"users/{owner_id}/jobs/{job_id}/"
    return Job(
        id=job_id,
        owner_id=owner_id,
        source_type=SourceType.PDF,
        source_key=f"{prefix}source",
        output_key=f"{prefix}output",
        status=JobStatus.UPLOADING,
        page_count=0,
        completed_pages=0,
        created_at=NOW,
        expires_at=NOW + timedelta(hours=24),
        model_versions={},
        version=1,
    )


def make_manifest(version: int = 1) -> PageManifest:
    suggestion = RedactionRegion(
        id="region-1",
        page_number=1,
        x=0.1,
        y=0.1,
        width=0.2,
        height=0.2,
        source=RegionSource.AUTOMATIC,
        category="EMAIL",
        confidence=0.9,
        selected=True,
    )
    return PageManifest(
        job_id="job-123",
        page_number=1,
        suggestions=(suggestion,),
        regions=(suggestion,),
        version=version,
        last_saved_at=NOW,
    )


def test_dynamodb_round_trip_listing_ttl_and_conflict(
    aws_resources: dict[str, object],
) -> None:
    jobs = aws_resources["jobs"]
    table = aws_resources["table"]
    older = make_job("job-older")
    newer = make_job("job-newer").model_copy(
        update={"created_at": NOW + timedelta(minutes=1)}
    )
    jobs.create(older)
    jobs.create(newer)

    assert jobs.get(older.id) == older
    assert [job.id for job in jobs.list_owner(older.owner_id)] == [
        "job-newer",
        "job-older",
    ]
    raw = table.get_item(Key={"id": older.id})["Item"]
    assert raw["ttl"] == int(older.expires_at.timestamp())
    assert "filename" not in raw
    assert "manifest" not in raw

    updated = older.model_copy(update={"version": 2})
    jobs.save(updated, expected_version=1)
    with pytest.raises(PersistenceConflictError):
        jobs.save(updated.model_copy(update={"version": 3}), expected_version=1)


def test_s3_presigning_objects_and_manifest_conflicts(
    aws_resources: dict[str, object],
) -> None:
    objects = aws_resources["objects"]
    s3 = aws_resources["s3"]
    source_key = "users/user-456/jobs/job-123/source"
    upload_id = objects.create_multipart_upload(source_key)

    upload_url = objects.presign_upload_part(
        source_key,
        upload_id=upload_id,
        part_number=1,
    )
    assert source_key in upload_url
    assert not objects.object_exists(source_key)

    s3.put_object(Bucket="redact-files", Key=source_key, Body=b"document")
    assert objects.object_exists(source_key)
    assert source_key in objects.presign_download(source_key)

    stored = objects.create_manifest("user-456", make_manifest())
    loaded = objects.get_manifest("user-456", "job-123", 1)
    assert loaded == stored

    next_manifest = stored.manifest.model_copy(update={"version": 2})
    saved = objects.save_manifest(
        "user-456",
        next_manifest,
        expected_etag=stored.etag,
    )
    assert saved.manifest.version == 2
    with pytest.raises(PersistenceConflictError):
        objects.save_manifest(
            "user-456",
            saved.manifest.model_copy(update={"version": 3}),
            expected_etag=stored.etag,
        )


@pytest.mark.parametrize("mode", [WorkerMode.ANALYZE, WorkerMode.RENDER])
def test_recording_batch_fake_is_idempotent(
    aws_resources: dict[str, object],
    mode: WorkerMode,
) -> None:
    batch = aws_resources["batch"]
    submission = WorkerSubmission(
        job_id="job-123",
        owner_id="user-456",
        source_key="users/user-456/jobs/job-123/source",
        output_key="users/user-456/jobs/job-123/output",
        mode=mode,
        idempotency_token=f"job-123:{mode.value}:2",
    )

    assert batch.submit(submission) == submission
    assert batch.submit(submission) == submission
    assert list(batch.submissions.values()) == [submission]
