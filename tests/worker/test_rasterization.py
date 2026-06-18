import io
import json
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta

import pypdfium2 as pdfium
import pytest
from PIL import Image

from redact_api.domain import FailureCode, Job, JobStatus, SourceType
from redact_api.worker import (
    PageArtifactIndex,
    RasterizationError,
    RenderedPage,
    ValidatedSource,
    WorkerRasterizationConfig,
    analyze_source,
    rasterize_source,
    validate_source,
)


NOW = datetime(2026, 6, 17, 12, 0, tzinfo=UTC)


class RecordingJobs:
    def __init__(self) -> None:
        self.saved: list[tuple[Job, int]] = []

    def save(self, job: Job, *, expected_version: int) -> None:
        self.saved.append((job, expected_version))


class RecordingArtifactWriter:
    def __init__(self) -> None:
        self.events: list[tuple[str, str]] = []
        self.objects: dict[str, bytes] = {}

    def put_page_artifact(self, key: str, content: bytes) -> None:
        self.events.append(("page", key))
        self.objects[key] = content

    def put_page_artifact_index(self, key: str, content: bytes) -> None:
        self.events.append(("index", key))
        self.objects[key] = content


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


def pdf_bytes(page_sizes: tuple[tuple[int, int], ...] = ((72, 72), (144, 72))) -> bytes:
    document = pdfium.PdfDocument.new()
    for width, height in page_sizes:
        document.new_page(width, height)
    output = io.BytesIO()
    document.save(output)
    document.close()
    return output.getvalue()


def image_bytes(
    source_type: SourceType,
    *,
    width: int = 3,
    height: int = 2,
) -> bytes:
    output = io.BytesIO()
    image = Image.new("RGB", (width, height), color=(12, 34, 56))
    image.save(output, format="JPEG" if source_type is SourceType.JPEG else "PNG")
    return output.getvalue()


def assert_png(content: bytes) -> None:
    assert content.startswith(b"\x89PNG\r\n\x1a\n")


def test_rasterize_pdf_pages_in_source_order() -> None:
    source = pdf_bytes()
    job = make_job()
    writer = RecordingArtifactWriter()

    index = rasterize_source(
        job,
        source,
        validate_source(SourceType.PDF, source),
        writer=writer,
        config=WorkerRasterizationConfig(dpi=72),
    )

    assert [page.page_number for page in index.pages] == [1, 2]
    assert [page.width for page in index.pages] == [72, 144]
    assert [page.height for page in index.pages] == [72, 72]
    assert [event[0] for event in writer.events] == ["page", "page", "index"]
    for page in index.pages:
        assert page.format == "png"
        assert page.key == (
            f"users/user-456/jobs/job-123/artifacts/pages/{page.page_number}.png"
        )
        assert_png(writer.objects[page.key])


@pytest.mark.parametrize("source_type", [SourceType.JPEG, SourceType.PNG])
def test_rasterize_image_source_as_one_png_page(source_type: SourceType) -> None:
    source = image_bytes(source_type)
    job = make_job(source_type=source_type)
    writer = RecordingArtifactWriter()

    index = rasterize_source(
        job,
        source,
        validate_source(source_type, source),
        writer=writer,
    )

    assert len(index.pages) == 1
    page = index.pages[0]
    assert page.page_number == 1
    assert page.width == 3
    assert page.height == 2
    assert page.format == "png"
    assert_png(writer.objects[page.key])


def test_page_artifact_index_records_ordered_metadata() -> None:
    source = image_bytes(SourceType.PNG)
    job = make_job(source_type=SourceType.PNG)
    writer = RecordingArtifactWriter()

    index = rasterize_source(
        job,
        source,
        validate_source(SourceType.PNG, source),
        writer=writer,
    )

    assert isinstance(index, PageArtifactIndex)
    assert index.key == "users/user-456/jobs/job-123/artifacts/pages/index.json"
    payload = json.loads(writer.objects[index.key])
    assert payload == {
        "job_id": "job-123",
        "pages": [
            {
                "page_number": 1,
                "width": 3,
                "height": 2,
                "format": "png",
                "key": "users/user-456/jobs/job-123/artifacts/pages/1.png",
            }
        ],
    }


def test_rasterization_writes_each_page_before_rendering_next() -> None:
    writer = RecordingArtifactWriter()
    render_events: list[str] = []

    def render_pages() -> Iterable[RenderedPage]:
        render_events.append("render-1")
        yield RenderedPage(1, 1, 1, b"\x89PNG\r\n\x1a\npage-1")
        assert writer.events == [
            ("page", "users/user-456/jobs/job-123/artifacts/pages/1.png")
        ]
        render_events.append("render-2")
        yield RenderedPage(2, 1, 1, b"\x89PNG\r\n\x1a\npage-2")

    rasterize_source(
        make_job(),
        b"%PDF-1.7\n%%EOF\n",
        ValidatedSource(SourceType.PDF, 2),
        writer=writer,
        render_pages=render_pages,
    )

    assert render_events == ["render-1", "render-2"]
    assert [event[0] for event in writer.events] == ["page", "page", "index"]


def test_analyze_source_persists_processing_failed_on_rasterization_error() -> None:
    jobs = RecordingJobs()
    downstream_called = False

    class FailingWriter(RecordingArtifactWriter):
        def put_page_artifact(self, key: str, content: bytes) -> None:
            super().put_page_artifact(key, content)
            raise RasterizationError("write failed")

    def write_downstream(_: ValidatedSource) -> None:
        nonlocal downstream_called
        downstream_called = True

    failed = analyze_source(
        make_job(source_type=SourceType.PNG),
        image_bytes(SourceType.PNG),
        jobs=jobs,
        now=NOW,
        raster_writer=FailingWriter(),
        write_artifacts=write_downstream,
    )

    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is FailureCode.PROCESSING_FAILED
    assert jobs.saved == [(failed, 1)]
    assert not downstream_called
