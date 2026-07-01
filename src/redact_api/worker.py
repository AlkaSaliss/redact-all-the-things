"""Analysis worker validation and rasterization boundaries."""

from __future__ import annotations

import io
import json
import tempfile
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

import pypdfium2 as pdfium
import yaml
from PIL import Image, UnidentifiedImageError

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
class RenderedPage:
    """PNG bytes for one rendered source page."""

    page_number: int
    width: int
    height: int
    png: bytes


@dataclass(frozen=True)
class PageArtifact:
    """Metadata for one persisted raster page artifact."""

    page_number: int
    width: int
    height: int
    format: str
    key: str


@dataclass(frozen=True)
class PageArtifactIndex:
    """Ordered metadata for page artifacts produced by rasterization."""

    job_id: str
    pages: tuple[PageArtifact, ...]
    key: str


@dataclass(frozen=True)
class OcrLine:
    """One raw OCR line using pixel-space page coordinates."""

    text: str
    confidence: float
    polygon: tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class OcrTextBlock:
    """One normalized OCR text block in page text order."""

    text: str
    confidence: float
    polygon: tuple[tuple[float, float], ...]
    start: int
    end: int


@dataclass(frozen=True)
class OcrPageText:
    """OCR text and line geometry for one rasterized page."""

    job_id: str
    page_number: int
    page_width: int
    page_height: int
    engine: str
    model: str
    page_text: str
    blocks: tuple[OcrTextBlock, ...]


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


@dataclass(frozen=True)
class WorkerRasterizationConfig:
    """Tunable rasterization settings."""

    dpi: int = 150

    @property
    def scale(self) -> float:
        return self.dpi / 72


class PageArtifactWriter(Protocol):
    """Persistence boundary for raster page artifacts."""

    def put_page_artifact(self, key: str, content: bytes) -> None:
        """Persist one PNG page artifact."""

    def put_page_artifact_index(self, key: str, content: bytes) -> None:
        """Persist the JSON page-artifact index."""


class OcrArtifactStore(Protocol):
    """Persistence boundary for OCR input pages and output text artifacts."""

    def get_page_artifact(self, key: str) -> bytes:
        """Load one raster page artifact."""

    def put_ocr_page_text(self, key: str, content: bytes) -> None:
        """Persist one per-page OCR JSON artifact."""


class OcrEngine(Protocol):
    """OCR engine boundary used by production and deterministic tests."""

    name: str
    model: str

    def recognize(self, page: PageArtifact, content: bytes) -> Iterable[OcrLine]:
        """Return OCR lines for one raster page artifact."""


class SourceValidationError(ValueError):
    """Raised when source validation maps to a safe failure code."""

    def __init__(self, failure_code: FailureCode) -> None:
        super().__init__(failure_code.value)
        self.failure_code = failure_code


class RasterizationError(RuntimeError):
    """Raised when accepted source content cannot be rasterized safely."""


class OcrExtractionError(RuntimeError):
    """Raised when accepted page artifacts cannot be OCR-processed safely."""


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
    raster_writer: PageArtifactWriter | None = None,
    ocr_store: OcrArtifactStore | None = None,
    ocr_engine: OcrEngine | None = None,
    render_pages: Callable[[], Iterable[RenderedPage]] | None = None,
    write_artifacts: Callable[[ValidatedSource], None] | None = None,
) -> Job:
    """Validate and optionally rasterize/OCR an analyze request."""

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
    page_index = None
    if raster_writer is not None:
        try:
            page_index = rasterize_source(
                job,
                source,
                validated,
                writer=raster_writer,
                render_pages=render_pages,
            )
        except RasterizationError:
            failed = transition_job(
                job,
                JobStatus.FAILED,
                now=now,
                failure_code=FailureCode.PROCESSING_FAILED,
            )
            jobs.save(failed, expected_version=job.version)
            return failed
    if page_index is not None and ocr_store is not None and ocr_engine is not None:
        try:
            extract_ocr_text(job, page_index, store=ocr_store, engine=ocr_engine)
        except OcrExtractionError:
            failed = transition_job(
                job,
                JobStatus.FAILED,
                now=now,
                failure_code=FailureCode.PROCESSING_FAILED,
            )
            jobs.save(failed, expected_version=job.version)
            return failed
    if write_artifacts is not None:
        write_artifacts(validated)
    return job


