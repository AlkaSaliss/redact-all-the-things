import io
from datetime import UTC, datetime, timedelta

import pytest
from PIL import Image

from redact_api.domain import (
    FailureCode,
    Job,
    JobStatus,
    PageManifest,
    RegionSource,
    SourceType,
)
from redact_api.worker import (
    OcrLine,
    OcrPageText,
    OcrTextBlock,
    PageArtifact,
    PiiEntity,
    PiiMappingError,
    RenderedPage,
    ValidatedSource,
    analyze_source,
    create_pii_manifests,
    map_pii_regions,
)


NOW = datetime(2026, 6, 19, 12, 0, tzinfo=UTC)


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
        self.ocr_objects: dict[str, bytes] = {}

    def get_page_artifact(self, key: str) -> bytes:
        return self.pages[key]

    def put_ocr_page_text(self, key: str, content: bytes) -> None:
        self.ocr_objects[key] = content


class RecordingOcrEngine:
    name = "test-ocr"
    model = "test-model"

    def recognize(self, page: PageArtifact, content: bytes) -> tuple[OcrLine, ...]:
        return (
            OcrLine(
                "Email ada@example.com phone +1 415 555 0199",
                0.99,
                ((0, 0), (200, 0), (200, 20), (0, 20)),
            ),
            OcrLine(
                "Passport A12345678 API key sk-test-secret",
                0.98,
                ((0, 20), (200, 20), (200, 40), (0, 40)),
            ),
            OcrLine(
                "Ada Lovelace lives at 123 Main St",
                0.97,
                ((0, 40), (200, 40), (200, 60), (0, 60)),
            ),
        )


class RecordingPiiDetector:
    name = "test-pii"
    model = "test-model"

    def __init__(self, entities: tuple[PiiEntity, ...]) -> None:
        self.entities = entities
        self.pages: list[int] = []

    def detect(self, page: OcrPageText) -> tuple[PiiEntity, ...]:
        self.pages.append(page.page_number)
        return self.entities


class FailingPiiDetector(RecordingPiiDetector):
    def detect(self, page: OcrPageText) -> tuple[PiiEntity, ...]:
        raise PiiMappingError("pii failed")


class RecordingManifestWriter:
    def __init__(self) -> None:
        self.manifests: list[tuple[str, PageManifest]] = []

    def create_manifest(self, owner_id: str, manifest: PageManifest) -> object:
        self.manifests.append((owner_id, manifest))
        return manifest


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


def png_bytes() -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (1, 1), color=(255, 255, 255)).save(output, format="PNG")
    return output.getvalue()


def ocr_page(text: str = "Email ada@example.com phone +1 415 555 0199") -> OcrPageText:
    return OcrPageText(
        job_id="job-123",
        page_number=1,
        page_width=200,
        page_height=100,
        engine="test-ocr",
        model="test-model",
        page_text=text,
        blocks=(
            OcrTextBlock(
                text=text,
                confidence=0.99,
                polygon=((0, 0), (1, 0), (1, 0.2), (0, 0.2)),
                start=0,
                end=len(text),
            ),
        ),
    )


def test_map_pii_regions_creates_safe_selected_regions() -> None:
    page = ocr_page()

    regions = map_pii_regions(
        page,
        (
            PiiEntity("email", 6, 21, 0.95),
            PiiEntity("phone_number", 28, 43, 0.9),
            PiiEntity("person", 0, 5, 0.49),
        ),
    )

    assert [region.category for region in regions] == ["email", "phone_number"]
    assert all(region.source is RegionSource.AUTOMATIC for region in regions)
    assert all(region.selected for region in regions)
    assert all(region.confidence is not None for region in regions)
    assert "ada@example.com" not in regions[0].model_dump_json()


def test_substring_geometry_uses_character_ratios() -> None:
    page = ocr_page("abcdefghij")

    (region,) = map_pii_regions(page, (PiiEntity("secret", 2, 5, 0.8),))

    assert region.x == pytest.approx(0.2)
    assert region.y == 0
    assert region.width == pytest.approx(0.3)
    assert region.height == pytest.approx(0.2)


def test_multiple_entities_on_one_line_get_stable_regions() -> None:
    page = ocr_page("alpha beta gamma")

    regions = map_pii_regions(
        page,
        (
            PiiEntity("first_name", 0, 5, 0.9),
            PiiEntity("last_name", 11, 16, 0.91),
        ),
    )

    assert [region.id for region in regions] == ["pii-1-1-1", "pii-1-2-1"]
    assert regions[0].x < regions[1].x


