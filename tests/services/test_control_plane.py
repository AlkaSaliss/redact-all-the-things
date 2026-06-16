from datetime import UTC, datetime, timedelta

import pytest

from redact_api.domain import (
    FailureCode,
    JobStatus,
    PageManifest,
    RedactionRegion,
    RegionSource,
    SourceType,
    WorkerMode,
)
from redact_api.services import (
    ControlPlaneService,
    InvalidRequestError,
    JobNotFoundError,
    ManifestConflictError,
)


pytestmark = pytest.mark.localstack
NOW = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


@pytest.fixture
def clock() -> dict[str, datetime]:
    return {"now": NOW}


@pytest.fixture
def service(
    aws_resources: dict[str, object],
    clock: dict[str, datetime],
) -> ControlPlaneService:
    return ControlPlaneService(
        aws_resources["jobs"],
        aws_resources["objects"],
        aws_resources["batch"],
        clock=lambda: clock["now"],
        id_factory=lambda: "job-123",
    )


def upload_part(
    aws_resources: dict[str, object],
    *,
    upload_id: str,
) -> tuple[dict[str, object], ...]:
    response = aws_resources["s3"].upload_part(
        Bucket="redact-files",
        Key="users/user-456/jobs/job-123/source",
        UploadId=upload_id,
        PartNumber=1,
        Body=b"document",
    )
    return ({"PartNumber": 1, "ETag": response["ETag"]},)


def set_status(
    aws_resources: dict[str, object],
    status: JobStatus,
    *,
    failure_code: FailureCode | None = None,
) -> None:
    jobs = aws_resources["jobs"]
    job = jobs.get("job-123")
    jobs.save(
        job.model_copy(
            update={
                "status": status,
                "failure_code": failure_code,
                "version": job.version + 1,
            }
        ),
        expected_version=job.version,
    )


def create_ready_manifest(aws_resources: dict[str, object]) -> PageManifest:
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
    manifest = PageManifest(
        job_id="job-123",
        page_number=1,
        suggestions=(suggestion,),
        regions=(suggestion,),
        version=1,
        last_saved_at=NOW,
    )
    aws_resources["objects"].create_manifest("user-456", manifest)
    return manifest


def test_create_list_get_ownership_and_exact_expiry(
    service: ControlPlaneService,
    clock: dict[str, datetime],
) -> None:
    job, upload_id, upload_parts = service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )

    assert job.status is JobStatus.UPLOADING
    assert job.expires_at == NOW + timedelta(hours=24)
    assert upload_id
    assert job.source_key in upload_parts[0][1]
    assert service.list_jobs("user-456") == [job]
    assert service.get_job("user-456", job.id) == job
    with pytest.raises(JobNotFoundError):
        service.get_job("other-user", job.id)

    clock["now"] = job.expires_at
    assert service.list_jobs("user-456") == []
    with pytest.raises(JobNotFoundError):
        service.get_job("user-456", job.id)


@pytest.mark.parametrize("size", [0, 100 * 1024 * 1024 + 1])
def test_create_rejects_invalid_sizes(
    service: ControlPlaneService,
    size: int,
) -> None:
    with pytest.raises(InvalidRequestError):
        service.create_job(
            "user-456",
            source_type=SourceType.PDF,
            size_bytes=size,
        )


def test_upload_completion_is_idempotent(
    service: ControlPlaneService,
    aws_resources: dict[str, object],
) -> None:
    job, upload_id, _ = service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    with pytest.raises(InvalidRequestError):
        service.complete_upload(
            "user-456",
            job.id,
            upload_id="",
            parts=(),
        )

    parts = upload_part(aws_resources, upload_id=upload_id)
    queued = service.complete_upload(
        "user-456",
        job.id,
        upload_id=upload_id,
        parts=parts,
    )
    repeated = service.complete_upload(
        "user-456",
        job.id,
        upload_id=upload_id,
        parts=parts,
    )

    assert queued.status is JobStatus.QUEUED
    assert repeated == queued
    submissions = list(aws_resources["batch"].submissions.values())
    assert len(submissions) == 1
    assert submissions[0].mode is WorkerMode.ANALYZE


