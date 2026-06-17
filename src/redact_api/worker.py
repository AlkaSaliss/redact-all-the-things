"""Validation-only analysis worker boundary."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from redact_api.domain import (
    FailureCode,
    Job,
    JobStatus,
    SourceType,
    transition_job,
)
from redact_api.services import MAX_FILE_SIZE


MAX_PDF_PAGES = 200
MAX_IMAGE_PIXELS = 50_000_000
DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[2] / "config" / "worker-validation.yml"
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8"
PDF_SIGNATURE = b"%PDF-"
JPEG_SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


@dataclass(frozen=True)
class ValidatedSource:
    """Source metadata safe for later analysis stages."""

    source_type: SourceType
    page_count: int


@dataclass(frozen=True)
class WorkerValidationConfig:
    """Tunable validation limits loaded from YAML."""

    max_file_size_bytes: int = MAX_FILE_SIZE
    max_pdf_pages: int = MAX_PDF_PAGES
    max_image_pixels: int = MAX_IMAGE_PIXELS

    @classmethod
    def from_yaml(cls, path: str | Path) -> WorkerValidationConfig:
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        values = raw.get("worker_validation", {})
        if not isinstance(values, dict):
            raise ValueError("worker_validation must be a mapping")
        config = cls(
            max_file_size_bytes=int(
                values.get("max_file_size_bytes", cls.max_file_size_bytes)
            ),
            max_pdf_pages=int(values.get("max_pdf_pages", cls.max_pdf_pages)),
            max_image_pixels=int(
                values.get("max_image_pixels", cls.max_image_pixels)
            ),
        )
        if (
            config.max_file_size_bytes <= 0
            or config.max_pdf_pages <= 0
            or config.max_image_pixels <= 0
        ):
            raise ValueError("worker validation limits must be positive")
        return config


class SourceValidationError(ValueError):
    """Raised when source validation maps to a safe failure code."""

    def __init__(self, failure_code: FailureCode) -> None:
        super().__init__(failure_code.value)
        self.failure_code = failure_code


def validate_source(
    source_type: SourceType,
    source: bytes,
    *,
    config: WorkerValidationConfig | None = None,
) -> ValidatedSource:
    """Validate source bytes before any analysis artifact can be created."""

    limits = config or WorkerValidationConfig.from_yaml(DEFAULT_CONFIG_PATH)
    if not source or len(source) > limits.max_file_size_bytes:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)
    if source_type is SourceType.PDF:
        return ValidatedSource(
            source_type,
            _validate_pdf(source, max_pdf_pages=limits.max_pdf_pages),
        )
    if source_type is SourceType.JPEG:
        _validate_jpeg(source, max_image_pixels=limits.max_image_pixels)
        return ValidatedSource(source_type, 1)
    if source_type is SourceType.PNG:
        _validate_png(source, max_image_pixels=limits.max_image_pixels)
        return ValidatedSource(source_type, 1)
    raise SourceValidationError(FailureCode.UNSUPPORTED_CONTENT)


def analyze_source(
    job: Job,
    source: bytes,
    *,
    jobs: Any,
    now: datetime,
    config: WorkerValidationConfig | None = None,
    write_artifacts: Callable[[ValidatedSource], None] | None = None,
) -> Job:
    """Validate an analyze request and persist safe failure state on rejection."""

    try:
        validated = validate_source(job.source_type, source, config=config)
    except SourceValidationError as error:
        failed = transition_job(
            job,
            JobStatus.FAILED,
            now=now,
            failure_code=error.failure_code,
        )
        jobs.save(failed, expected_version=job.version)
        return failed
    if write_artifacts is not None:
        write_artifacts(validated)
    return job


def _validate_pdf(source: bytes, *, max_pdf_pages: int) -> int:
    if not source.startswith(PDF_SIGNATURE):
        raise SourceValidationError(FailureCode.UNSUPPORTED_CONTENT)
    if b"/Encrypt" in source:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)
    page_count = len(re.findall(rb"/Type\s*/Page(?!s)\b", source))
    if page_count < 1 or page_count > max_pdf_pages:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)
    if b"%%EOF" not in source:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)
    return page_count


def _validate_png(source: bytes, *, max_image_pixels: int) -> None:
    if not source.startswith(PNG_SIGNATURE):
        raise SourceValidationError(FailureCode.UNSUPPORTED_CONTENT)
    try:
        length = int.from_bytes(source[8:12], "big")
        chunk_type = source[12:16]
        data = source[16 : 16 + length]
        width = int.from_bytes(data[0:4], "big")
        height = int.from_bytes(data[4:8], "big")
    except (IndexError, ValueError) as error:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED) from error
    if length != 13 or chunk_type != b"IHDR" or len(data) != 13:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)
    if width <= 0 or height <= 0 or width * height > max_image_pixels:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)


def _validate_jpeg(source: bytes, *, max_image_pixels: int) -> None:
    if not source.startswith(JPEG_SIGNATURE):
        raise SourceValidationError(FailureCode.UNSUPPORTED_CONTENT)
    index = 2
    try:
        while index < len(source):
            if source[index] != 0xFF:
                raise SourceValidationError(FailureCode.VALIDATION_FAILED)
            while index < len(source) and source[index] == 0xFF:
                index += 1
            marker = source[index]
            index += 1
            if marker == 0xD9:
                break
            if marker == 0xDA:
                raise SourceValidationError(FailureCode.VALIDATION_FAILED)
            segment_length = int.from_bytes(source[index : index + 2], "big")
            if segment_length < 2:
                raise SourceValidationError(FailureCode.VALIDATION_FAILED)
            segment = source[index + 2 : index + segment_length]
            if len(segment) != segment_length - 2:
                raise SourceValidationError(FailureCode.VALIDATION_FAILED)
            if marker in JPEG_SOF_MARKERS:
                if len(segment) < 5:
                    raise SourceValidationError(FailureCode.VALIDATION_FAILED)
                height = int.from_bytes(segment[1:3], "big")
                width = int.from_bytes(segment[3:5], "big")
                if width <= 0 or height <= 0 or width * height > max_image_pixels:
                    raise SourceValidationError(FailureCode.VALIDATION_FAILED)
                return
            index += segment_length
    except IndexError as error:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED) from error
    raise SourceValidationError(FailureCode.VALIDATION_FAILED)
