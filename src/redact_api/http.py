"""FastAPI control-plane boundary."""

from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from redact_api.domain import Job, PageManifest, RedactionRegion, SourceType
from redact_api.services import (
    ControlPlaneService,
    InvalidRequestError,
    JobNotFoundError,
    ManifestConflictError,
)


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateJobRequest(ApiModel):
    source_type: SourceType
    size_bytes: int = Field(gt=0, le=100 * 1024 * 1024)


class UploadPartAuthorization(ApiModel):
    part_number: int
    upload_url: str


class CreateJobResponse(ApiModel):
    job: Job
    upload_id: str
    upload_parts: tuple[UploadPartAuthorization, ...]


class CompletedUploadPart(ApiModel):
    part_number: int = Field(ge=1)
    etag: str = Field(min_length=1)


class CompleteUploadRequest(ApiModel):
    upload_id: str = Field(min_length=1)
    parts: tuple[CompletedUploadPart, ...] = Field(min_length=1)


class SaveManifestRequest(ApiModel):
    version: int = Field(ge=1)
    regions: tuple[RedactionRegion, ...]


class ExportRequest(ApiModel):
    acknowledged: bool


class DownloadResponse(ApiModel):
    download_url: str


class AuthenticationError(RuntimeError):
    """Raised when API Gateway did not supply a Cognito subject."""


def create_app(
    service: ControlPlaneService,
    *,
    allow_test_identity_header: bool = False,
) -> FastAPI:
    app = FastAPI(title="Redact All The Things Control Plane", version="0.1.0")
    app.state.service = service
    app.state.allow_test_identity_header = allow_test_identity_header

    @app.exception_handler(JobNotFoundError)
    async def handle_not_found(
        request: Request,
        error: JobNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": "job not found"})

    @app.exception_handler(ManifestConflictError)
    async def handle_manifest_conflict(
        request: Request,
        error: ManifestConflictError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": "manifest version conflict"},
        )

    @app.exception_handler(InvalidRequestError)
    async def handle_invalid_request(
        request: Request,
        error: InvalidRequestError,
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(error)})

    @app.exception_handler(AuthenticationError)
    async def handle_authentication_error(
        request: Request,
        error: AuthenticationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": "authentication required"},
        )

    def current_owner(request: Request) -> str:
        event: dict[str, Any] = request.scope.get("aws.event", {})
        claims = (
            event.get("requestContext", {})
            .get("authorizer", {})
            .get("jwt", {})
            .get("claims", {})
        )
        subject = claims.get("sub")
        if subject:
            return str(subject)
        if app.state.allow_test_identity_header:
            test_subject = request.headers.get("x-test-cognito-sub")
            if test_subject:
                return test_subject
        raise AuthenticationError("authenticated Cognito subject is required")

    @app.post("/jobs", response_model=CreateJobResponse, status_code=201)
    def create_job(
        payload: CreateJobRequest,
        owner_id: str = Depends(current_owner),
    ) -> CreateJobResponse:
        job, upload_id, upload_parts = service.create_job(
            owner_id,
            source_type=payload.source_type,
            size_bytes=payload.size_bytes,
        )
        return CreateJobResponse(
            job=job,
            upload_id=upload_id,
            upload_parts=tuple(
                UploadPartAuthorization(
                    part_number=part_number,
                    upload_url=upload_url,
                )
                for part_number, upload_url in upload_parts
            ),
        )

    @app.get("/jobs", response_model=list[Job])
    def list_jobs(owner_id: str = Depends(current_owner)) -> list[Job]:
        return service.list_jobs(owner_id)

    @app.get("/jobs/{job_id}", response_model=Job)
    def get_job(
        job_id: str,
        owner_id: str = Depends(current_owner),
    ) -> Job:
        return service.get_job(owner_id, job_id)

    @app.post("/jobs/{job_id}/upload-complete", response_model=Job)
    def complete_upload(
        job_id: str,
        payload: CompleteUploadRequest,
        owner_id: str = Depends(current_owner),
    ) -> Job:
        return service.complete_upload(
            owner_id,
            job_id,
            upload_id=payload.upload_id,
            parts=tuple(
                {"PartNumber": part.part_number, "ETag": part.etag}
                for part in payload.parts
            ),
        )

    @app.get(
        "/jobs/{job_id}/pages/{page_number}/manifest",
        response_model=PageManifest,
    )
    def get_manifest(
        job_id: str,
        page_number: int,
        owner_id: str = Depends(current_owner),
    ) -> PageManifest:
        return service.get_manifest(owner_id, job_id, page_number)

    @app.put(
        "/jobs/{job_id}/pages/{page_number}/manifest",
        response_model=PageManifest,
    )
    def save_manifest_route(
        job_id: str,
        page_number: int,
        payload: SaveManifestRequest,
        owner_id: str = Depends(current_owner),
    ) -> PageManifest:
        return service.save_manifest(
            owner_id,
            job_id,
            page_number,
            expected_version=payload.version,
            regions=payload.regions,
        )

    @app.post("/jobs/{job_id}/export", response_model=Job)
    def confirm_export(
        job_id: str,
        payload: ExportRequest,
        owner_id: str = Depends(current_owner),
    ) -> Job:
        return service.confirm_export(
            owner_id,
            job_id,
            acknowledged=payload.acknowledged,
        )

    @app.get("/jobs/{job_id}/download", response_model=DownloadResponse)
    def authorize_download(
        job_id: str,
        owner_id: str = Depends(current_owner),
    ) -> DownloadResponse:
        return DownloadResponse(
            download_url=service.authorize_download(owner_id, job_id)
        )

    @app.post("/jobs/{job_id}/retry", response_model=Job)
    def retry(
        job_id: str,
        owner_id: str = Depends(current_owner),
    ) -> Job:
        return service.retry(owner_id, job_id)

    return app