def test_export_requires_acknowledgement_and_is_idempotent(
    service: ControlPlaneService,
    aws_resources: dict[str, object],
) -> None:
    service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    set_status(aws_resources, JobStatus.READY)

    with pytest.raises(InvalidRequestError):
        service.confirm_export("user-456", "job-123", acknowledged=False)
    exporting = service.confirm_export(
        "user-456",
        "job-123",
        acknowledged=True,
    )
    assert service.confirm_export(
        "user-456",
        "job-123",
        acknowledged=True,
    ) == exporting
    submissions = list(aws_resources["batch"].submissions.values())
    assert len(submissions) == 1
    assert submissions[0].mode is WorkerMode.RENDER


def test_retry_allows_only_transient_failures(
    service: ControlPlaneService,
    aws_resources: dict[str, object],
) -> None:
    service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    set_status(
        aws_resources,
        JobStatus.FAILED,
        failure_code=FailureCode.ANALYZE_TRANSIENT,
    )
    assert service.retry("user-456", "job-123").status is JobStatus.QUEUED


def test_retry_rejects_permanent_failures(
    service: ControlPlaneService,
    aws_resources: dict[str, object],
) -> None:
    service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    set_status(
        aws_resources,
        JobStatus.FAILED,
        failure_code=FailureCode.PROCESSING_FAILED,
    )
    with pytest.raises(InvalidRequestError):
        service.retry("user-456", "job-123")


@pytest.mark.parametrize(
    ("initial_status", "operation", "failure_code"),
    [
        (
            JobStatus.UPLOADING,
            "analyze",
            FailureCode.ANALYZE_TRANSIENT,
        ),
        (
            JobStatus.READY,
            "render",
            FailureCode.RENDER_TRANSIENT,
        ),
    ],
)
def test_submission_failure_becomes_retryable(
    aws_resources: dict[str, object],
    initial_status: JobStatus,
    operation: str,
    failure_code: FailureCode,
) -> None:
    class FailingBatch:
        def submit(self, submission: object) -> None:
            raise RuntimeError("unavailable")

    service = ControlPlaneService(
        aws_resources["jobs"],
        aws_resources["objects"],
        FailingBatch(),
        clock=lambda: NOW,
        id_factory=lambda: "job-123",
    )
    job, upload_id, _ = service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    if initial_status is JobStatus.READY:
        set_status(aws_resources, JobStatus.READY)
        with pytest.raises(InvalidRequestError):
            service.confirm_export(
                "user-456",
                job.id,
                acknowledged=True,
            )
    else:
        parts = upload_part(aws_resources, upload_id=upload_id)
        with pytest.raises(InvalidRequestError):
            service.complete_upload(
                "user-456",
                job.id,
                upload_id=upload_id,
                parts=parts,
            )

    failed = aws_resources["jobs"].get(job.id)
    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is failure_code


def test_manifest_read_save_preserves_suggestions_and_conflicts(
    service: ControlPlaneService,
    aws_resources: dict[str, object],
) -> None:
    service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    set_status(aws_resources, JobStatus.READY)
    original = create_ready_manifest(aws_resources)
    manual = RedactionRegion(
        id="manual-1",
        page_number=1,
        x=0.4,
        y=0.4,
        width=0.2,
        height=0.2,
        source=RegionSource.MANUAL,
        category="MANUAL",
        confidence=None,
        selected=True,
    )

    assert service.get_manifest("user-456", "job-123", 1) == original
    saved = service.save_manifest(
        "user-456",
        "job-123",
        1,
        expected_version=1,
        regions=(manual,),
    )
    assert saved.suggestions == original.suggestions
    assert saved.regions == (manual,)
    assert saved.version == 2
    with pytest.raises(ManifestConflictError):
        service.save_manifest(
            "user-456",
            "job-123",
            1,
            expected_version=1,
            regions=(manual,),
        )


def test_download_requires_complete_existing_output(
    service: ControlPlaneService,
    aws_resources: dict[str, object],
) -> None:
    service.create_job(
        "user-456",
        source_type=SourceType.PDF,
        size_bytes=1024,
    )
    with pytest.raises(InvalidRequestError):
        service.authorize_download("user-456", "job-123")

    set_status(aws_resources, JobStatus.COMPLETE)
    with pytest.raises(InvalidRequestError):
        service.authorize_download("user-456", "job-123")

    aws_resources["s3"].put_object(
        Bucket="redact-files",
        Key="users/user-456/jobs/job-123/output",
        Body=b"redacted",
    )
    assert "users/user-456/jobs/job-123/output" in service.authorize_download(
        "user-456",
        "job-123",
    )