def rasterize_source(
    job: Job,
    source: bytes,
    validated: ValidatedSource,
    *,
    writer: PageArtifactWriter,
    config: WorkerRasterizationConfig | None = None,
    render_pages: Callable[[], Iterable[RenderedPage]] | None = None,
) -> PageArtifactIndex:
    """Rasterize a validated source into PNG page artifacts and an index."""

    pages = []
    index_key = page_artifact_index_key(job.owner_id, job.id)
    try:
        rendered_pages = (
            render_pages()
            if render_pages is not None
            else _render_source_pages(
                source,
                validated,
                config or WorkerRasterizationConfig(),
            )
        )
        for rendered in rendered_pages:
            if (
                rendered.page_number != len(pages) + 1
                or rendered.width <= 0
                or rendered.height <= 0
            ):
                raise RasterizationError("invalid rendered page metadata")
            key = page_artifact_key(job.owner_id, job.id, rendered.page_number)
            writer.put_page_artifact(key, rendered.png)
            pages.append(
                PageArtifact(
                    page_number=rendered.page_number,
                    width=rendered.width,
                    height=rendered.height,
                    format="png",
                    key=key,
                )
            )
        if len(pages) != validated.page_count:
            raise RasterizationError("rendered page count mismatch")
        index = PageArtifactIndex(
            job_id=job.id,
            pages=tuple(pages),
            key=index_key,
        )
        writer.put_page_artifact_index(
            index_key,
            _serialize_page_artifact_index(index),
        )
        return index
    except RasterizationError:
        raise
    except Exception as error:
        raise RasterizationError("source rasterization failed") from error


def page_artifact_key(owner_id: str, job_id: str, page_number: int) -> str:
    """Return the owner/job-namespaced key for a raster page PNG."""

    return f"users/{owner_id}/jobs/{job_id}/artifacts/pages/{page_number}.png"


def page_artifact_index_key(owner_id: str, job_id: str) -> str:
    """Return the owner/job-namespaced key for the raster page index."""

    return f"users/{owner_id}/jobs/{job_id}/artifacts/pages/index.json"


def extract_ocr_text(
    job: Job,
    page_index: PageArtifactIndex,
    *,
    store: OcrArtifactStore,
    engine: OcrEngine,
) -> tuple[OcrPageText, ...]:
    """Extract and persist OCR text for every raster page in an index."""

    pages = []
    try:
        for page in page_index.pages:
            content = store.get_page_artifact(page.key)
            lines = tuple(engine.recognize(page, content))
            page_text = _build_ocr_page_text(job, page, lines, engine=engine)
            key = ocr_page_text_key(job.owner_id, job.id, page.page_number)
            store.put_ocr_page_text(key, _serialize_ocr_page_text(page_text))
            pages.append(page_text)
        return tuple(pages)
    except OcrExtractionError:
        raise
    except Exception as error:
        raise OcrExtractionError("ocr extraction failed") from error


def ocr_page_text_key(owner_id: str, job_id: str, page_number: int) -> str:
    """Return the owner/job-namespaced key for one OCR page JSON artifact."""

    return f"users/{owner_id}/jobs/{job_id}/artifacts/ocr/pages/{page_number}.json"


class PaddleOcrEngine:
    """Embedded PaddleOCR adapter for the worker image runtime."""

    name = "paddleocr"
    model = "PP-OCRv6_medium"

    def __init__(self, *, device: str = "cpu") -> None:
        try:
            from paddleocr import PaddleOCR
        except ImportError as error:
            raise OcrExtractionError("paddleocr is not installed") from error
        self._pipeline = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=True,
            device=device,
        )

    def recognize(self, page: PageArtifact, content: bytes) -> tuple[OcrLine, ...]:
        try:
            with tempfile.NamedTemporaryFile(suffix=".png") as image:
                image.write(content)
                image.flush()
                results = self._pipeline.predict(image.name)
            lines: list[OcrLine] = []
            for result in results:
                payload = result.json.get("res", result.json)
                texts = payload.get("rec_texts", ())
                scores = payload.get("rec_scores", ())
                polygons = payload.get("rec_polys", ())
                for text, score, polygon in zip(texts, scores, polygons, strict=True):
                    lines.append(
                        OcrLine(
                            text=str(text),
                            confidence=float(score),
                            polygon=tuple(
                                (float(point[0]), float(point[1]))
                                for point in polygon
                            ),
                        )
                    )
            return tuple(lines)
        except OcrExtractionError:
            raise
        except Exception as error:
            raise OcrExtractionError("paddleocr recognition failed") from error


