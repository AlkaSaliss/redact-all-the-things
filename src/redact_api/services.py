"""Application services for owner-scoped job workflows."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from uuid import uuid4

from redact_api.aws import (
    AwsBatchSubmitter,
    DynamoJobRepository,
    PersistenceConflictError,
    RecordingBatchSubmitter,
    S3ObjectRepository,
)
from redact_api.domain import (
    FailureCode,
    InvalidTransitionError,
    Job,
    JobStatus,
    PageManifest,
    RedactionRegion,
    SourceType,
    WorkerMode,
    WorkerSubmission,
    is_expired,
    retry_mode,
    save_manifest,
    submission_token,
    transition_job,
)


MAX_FILE_SIZE = 100 * 1024 * 1024
MULTIPART_PART_SIZE = 5 * 1024 * 1024


class JobNotFoundError(LookupError):
    """Used for missing, foreign-owned, and expired jobs."""


class InvalidRequestError(ValueError):
    """Raised when an operation is invalid for the current job."""


class ManifestConflictError(RuntimeError):
    """Raised when a page manifest has changed concurrently."""


class ControlPlaneService:
    """Coordinate owner-scoped job workflows across persistent AWS services."""

    def __init__(
        self,
        jobs: DynamoJobRepository,
        objects: S3ObjectRepository,
        batch: RecordingBatchSubmitter | AwsBatchSubmitter,
        *,
        clock: Callable[[], datetime],
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._jobs = jobs
        self._objects = objects
        self._batch = batch
        self._clock = clock
        self._id_factory = id_factory or (lambda: str(uuid4()))

    def create_job(
        self,
        owner_id: str,
        *,
        source_type: SourceType,
        size_bytes: int,
    ) -> tuple[Job, str, tuple[tuple[int, str], ...]]:
        if size_bytes <= 0 or size_bytes > MAX_FILE_SIZE:
            raise InvalidRequestError("file size must be between 1 byte and 100 MB")
        job_id = self._id_factory()
        now = self._clock()
        prefix = f"users/{owner_id}/jobs/{job_id}/"
        job = Job(
            id=job_id,
            owner_id=owner_id,
            source_type=source_type,
            source_key=f"{prefix}source",
            output_key=f"{prefix}output",
            status=JobStatus.UPLOADING,
            page_count=0,
            completed_pages=0,
            created_at=now,
            expires_at=now + timedelta(hours=24),
            model_versions={},
            version=1,
        )
        self._jobs.create(job)
        upload_id = self._objects.create_multipart_upload(job.source_key)
        part_count = (size_bytes + MULTIPART_PART_SIZE - 1) // MULTIPART_PART_SIZE
        upload_parts = tuple(
            (
                part_number,
                self._objects.presign_upload_part(
                    job.source_key,
                    upload_id=upload_id,
                    part_number=part_number,
                ),
            )
            for part_number in range(1, part_count + 1)
        )
        return job, upload_id, upload_parts

    def list_jobs(self, owner_id: str) -> list[Job]:
        now = self._clock()
        return [
            job
            for job in self._jobs.list_owner(owner_id)
            if not is_expired(job, now)
        ]

    def get_job(self, owner_id: str, job_id: str) -> Job:
        job = self._jobs.get(job_id)
        if (
            job is None
            or job.owner_id != owner_id
            or is_expired(job, self._clock())
        ):
            raise JobNotFoundError(job_id)
        return job

    def complete_upload(
        self,
        owner_id: str,
        job_id: str,
        *,
        upload_id: str,
        parts: tuple[dict[str, object], ...],
    ) -> Job:
        job = self.get_job(owner_id, job_id)
        if job.status is JobStatus.QUEUED:
            return job
        if job.status is not JobStatus.UPLOADING:
            raise InvalidRequestError("job is not awaiting upload")
        if not upload_id or not parts:
            raise InvalidRequestError("completed multipart parts are required")
        self._objects.complete_multipart_upload(
            job.source_key,
            upload_id=upload_id,
            parts=parts,
        )
        if not self._objects.object_exists(job.source_key):
            raise InvalidRequestError("uploaded source object does not exist")
        return self._transition_and_submit(job, JobStatus.QUEUED, WorkerMode.ANALYZE)

    def confirm_export(
        self,
        owner_id: str,
        job_id: str,
        *,
        acknowledged: bool,
    ) -> Job:
        job = self.get_job(owner_id, job_id)
        if not acknowledged:
            raise InvalidRequestError("export acknowledgement is required")
        if job.status is JobStatus.EXPORTING:
            return job
        if job.status is not JobStatus.READY:
            raise InvalidRequestError("job is not ready for export")
        return self._transition_and_submit(
            job,
            JobStatus.EXPORTING,
            WorkerMode.RENDER,
        )

    def retry(self, owner_id: str, job_id: str) -> Job:
        job = self.get_job(owner_id, job_id)
        if job.status is not JobStatus.FAILED or job.failure_code is None:
            raise InvalidRequestError("job is not retryable")
        mode = retry_mode(job.failure_code)
        if mode is None:
            raise InvalidRequestError("job failure is permanent")
        target = (
            JobStatus.QUEUED
            if mode is WorkerMode.ANALYZE
            else JobStatus.EXPORTING
        )
        return self._transition_and_submit(job, target, mode)

    def get_manifest(
        self,
        owner_id: str,
        job_id: str,
        page_number: int,
    ) -> PageManifest:
        job = self.get_job(owner_id, job_id)
        self._require_manifest_status(job)
        stored = self._objects.get_manifest(owner_id, job_id, page_number)
        if stored is None:
            raise JobNotFoundError(f"{job_id}:{page_number}")
        return stored.manifest

    def save_manifest(
        self,
        owner_id: str,
        job_id: str,
        page_number: int,
        *,
        expected_version: int,
        regions: tuple[RedactionRegion, ...],
    ) -> PageManifest:
        job = self.get_job(owner_id, job_id)
        self._require_manifest_status(job)
        stored = self._objects.get_manifest(owner_id, job_id, page_number)
        if stored is None:
            raise JobNotFoundError(f"{job_id}:{page_number}")
        if stored.manifest.version != expected_version:
            raise ManifestConflictError("manifest version conflict")
        updated = save_manifest(
            stored.manifest,
            regions=regions,
            now=self._clock(),
        )
        try:
            return self._objects.save_manifest(
                owner_id,
                updated,
                expected_etag=stored.etag,
            ).manifest
        except PersistenceConflictError as error:
            raise ManifestConflictError("manifest version conflict") from error

    def authorize_download(self, owner_id: str, job_id: str) -> str:
        job = self.get_job(owner_id, job_id)
        if job.status is not JobStatus.COMPLETE:
            raise InvalidRequestError("job output is not complete")
        if not self._objects.object_exists(job.output_key):
            raise InvalidRequestError("job output object does not exist")
        return self._objects.presign_download(job.output_key)

    def _transition_and_submit(
        self,
        job: Job,
        target: JobStatus,
        mode: WorkerMode,
    ) -> Job:
        """Persist a transition and submit its corresponding worker request."""

        try:
            updated = transition_job(job, target, now=self._clock())
            self._jobs.save(updated, expected_version=job.version)
        except (InvalidTransitionError, PersistenceConflictError) as error:
            raise InvalidRequestError(str(error)) from error
        submission = WorkerSubmission(
            job_id=job.id,
            owner_id=job.owner_id,
            source_key=job.source_key,
            output_key=job.output_key,
            mode=mode,
            idempotency_token=submission_token(job, target),
        )
        try:
            self._batch.submit(submission)
        except Exception as error:
            failure_code = (
                FailureCode.ANALYZE_TRANSIENT
                if mode is WorkerMode.ANALYZE
                else FailureCode.RENDER_TRANSIENT
            )
            failed = transition_job(
                updated,
                JobStatus.FAILED,
                now=self._clock(),
                failure_code=failure_code,
            )
            self._jobs.save(failed, expected_version=updated.version)
            raise InvalidRequestError("worker submission failed") from error
        return updated

    @staticmethod
    def _require_manifest_status(job: Job) -> None:
        if job.status not in {JobStatus.READY, JobStatus.FAILED}:
            raise InvalidRequestError("page manifests are not available")
