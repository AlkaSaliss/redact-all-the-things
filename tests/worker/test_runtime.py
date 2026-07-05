from datetime import UTC, datetime

from redact_api.domain import Job, JobStatus, SourceType, WorkerMode, WorkerSubmission
from redact_api.worker_runtime import parse_args, run_submission


NOW = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)


def make_job(status: JobStatus = JobStatus.QUEUED) -> Job:
    return Job(
        id="job-123",
        owner_id="user-456",
        source_type=SourceType.PDF,
        source_key="users/user-456/jobs/job-123/source",
        output_key="users/user-456/jobs/job-123/output",
        status=status,
        page_count=0,
        completed_pages=0,
        created_at=NOW,
        expires_at=datetime(2026, 7, 5, 12, 0, tzinfo=UTC),
        model_versions={},
        version=2,
    )


class RecordingJobs:
    def __init__(self, job: Job) -> None:
        self.job = job

    def get(self, job_id: str) -> Job | None:
        return self.job if job_id == self.job.id else None

    def save(self, job: Job, *, expected_version: int) -> None:
        self.job = job


class RecordingObjects:
    def __init__(self) -> None:
        self.source_reads: list[str] = []

    def get_source_object(self, key: str) -> bytes:
        self.source_reads.append(key)
        return b"%PDF-1.4\n"

    def put_page_artifact(self, key: str, content: bytes) -> None:
        pass

    def put_page_artifact_index(self, key: str, content: bytes) -> None:
        pass

    def get_page_artifact_index(self, key: str) -> bytes:
        raise AssertionError("not used")

    def get_page_artifact(self, key: str) -> bytes:
        raise AssertionError("not used")

    def put_ocr_page_text(self, key: str, content: bytes) -> None:
        pass

    def get_manifest(self, owner_id: str, job_id: str, page_number: int) -> None:
        return None

    def create_manifest(self, owner_id: str, manifest: object) -> object:
        return manifest


def make_submission(mode: WorkerMode = WorkerMode.ANALYZE) -> WorkerSubmission:
    return WorkerSubmission(
        job_id="job-123",
        owner_id="user-456",
        source_key="users/user-456/jobs/job-123/source",
        output_key="users/user-456/jobs/job-123/output",
        mode=mode,
        idempotency_token=f"job-123:{mode.value}:2",
    )


def test_parse_args_builds_worker_submission() -> None:
    submission = parse_args(
        [
            "analyze",
            "--job-id",
            "job-123",
            "--owner-id",
            "user-456",
            "--source-key",
            "users/user-456/jobs/job-123/source",
            "--output-key",
            "users/user-456/jobs/job-123/output",
            "--idempotency-token",
            "job-123:queued:2",
        ]
    )

    assert submission.mode is WorkerMode.ANALYZE
    assert submission.job_id == "job-123"


def test_run_submission_rejects_mismatched_job() -> None:
    jobs = RecordingJobs(make_job())
    submission = make_submission().model_copy(update={"owner_id": "other"})

    try:
        run_submission(
            submission,
            jobs=jobs,
            objects=RecordingObjects(),
            now=lambda: NOW,
        )
    except RuntimeError as error:
        assert str(error) == "worker submission does not match persisted job"
    else:
        raise AssertionError("expected mismatch rejection")