def test_mapping_clamps_geometry_to_page_bounds() -> None:
    text = "edge"
    page = OcrPageText(
        job_id="job-123",
        page_number=1,
        page_width=100,
        page_height=100,
        engine="test-ocr",
        model="test-model",
        page_text=text,
        blocks=(
            OcrTextBlock(
                text=text,
                confidence=0.9,
                polygon=((0.9, 0.9), (1.1, 0.9), (1.1, 1.1), (0.9, 1.1)),
                start=0,
                end=len(text),
            ),
        ),
    )

    (region,) = map_pii_regions(page, (PiiEntity("account_id", 0, 4, 0.8),))

    assert region.x == pytest.approx(0.9)
    assert region.y == pytest.approx(0.9)
    assert region.x + region.width <= 1
    assert region.y + region.height <= 1


def test_mapping_rejects_span_outside_page_text() -> None:
    with pytest.raises(PiiMappingError):
        map_pii_regions(ocr_page("short"), (PiiEntity("email", 0, 10, 0.8),))


def test_create_pii_manifests_writes_manifest_for_empty_page() -> None:
    detector = RecordingPiiDetector(())
    writer = RecordingManifestWriter()

    manifests = create_pii_manifests(
        make_job(),
        (ocr_page("No sensitive text"),),
        detector=detector,
        writer=writer,
        now=NOW,
    )

    assert len(manifests) == 1
    assert manifests[0].suggestions == ()
    assert manifests[0].regions == ()
    assert manifests[0].version == 1
    assert manifests[0].last_saved_at == NOW
    assert writer.manifests == [("user-456", manifests[0])]


def test_analyze_source_runs_pii_after_ocr_and_creates_manifest() -> None:
    jobs = RecordingJobs()
    raster_writer = RecordingRasterWriter()
    ocr_store = RecordingOcrStore(
        {"users/user-456/jobs/job-123/artifacts/pages/1.png": b"page"}
    )
    detector = RecordingPiiDetector(
        (
            PiiEntity("email", 6, 21, 0.95),
            PiiEntity("phone_number", 28, 43, 0.9),
            PiiEntity("passport_number", 53, 62, 0.88),
            PiiEntity("api_key", 71, 85, 0.92),
            PiiEntity("full_name", 86, 98, 0.86),
            PiiEntity("street_address", 108, 119, 0.84),
        )
    )
    manifest_writer = RecordingManifestWriter()
    downstream_called = False

    def render_pages():
        yield RenderedPage(1, 200, 100, b"\x89PNG\r\n\x1a\npage")

    def write_downstream(_: ValidatedSource) -> None:
        nonlocal downstream_called
        assert manifest_writer.manifests
        downstream_called = True

    job = analyze_source(
        make_job(),
        png_bytes(),
        jobs=jobs,
        now=NOW,
        config=None,
        raster_writer=raster_writer,
        ocr_store=ocr_store,
        ocr_engine=RecordingOcrEngine(),
        pii_detector=detector,
        manifest_writer=manifest_writer,
        render_pages=render_pages,
        write_artifacts=write_downstream,
    )

    assert job.status is JobStatus.QUEUED
    assert jobs.saved == []
    assert detector.pages == [1]
    assert downstream_called
    manifest = manifest_writer.manifests[0][1]
    assert [region.category for region in manifest.suggestions] == [
        "email",
        "phone_number",
        "passport_number",
        "api_key",
        "full_name",
        "street_address",
    ]


def test_analyze_source_persists_processing_failed_on_pii_error() -> None:
    jobs = RecordingJobs()
    raster_writer = RecordingRasterWriter()
    ocr_store = RecordingOcrStore(
        {"users/user-456/jobs/job-123/artifacts/pages/1.png": b"page"}
    )
    manifest_writer = RecordingManifestWriter()
    downstream_called = False

    def render_pages():
        yield RenderedPage(1, 200, 100, b"\x89PNG\r\n\x1a\npage")

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
        ocr_engine=RecordingOcrEngine(),
        pii_detector=FailingPiiDetector(()),
        manifest_writer=manifest_writer,
        render_pages=render_pages,
        write_artifacts=write_downstream,
    )

    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is FailureCode.PROCESSING_FAILED
    assert jobs.saved == [(failed, 1)]
    assert manifest_writer.manifests == []
    assert not downstream_called