def _render_source_pages(
    source: bytes,
    validated: ValidatedSource,
    config: WorkerRasterizationConfig,
) -> Iterable[RenderedPage]:
    if validated.source_type is SourceType.PDF:
        return _render_pdf_pages(source, config=config)
    if validated.source_type in {SourceType.JPEG, SourceType.PNG}:
        return (_render_image_page(source),)
    raise RasterizationError("unsupported source type")


def _render_pdf_pages(
    source: bytes,
    *,
    config: WorkerRasterizationConfig,
) -> Iterable[RenderedPage]:
    document = pdfium.PdfDocument(source)
    try:
        for index in range(len(document)):
            page = document[index]
            try:
                image = page.render(scale=config.scale).to_pil()
                yield _image_to_rendered_page(index + 1, image)
            finally:
                page.close()
    finally:
        document.close()


def _render_image_page(source: bytes) -> RenderedPage:
    try:
        with Image.open(io.BytesIO(source)) as image:
            return _image_to_rendered_page(1, image)
    except UnidentifiedImageError as error:
        raise RasterizationError("image rasterization failed") from error


def _image_to_rendered_page(page_number: int, image: Image.Image) -> RenderedPage:
    output = io.BytesIO()
    normalized = image.convert("RGB")
    normalized.save(output, format="PNG")
    return RenderedPage(
        page_number=page_number,
        width=normalized.width,
        height=normalized.height,
        png=output.getvalue(),
    )


def _serialize_page_artifact_index(index: PageArtifactIndex) -> bytes:
    payload = {
        "job_id": index.job_id,
        "pages": [
            {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "format": page.format,
                "key": page.key,
            }
            for page in index.pages
        ],
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()


def _build_ocr_page_text(
    job: Job,
    page: PageArtifact,
    lines: tuple[OcrLine, ...],
    *,
    engine: OcrEngine,
) -> OcrPageText:
    blocks = []
    text_parts = []
    offset = 0
    for line in lines:
        end = offset + len(line.text)
        blocks.append(
            OcrTextBlock(
                text=line.text,
                confidence=line.confidence,
                polygon=_normalize_polygon(line.polygon, page),
                start=offset,
                end=end,
            )
        )
        text_parts.append(line.text)
        offset = end + 1
    return OcrPageText(
        job_id=job.id,
        page_number=page.page_number,
        page_width=page.width,
        page_height=page.height,
        engine=engine.name,
        model=engine.model,
        page_text="\n".join(text_parts),
        blocks=tuple(blocks),
    )


def _normalize_polygon(
    polygon: tuple[tuple[float, float], ...],
    page: PageArtifact,
) -> tuple[tuple[float, float], ...]:
    if len(polygon) != 4:
        raise OcrExtractionError("ocr line polygon must contain four points")
    if page.width <= 0 or page.height <= 0:
        raise OcrExtractionError("page dimensions must be positive")
    normalized = tuple((x / page.width, y / page.height) for x, y in polygon)
    if any(x < 0 or x > 1 or y < 0 or y > 1 for x, y in normalized):
        raise OcrExtractionError("ocr line polygon is outside page bounds")
    return normalized


def _serialize_ocr_page_text(page_text: OcrPageText) -> bytes:
    payload = {
        "job_id": page_text.job_id,
        "page_number": page_text.page_number,
        "page_width": page_text.page_width,
        "page_height": page_text.page_height,
        "engine": page_text.engine,
        "model": page_text.model,
        "page_text": page_text.page_text,
        "blocks": [
            {
                "text": block.text,
                "confidence": block.confidence,
                "polygon": [[x, y] for x, y in block.polygon],
                "start": block.start,
                "end": block.end,
            }
            for block in page_text.blocks
        ],
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()


def _validate_pdf(source: bytes, *, max_pdf_pages: int) -> int:
    if not source.startswith(PDF_SIGNATURE):
        raise SourceValidationError(FailureCode.UNSUPPORTED_CONTENT)
    if b"/Encrypt" in source:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED)
    try:
        document = pdfium.PdfDocument(source)
        try:
            page_count = len(document)
        finally:
            document.close()
    except Exception as error:
        raise SourceValidationError(FailureCode.VALIDATION_FAILED) from error
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
