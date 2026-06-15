"""Validated job and page-manifest contracts."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from math import isfinite
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)


Identifier = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._-]*$",
    ),
]


class SourceType(StrEnum):
    PDF = "pdf"
    JPEG = "jpeg"
    PNG = "png"


class JobStatus(StrEnum):
    UPLOADING = "uploading"
    QUEUED = "queued"
    ANALYZING = "analyzing"
    READY = "ready"
    EXPORTING = "exporting"
    COMPLETE = "complete"
    FAILED = "failed"
    EXPIRED = "expired"


class WorkerMode(StrEnum):
    ANALYZE = "analyze"
    RENDER = "render"


class FailureCode(StrEnum):
    ANALYZE_TRANSIENT = "analyze_transient"
    ANALYZE_SPOT_INTERRUPTED = "analyze_spot_interrupted"
    RENDER_TRANSIENT = "render_transient"
    RENDER_SPOT_INTERRUPTED = "render_spot_interrupted"
    VALIDATION_FAILED = "validation_failed"
    UNSUPPORTED_CONTENT = "unsupported_content"
    PROCESSING_FAILED = "processing_failed"


class RegionSource(StrEnum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class InvalidTransitionError(ValueError):
    """Raised when a job status transition violates the lifecycle."""


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


def _is_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


class Job(ContractModel):
    id: Identifier
    owner_id: Identifier
    source_type: SourceType
    source_key: str = Field(min_length=1)
    output_key: str = Field(min_length=1)
    status: JobStatus
    page_count: int = Field(ge=0, le=200)
    completed_pages: int = Field(ge=0)
    created_at: datetime
    expires_at: datetime
    model_versions: dict[str, str]
    failure_code: FailureCode | None = None
    version: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_contract(self) -> Job:
        if not _is_aware(self.created_at) or not _is_aware(self.expires_at):
            raise ValueError("job timestamps must be timezone-aware")
        if self.expires_at <= self.created_at:
            raise ValueError("expires_at must be after created_at")
        if self.completed_pages > self.page_count:
            raise ValueError("completed_pages cannot exceed page_count")

        prefix = f"users/{self.owner_id}/jobs/{self.id}/"
        if self.source_key != f"{prefix}source":
            raise ValueError("source_key is outside the owner job namespace")
        if self.output_key != f"{prefix}output":
            raise ValueError("output_key is outside the owner job namespace")

        if self.status is JobStatus.FAILED and self.failure_code is None:
            raise ValueError("failed jobs require a safe failure code")
        if self.status is not JobStatus.FAILED and self.failure_code is not None:
            raise ValueError("only failed jobs may contain a failure code")
        return self


class WorkerSubmission(ContractModel):
    job_id: Identifier
    owner_id: Identifier
    source_key: str = Field(min_length=1)
    output_key: str = Field(min_length=1)
    mode: WorkerMode
    idempotency_token: str = Field(min_length=1, max_length=256)

    @model_validator(mode="after")
    def validate_keys(self) -> WorkerSubmission:
        prefix = f"users/{self.owner_id}/jobs/{self.job_id}/"
        if self.source_key != f"{prefix}source":
            raise ValueError("source_key is outside the owner job namespace")
        if self.output_key != f"{prefix}output":
            raise ValueError("output_key is outside the owner job namespace")
        return self


class RedactionRegion(ContractModel):
    id: Identifier
    page_number: int = Field(ge=1, le=200)
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)
    source: RegionSource
    category: str = Field(min_length=1, max_length=128)
    confidence: float | None = Field(default=None, ge=0, le=1)
    selected: bool

    @model_validator(mode="after")
    def validate_geometry(self) -> RedactionRegion:
        values = (self.x, self.y, self.width, self.height)
        if not all(isfinite(value) for value in values):
            raise ValueError("region coordinates must be finite")
        if self.x + self.width > 1 or self.y + self.height > 1:
            raise ValueError("region extends beyond normalized page bounds")
        if self.source is RegionSource.AUTOMATIC and self.confidence is None:
            raise ValueError("automatic regions require confidence")
        if self.source is RegionSource.MANUAL and self.confidence is not None:
            raise ValueError("manual regions cannot contain confidence")
        return self


class PageManifest(ContractModel):
    job_id: Identifier
    page_number: int = Field(ge=1, le=200)
    suggestions: tuple[RedactionRegion, ...]
    regions: tuple[RedactionRegion, ...]
    version: int = Field(ge=1)
    last_saved_at: datetime

    @model_validator(mode="after")
    def validate_contract(self) -> PageManifest:
        if not _is_aware(self.last_saved_at):
            raise ValueError("last_saved_at must be timezone-aware")
        for suggestion in self.suggestions:
            if suggestion.source is not RegionSource.AUTOMATIC:
                raise ValueError("manifest suggestions must be automatic")
            if suggestion.page_number != self.page_number:
                raise ValueError("suggestion page does not match manifest")
        if any(region.page_number != self.page_number for region in self.regions):
            raise ValueError("region page does not match manifest")
        return self


_NORMAL_TRANSITIONS: dict[JobStatus, frozenset[JobStatus]] = {
    JobStatus.UPLOADING: frozenset({JobStatus.QUEUED}),
    JobStatus.QUEUED: frozenset({JobStatus.ANALYZING, JobStatus.FAILED}),
    JobStatus.ANALYZING: frozenset({JobStatus.READY, JobStatus.FAILED}),
    JobStatus.READY: frozenset({JobStatus.EXPORTING}),
    JobStatus.EXPORTING: frozenset({JobStatus.COMPLETE, JobStatus.FAILED}),
}

_RETRY_MODES: dict[FailureCode, WorkerMode] = {
    FailureCode.ANALYZE_TRANSIENT: WorkerMode.ANALYZE,
    FailureCode.ANALYZE_SPOT_INTERRUPTED: WorkerMode.ANALYZE,
    FailureCode.RENDER_TRANSIENT: WorkerMode.RENDER,
    FailureCode.RENDER_SPOT_INTERRUPTED: WorkerMode.RENDER,
}


def is_expired(job: Job, now: datetime) -> bool:
    if not _is_aware(now):
        raise ValueError("now must be timezone-aware")
    return now >= job.expires_at


def retry_mode(code: FailureCode) -> WorkerMode | None:
    return _RETRY_MODES.get(code)


def submission_token(job: Job, target: JobStatus) -> str:
    return f"{job.id}:{target.value}:{job.version + 1}"


def transition_job(
    job: Job,
    target: JobStatus,
    *,
    now: datetime,
    failure_code: FailureCode | None = None,
) -> Job:
    if target is JobStatus.EXPIRED:
        if not is_expired(job, now):
            raise InvalidTransitionError("job has not expired")
    elif is_expired(job, now):
        raise InvalidTransitionError("expired jobs cannot transition")
    elif job.status is JobStatus.FAILED:
        mode = retry_mode(job.failure_code) if job.failure_code is not None else None
        expected = (
            JobStatus.QUEUED
            if mode is WorkerMode.ANALYZE
            else JobStatus.EXPORTING
            if mode is WorkerMode.RENDER
            else None
        )
        if target is not expected:
            raise InvalidTransitionError("failure is not retryable in that mode")
    elif target not in _NORMAL_TRANSITIONS.get(job.status, frozenset()):
        raise InvalidTransitionError(
            f"cannot transition {job.status.value} to {target.value}"
        )

    if target is JobStatus.FAILED and failure_code is None:
        raise InvalidTransitionError("failed transition requires failure code")
    if target is not JobStatus.FAILED and failure_code is not None:
        raise InvalidTransitionError("failure code requires failed status")

    return job.model_copy(
        update={
            "status": target,
            "failure_code": failure_code,
            "version": job.version + 1,
        }
    )


def save_manifest(
    manifest: PageManifest,
    *,
    regions: tuple[RedactionRegion, ...],
    now: datetime,
) -> PageManifest:
    return PageManifest(
        job_id=manifest.job_id,
        page_number=manifest.page_number,
        suggestions=manifest.suggestions,
        regions=regions,
        version=manifest.version + 1,
        last_saved_at=now,
    )
