import io
import json
from datetime import UTC, datetime, timedelta

from PIL import Image

from redact_api.domain import FailureCode, Job, JobStatus, SourceType
from redact_api.worker import (
    OcrExtractionError,
    OcrLine,
    PageArtifact,
    PageArtifactIndex,
    ValidatedSource,
    analyze_source,
    extract_ocr_text,
)


NOW = datetime(2026, 6, 17, 12, 0, tzinfo=UTC)


class RecordingJobs:
    def __init__(self) -> None:
        self.saved: list[tuple[Job, int]] = []

    def save(self, job: Job, *, expected_version: int) -> None:
        self.saved.append((job, expected_version))


class RecordingRasterWriter:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    def put_page_artifact(self, key: str, content: bytes) -> None:
        self.objects[key] = content

    def put_page_artifact_index(self, key: str, content: bytes) -> None:
        self.objects[key] = content


class RecordingOcrStore:
    def __init__(self, pages: dict[str, bytes]) -> None:
        self.pages = pages
        self.events: list[tuple[str, str]] = []
        self.objects: dict[str, bytes] = {}

    def get_page_artifact(self, key: str) -> bytes:
        self.events.append(("get", key))
        return self.pages[key]

    def put_ocr_page_text(self, key: str, content: bytes) -> None:
        self.events.append(("put", key))
        self.objects[key] = content


class RecordingOcrEngine:
    name = "test-ocr"
    model = "test-model"

    def __init__(self) -> None:
        self.pages: list[tuple[int, bytes]] = []

    def recognize(self, page: PageArtifact, content: bytes) -> tuple[OcrLine, ...]:
        self.pages.append((page.page_number, content))
        return (
            OcrLine(
                text=f"Page {page.page_number}",
                confidence=0.9,
                polygon=((10, 10), (60, 10), (60, 20), (10, 20)),
            ),
        )


class FailingOcrEngine(RecordingOcrEngine):
    def recognize(self, page: PageArtifact, content: bytes) -> tuple[OcrLine, ...]:
        raise OcrExtractionError("ocr failed")


def make_job(**overrides: object) -> Job:
    values: dict[str, object] = {
        "id": "job-123",
        "owner_id": "user-456",
        "source_type": SourceType.PNG,
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


def page_index() -> PageArtifactIndex:
    return PageArtifactIndex(
        job_id="job-123",
        key="users/user-456/jobs/job-123/artifacts/pages/index.json",
        pages=(
            PageArtifact(
                page_number=1,
                width=100,
                height=50,
                format="png",
                key="users/user-456/jobs/job-123/artifacts/pages/1.png",
            ),
            PageArtifact(
                page_number=2,
                width=200,
                height=100,
                format="png",
                key="users/user-456/jobs/job-123/artifacts/pages/2.png",
            ),
        ),
    )


def png_bytes() -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (1, 1), color=(255, 255, 255)).save(output, format="PNG")
    return output.getvalue()


def test_extract_ocr_runs_for_each_page_in_order() -> None:
    index = page_index()
    store = RecordingOcrStore(
        {page.key: f"page-{page.page_number}".encode() for page in index.pages}
    )
    engine = RecordingOcrEngine()

    pages = extract_ocr_text(make_job(), index, store=store, engine=engine)

    assert [page.page_number for page in pages] == [1, 2]
    assert engine.pages == [(1, b"page-1"), (2, b"page-2")]
    assert [event[0] for event in store.events] == ["get", "put", "get", "put"]


def test_extract_ocr_writes_page_text_json_with_normalized_polygons() -> None:
    index = page_index()
    store = RecordingOcrStore({page.key: b"page" for page in index.pages})

    extract_ocr_text(make_job(), index, store=store, engine=RecordingOcrEngine())

    key = "users/user-456/jobs/job-123/artifacts/ocr/pages/1.json"
    payload = json.loads(store.objects[key])
    assert payload == {
        "job_id": "job-123",
        "page_number": 1,
        "page_width": 100,
        "page_height": 50,
        "engine": "test-ocr",
        "model": "test-model",
        "page_text": "Page 1",
        "blocks": [
            {
                "text": "Page 1",
                "confidence": 0.9,
                "polygon": [[0.1, 0.2], [0.6, 0.2], [0.6, 0.4], [0.1, 0.4]],
                "start": 0,
                "end": 6,
            }
        ],
    }


def test_extract_ocr_offsets_follow_ordered_page_text() -> None:
    class MultiLineEngine(RecordingOcrEngine):
        def recognize(self, page: PageArtifact, content: bytes) -> tuple[OcrLine, ...]:
            return (
                OcrLine("Jane Public", 0.98, ((0, 0), (10, 0), (10, 10), (0, 10))),
                OcrLine("DOB 2000-01-01", 0.97, ((0, 10), (20, 10), (20, 20), (0, 20))),
            )

    page = page_index().pages[0]
    index = PageArtifactIndex(job_id="job-123", key="index", pages=(page,))
    store = RecordingOcrStore({page.key: b"page"})

    extract_ocr_text(make_job(), index, store=store, engine=MultiLineEngine())

    payload = json.loads(store.objects["users/user-456/jobs/job-123/artifacts/ocr/pages/1.json"])
    assert payload["page_text"] == "Jane Public\nDOB 2000-01-01"
    assert [(block["start"], block["end"]) for block in payload["blocks"]] == [
        (0, 11),
        (12, 26),
    ]


def test_analyze_source_persists_processing_failed_on_ocr_error() -> None:
    jobs = RecordingJobs()
    raster_writer = RecordingRasterWriter()
    ocr_store = RecordingOcrStore(
        {"users/user-456/jobs/job-123/artifacts/pages/1.png": b"page"}
    )
    downstream_called = False

    def render_pages():
        from redact_api.worker import RenderedPage

        yield RenderedPage(1, 1, 1, b"\x89PNG\r\n\x1a\npage")

    def write_downstream(_: ValidatedSource) -> None:
        nonlocal downstream_called
        downstream_called = True

    failed = analyze_source(
        make_job(),
        png_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=raster_writer,
        ocr_store=ocr_store,
        ocr_engine=FailingOcrEngine(),
        render_pages=render_pages,
        write_artifacts=write_downstream,
    )

    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is FailureCode.PROCESSING_FAILED
    assert jobs.saved == [(failed, 1)]
    assert not downstream_called
    assert not ocr_store.objects


def test_analyze_source_runs_ocr_before_downstream_hook() -> None:
    jobs = RecordingJobs()
    raster_writer = RecordingRasterWriter()
    ocr_store = RecordingOcrStore(
        {"users/user-456/jobs/job-123/artifacts/pages/1.png": b"page"}
    )
    engine = RecordingOcrEngine()
    downstream_called = False

    def render_pages():
        from redact_api.worker import RenderedPage

        yield RenderedPage(1, 100, 50, b"\x89PNG\r\n\x1a\npage")

    def write_downstream(_: ValidatedSource) -> None:
        nonlocal downstream_called
        assert ocr_store.objects
        downstream_called = True

    job = analyze_source(
        make_job(),
        png_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=raster_writer,
        ocr_store=ocr_store,
        ocr_engine=engine,
        render_pages=render_pages,
        write_artifacts=write_downstream,
    )

    assert job.status is JobStatus.QUEUED
    assert jobs.saved == []
    assert engine.pages == [(1, b"page")]
    assert downstream_called
