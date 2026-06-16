from datetime import UTC, datetime, timedelta

import pytest

from redact_api.domain import (
    FailureCode,
    InvalidTransitionError,
    Job,
    JobStatus,
    SourceType,
    WorkerMode,
    is_expired,
    retry_mode,
    submission_token,
    transition_job,
)


NOW = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


def make_job(status: JobStatus, **overrides: object) -> Job:
    values: dict[str, object] = {
        "id": "job-123",
        "owner_id": "user-456",
        "source_type": SourceType.PDF,
        "source_key": "users/user-456/jobs/job-123/source",
        "output_key": "users/user-456/jobs/job-123/output",
        "status": status,
        "page_count": 1,
        "completed_pages": 0,
        "created_at": NOW,
        "expires_at": NOW + timedelta(hours=24),
        "model_versions": {},
        "failure_code": None,
        "version": 1,
    }
    values.update(overrides)
    return Job.model_validate(values)


@pytest.mark.parametrize(
    ("source", "target"),
    [
        (JobStatus.UPLOADING, JobStatus.QUEUED),
        (JobStatus.QUEUED, JobStatus.ANALYZING),
        (JobStatus.ANALYZING, JobStatus.READY),
        (JobStatus.READY, JobStatus.EXPORTING),
        (JobStatus.EXPORTING, JobStatus.COMPLETE),
    ],
)
def test_normal_transitions_increment_version(
    source: JobStatus, target: JobStatus
) -> None:
    updated = transition_job(make_job(source), target, now=NOW)

    assert updated.status is target
    assert updated.version == 2


@pytest.mark.parametrize(
    "source",
    [JobStatus.QUEUED, JobStatus.ANALYZING, JobStatus.EXPORTING],
)
def test_processing_can_fail(source: JobStatus) -> None:
    code = (
        FailureCode.ANALYZE_TRANSIENT
        if source in {JobStatus.QUEUED, JobStatus.ANALYZING}
        else FailureCode.RENDER_TRANSIENT
    )

    updated = transition_job(
        make_job(source), JobStatus.FAILED, now=NOW, failure_code=code
    )

    assert updated.status is JobStatus.FAILED
    assert updated.failure_code is code


def test_invalid_transition_is_rejected() -> None:
    with pytest.raises(InvalidTransitionError):
        transition_job(make_job(JobStatus.UPLOADING), JobStatus.READY, now=NOW)


@pytest.mark.parametrize(
    ("code", "mode"),
    [
        (FailureCode.ANALYZE_TRANSIENT, WorkerMode.ANALYZE),
        (FailureCode.ANALYZE_SPOT_INTERRUPTED, WorkerMode.ANALYZE),
        (FailureCode.RENDER_TRANSIENT, WorkerMode.RENDER),
        (FailureCode.RENDER_SPOT_INTERRUPTED, WorkerMode.RENDER),
    ],
)
def test_retryable_failures_select_the_worker_mode(
    code: FailureCode, mode: WorkerMode
) -> None:
    assert retry_mode(code) is mode


@pytest.mark.parametrize(
    "code",
    [
        FailureCode.VALIDATION_FAILED,
        FailureCode.UNSUPPORTED_CONTENT,
        FailureCode.PROCESSING_FAILED,
    ],
)
def test_permanent_failures_are_not_retryable(code: FailureCode) -> None:
    assert retry_mode(code) is None


def test_retry_transition_clears_failure_code() -> None:
    failed = make_job(
        JobStatus.FAILED, failure_code=FailureCode.ANALYZE_TRANSIENT
    )

    updated = transition_job(failed, JobStatus.QUEUED, now=NOW)

    assert updated.failure_code is None
    assert updated.version == 2


def test_expiry_is_exact_at_the_deadline() -> None:
    job = make_job(JobStatus.READY)

    assert not is_expired(job, job.expires_at - timedelta(microseconds=1))
    assert is_expired(job, job.expires_at)


def test_only_expired_jobs_can_transition_to_expired() -> None:
    job = make_job(JobStatus.READY)

    with pytest.raises(InvalidTransitionError):
        transition_job(job, JobStatus.EXPIRED, now=job.expires_at - timedelta(seconds=1))

    expired = transition_job(job, JobStatus.EXPIRED, now=job.expires_at)
    assert expired.status is JobStatus.EXPIRED


def test_submission_token_is_stable_for_the_transition_version() -> None:
    job = make_job(JobStatus.UPLOADING)

    assert submission_token(job, JobStatus.QUEUED) == "job-123:queued:2"
    assert submission_token(job, JobStatus.QUEUED) == "job-123:queued:2"
