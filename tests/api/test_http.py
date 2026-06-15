from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from redact_api.domain import (
    FailureCode,
    JobStatus,
    PageManifest,
    RedactionRegion,
    RegionSource,
)
from redact_api.http import create_app
from redact_api.services import ControlPlaneService


pytestmark = pytest.mark.localstack
NOW = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)
HEADERS = {"x-test-cognito-sub": "user-456"}


@pytest.fixture
def client(aws_resources: dict[str, object]) -> TestClient:
    service = ControlPlaneService(
        aws_resources["jobs"],
        aws_resources["objects"],
        aws_resources["batch"],
        clock=lambda: NOW,
        id_factory=lambda: "job-123",
    )
    return TestClient(create_app(service, allow_test_identity_header=True))


def create_job(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/jobs",
        headers=HEADERS,
        json={"source_type": "pdf", "size_bytes": 1024},
    )
    assert response.status_code == 201
    return response.json()


def set_status(
    aws_resources: dict[str, object],
    status: JobStatus,
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


def create_manifest(aws_resources: dict[str, object]) -> PageManifest:
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


def test_identity_validation_and_request_validation(client: TestClient) -> None:
    assert client.get("/jobs").status_code == 401
    invalid = client.post(
        "/jobs",
        headers=HEADERS,
        json={"source_type": "docx", "size_bytes": 0},
    )
    assert invalid.status_code == 422


def test_create_list_retrieve_and_non_disclosing_not_found(
    client: TestClient,
) -> None:
    created = create_job(client)

    listed = client.get("/jobs", headers=HEADERS)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == created["job"]["id"]
    assert client.get("/jobs/job-123", headers=HEADERS).status_code == 200
    foreign = client.get(
        "/jobs/job-123",
        headers={"x-test-cognito-sub": "other-user"},
    )
    assert foreign.status_code == 404
    assert foreign.json() == {"detail": "job not found"}


def test_upload_complete_export_retry_manifest_and_download_routes(
    client: TestClient,
    aws_resources: dict[str, object],
) -> None:
    created = create_job(client)
    part = aws_resources["s3"].upload_part(
        Bucket="redact-files",
        Key="users/user-456/jobs/job-123/source",
        UploadId=created["upload_id"],
        PartNumber=1,
        Body=b"document",
    )
    queued = client.post(
        "/jobs/job-123/upload-complete",
        headers=HEADERS,
        json={
            "upload_id": created["upload_id"],
            "parts": [{"part_number": 1, "etag": part["ETag"]}],
        },
    )
    assert queued.status_code == 200
    assert queued.json()["status"] == "queued"

    set_status(aws_resources, JobStatus.READY)
    create_manifest(aws_resources)
    manifest = client.get(
        "/jobs/job-123/pages/1/manifest",
        headers=HEADERS,
    )
    assert manifest.status_code == 200
    manual = {
        "id": "manual-1",
        "page_number": 1,
        "x": 0.4,
        "y": 0.4,
        "width": 0.2,
        "height": 0.2,
        "source": "manual",
        "category": "MANUAL",
        "confidence": None,
        "selected": True,
    }
    saved = client.put(
        "/jobs/job-123/pages/1/manifest",
        headers=HEADERS,
        json={"version": 1, "regions": [manual]},
    )
    assert saved.status_code == 200
    assert saved.json()["version"] == 2
    stale = client.put(
        "/jobs/job-123/pages/1/manifest",
        headers=HEADERS,
        json={"version": 1, "regions": [manual]},
    )
    assert stale.status_code == 409

    rejected_export = client.post(
        "/jobs/job-123/export",
        headers=HEADERS,
        json={"acknowledged": False},
    )
    assert rejected_export.status_code == 409
    exporting = client.post(
        "/jobs/job-123/export",
        headers=HEADERS,
        json={"acknowledged": True},
    )
    assert exporting.status_code == 200
    assert exporting.json()["status"] == "exporting"

    set_status(
        aws_resources,
        JobStatus.FAILED,
        FailureCode.RENDER_TRANSIENT,
    )
    retried = client.post("/jobs/job-123/retry", headers=HEADERS)
    assert retried.status_code == 200
    assert retried.json()["status"] == "exporting"

    set_status(aws_resources, JobStatus.COMPLETE)
    aws_resources["s3"].put_object(
        Bucket="redact-files",
        Key="users/user-456/jobs/job-123/output",
        Body=b"redacted",
    )
    download = client.get("/jobs/job-123/download", headers=HEADERS)
    assert download.status_code == 200
    assert "job-123/output" in download.json()["download_url"]


def test_openapi_contains_the_public_contract(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    expected_paths = {
        "/jobs",
        "/jobs/{job_id}",
        "/jobs/{job_id}/upload-complete",
        "/jobs/{job_id}/pages/{page_number}/manifest",
        "/jobs/{job_id}/export",
        "/jobs/{job_id}/download",
        "/jobs/{job_id}/retry",
    }

    assert expected_paths <= set(schema["paths"])
    assert "CreateJobRequest" in schema["components"]["schemas"]
    assert "PageManifest" in schema["components"]["schemas"]
