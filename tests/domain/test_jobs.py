from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from redact_api.domain import (
    FailureCode,
    Job,
    JobStatus,
    SourceType,
    WorkerMode,
    WorkerSubmission,
)


NOW = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


def make_job(**overrides: object) -> Job:
    values: dict[str, object] = {
        "id": "job-123",
        "owner_id": "user-456",
        "source_type": SourceType.PDF,
        "source_key": "users/user-456/jobs/job-123/source",
        "output_key": "users/user-456/jobs/job-123/output",
        "status": JobStatus.UPLOADING,
        "page_count": 0,
        "completed_pages": 0,
        "created_at": NOW,
        "expires_at": NOW + timedelta(hours=24),
        "model_versions": {},
        "failure_code": None,
        "version": 1,
    }
    values.update(overrides)
    return Job.model_validate(values)


def test_job_accepts_the_persistent_contract() -> None:
    job = make_job()

    assert job.status is JobStatus.UPLOADING
    assert job.expires_at - job.created_at == timedelta(hours=24)
    assert job.model_dump(mode="json")["source_type"] == "pdf"


@pytest.mark.parametrize("source_type", ["docx", "", "PDF"])
def test_job_rejects_unsupported_source_types(source_type: str) -> None:
    with pytest.raises(ValidationError):
        make_job(source_type=source_type)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("created_at", datetime(2026, 6, 15, 12, 0)),
        ("expires_at", NOW),
        ("page_count", 201),
        ("completed_pages", -1),
        ("version", 0),
    ],
)
def test_job_rejects_invalid_limits(field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        make_job(**{field: value})


def test_job_rejects_progress_beyond_page_count() -> None:
    with pytest.raises(ValidationError):
        make_job(page_count=2, completed_pages=3)


def test_job_rejects_foreign_object_namespaces() -> None:
    with pytest.raises(ValidationError):
        make_job(source_key="users/other/jobs/job-123/source")


def test_job_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        make_job(filename="sensitive.pdf")


def test_failed_job_requires_a_safe_failure_code() -> None:
    with pytest.raises(ValidationError):
        make_job(status=JobStatus.FAILED)


def test_non_failed_job_rejects_a_failure_code() -> None:
    with pytest.raises(ValidationError):
        make_job(failure_code=FailureCode.ANALYZE_TRANSIENT)


def test_worker_submission_serializes_stable_contract() -> None:
    submission = WorkerSubmission(
        job_id="job-123",
        owner_id="user-456",
        source_key="users/user-456/jobs/job-123/source",
        output_key="users/user-456/jobs/job-123/output",
        mode=WorkerMode.ANALYZE,
        idempotency_token="job-123:queued:2",
    )

    assert submission.model_dump(mode="json") == {
        "job_id": "job-123",
        "owner_id": "user-456",
        "source_key": "users/user-456/jobs/job-123/source",
        "output_key": "users/user-456/jobs/job-123/output",
        "mode": "analyze",
        "idempotency_token": "job-123:queued:2",
    }
