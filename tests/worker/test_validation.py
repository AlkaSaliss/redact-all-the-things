from datetime import UTC, datetime, timedelta

import pytest

from redact_api.domain import FailureCode, Job, JobStatus, SourceType
from redact_api.worker import (
    SourceValidationError,
    ValidatedSource,
    WorkerValidationConfig,
    analyze_source,
    validate_source,
)


NOW = datetime(2026, 6, 17, 12, 0, tzinfo=UTC)


class RecordingJobs:
    def __init__(self) -> None:
        self.saved: list[tuple[Job, int]] = []

    def save(self, job: Job, *, expected_version: int) -> None:
        self.saved.append((job, expected_version))


def make_job(**overrides: object) -> Job:
    values: dict[str, object] = {
        "id": "job-123",
        "owner_id": "user-456",
        "source_type": SourceType.PDF,
        "source_key": "users/user-456/jobs/job-123/source",
        "output_key": "users/user-456/jobs/job-123/output",
        "status": JobStatus.QUEUED,
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


def pdf_bytes(page_count: int = 1, *, encrypted: bool = False) -> bytes:
    page_objects = "\n".join(
        f"{number} 0 obj << /Type /Page >> endobj"
        for number in range(1, page_count + 1)
    )
    trailer = "trailer << /Encrypt <<>> >>" if encrypted else "trailer <<>>"
    return f"%PDF-1.7\n{page_objects}\n{trailer}\n%%EOF\n".encode()


def png_bytes(width: int = 1, height: int = 1) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + (13).to_bytes(4, "big")
        + b"IHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
        + b"\x00\x00\x00\x00"
        + (0).to_bytes(4, "big")
        + b"IEND"
        + b"\x00\x00\x00\x00"
    )


def jpeg_bytes(width: int = 1, height: int = 1) -> bytes:
    return (
        b"\xff\xd8"
        + b"\xff\xe0"
        + (2).to_bytes(2, "big")
        + b"\xff\xc0"
        + (17).to_bytes(2, "big")
        + b"\x08"
        + height.to_bytes(2, "big")
        + width.to_bytes(2, "big")
        + b"\x03\x01\x11\x00\x02\x11\x00\x03\x11\x00"
        + b"\xff\xd9"
    )


def write_config(
    tmp_path,
    *,
    max_file_size_bytes: int = 1024,
    max_pdf_pages: int = 200,
    max_image_pixels: int = 50_000_000,
) -> WorkerValidationConfig:
    path = tmp_path / "worker-validation.yml"
    path.write_text(
        "\n".join(
            [
                "worker_validation:",
                f"  max_file_size_bytes: {max_file_size_bytes}",
                f"  max_pdf_pages: {max_pdf_pages}",
                f"  max_image_pixels: {max_image_pixels}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return WorkerValidationConfig.from_yaml(path)


@pytest.mark.parametrize(
    ("source_type", "source", "expected_pages"),
    [
        (SourceType.PDF, pdf_bytes(2), 2),
        (SourceType.JPEG, jpeg_bytes(), 1),
        (SourceType.PNG, png_bytes(), 1),
    ],
)
def test_validate_source_accepts_supported_content(
    source_type: SourceType,
    source: bytes,
    expected_pages: int,
) -> None:
    result = validate_source(source_type, source)

    assert result == ValidatedSource(
        source_type=source_type,
        page_count=expected_pages,
    )


@pytest.mark.parametrize(
    ("source_type", "source"),
    [
        (SourceType.PDF, png_bytes()),
        (SourceType.JPEG, png_bytes()),
        (SourceType.PNG, jpeg_bytes()),
    ],
)
def test_validate_source_rejects_signature_mismatch(
    source_type: SourceType,
    source: bytes,
) -> None:
    with pytest.raises(SourceValidationError) as error:
        validate_source(source_type, source)

    assert error.value.failure_code is FailureCode.UNSUPPORTED_CONTENT


@pytest.mark.parametrize(
    ("source_type", "source"),
    [
        (SourceType.PDF, b"%PDF-1.7\nnot a page tree"),
        (SourceType.JPEG, b"\xff\xd8broken"),
        (SourceType.PNG, b"\x89PNG\r\n\x1a\nbroken"),
    ],
)
def test_validate_source_rejects_malformed_supported_content(
    source_type: SourceType,
    source: bytes,
) -> None:
    with pytest.raises(SourceValidationError) as error:
        validate_source(source_type, source)

    assert error.value.failure_code is FailureCode.VALIDATION_FAILED


def test_validate_source_rejects_encrypted_pdf() -> None:
    with pytest.raises(SourceValidationError) as error:
        validate_source(SourceType.PDF, pdf_bytes(encrypted=True))

    assert error.value.failure_code is FailureCode.VALIDATION_FAILED


def test_validate_source_rejects_oversized_source(tmp_path) -> None:
    config = write_config(tmp_path, max_file_size_bytes=4)

    with pytest.raises(SourceValidationError) as error:
        validate_source(SourceType.PDF, pdf_bytes(), config=config)

    assert error.value.failure_code is FailureCode.VALIDATION_FAILED


def test_validate_source_rejects_over_limit_pdf_page_count(tmp_path) -> None:
    config = write_config(tmp_path, max_pdf_pages=2)

    with pytest.raises(SourceValidationError) as error:
        validate_source(SourceType.PDF, pdf_bytes(3), config=config)

    assert error.value.failure_code is FailureCode.VALIDATION_FAILED


def test_validate_source_rejects_over_limit_image_pixel_count(tmp_path) -> None:
    config = write_config(tmp_path, max_image_pixels=10)

    with pytest.raises(SourceValidationError) as error:
        validate_source(
            SourceType.PNG,
            png_bytes(width=3, height=4),
            config=config,
        )

    assert error.value.failure_code is FailureCode.VALIDATION_FAILED


def test_analyze_source_persists_safe_failure_without_artifacts() -> None:
    jobs = RecordingJobs()
    artifacts_called = False

    def write_artifacts(_: ValidatedSource) -> None:
        nonlocal artifacts_called
        artifacts_called = True

    failed = analyze_source(
        make_job(),
        b"%PDF-1.7\nnot a page tree",
        jobs=jobs,
        now=NOW,
        write_artifacts=write_artifacts,
    )

    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is FailureCode.VALIDATION_FAILED
    assert failed.model_dump(mode="json")["failure_code"] == "validation_failed"
    assert jobs.saved == [(failed, 1)]
    assert not artifacts_called
