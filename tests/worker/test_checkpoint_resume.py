from datetime import UTC, datetime, timedelta
from io import BytesIO

from PIL import Image
from redact_api.aws import PersistenceConflictError
from redact_api.domain import (
    FailureCode,
    Job,
    JobStatus,
    PageManifest,
    RedactionRegion,
    RegionSource,
    SourceType,
)
from redact_api.worker import (
    OcrLine,
    OcrPageText,
    PageArtifact,
    PageArtifactIndex,
    PiiEntity,
    PiiMappingError,
    RenderedPage,
    analyze_source,
    page_artifact_index_key,
    render_redacted_output,
)


NOW = datetime(2026, 7, 3, 12, 0, tzinfo=UTC)


class RecordingJobs:
    def __init__(self, job: Job) -> None:
        self.current = job
        self.saved: list[tuple[Job, int]] = []

    def get(self, job_id: str) -> Job | None:
        return self.current if job_id == self.current.id else None

    def save(self, job: Job, *, expected_version: int) -> None:
        self.saved.append((job, expected_version))
        self.current = job


class RecordingRasterWriter:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    def put_page_artifact(self, key: str, content: bytes) -> None:
        self.objects[key] = content

    def put_page_artifact_index(self, key: str, content: bytes) -> None:
        self.objects[key] = content


class RecordingOcrStore:
    def __init__(self, *, index: bytes | None = None) -> None:
        self.index = index
        self.gets: list[str] = []
        self.ocr_objects: dict[str, bytes] = {}

    def get_page_artifact_index(self, key: str) -> bytes:
        if self.index is None:
            raise KeyError(key)
        return self.index

    def get_page_artifact(self, key: str) -> bytes:
        self.gets.append(key)
        return f"page:{key}".encode()

    def put_ocr_page_text(self, key: str, content: bytes) -> None:
        self.ocr_objects[key] = content


class RecordingOcrEngine:
    name = "test-ocr"
    model = "test-model"

    def __init__(self) -> None:
        self.pages: list[int] = []

    def recognize(self, page: PageArtifact, content: bytes) -> tuple[OcrLine, ...]:
        self.pages.append(page.page_number)
        return (
            OcrLine(
                text=f"Page {page.page_number}",
                confidence=0.9,
                polygon=((0, 0), (50, 0), (50, 10), (0, 10)),
            ),
        )


class RecordingPiiDetector:
    name = "test-pii"
    model = "test-model"

    def __init__(self, *, fail_page: int | None = None) -> None:
        self.fail_page = fail_page
        self.pages: list[int] = []

    def detect(self, page: OcrPageText) -> tuple[PiiEntity, ...]:
        self.pages.append(page.page_number)
        if page.page_number == self.fail_page:
            raise PiiMappingError("pii failed")
        return ()


class RecordingManifestWriter:
    def __init__(self, *, conflict_manifest: PageManifest | None = None) -> None:
        self.conflict_manifest = conflict_manifest
        self.manifests: dict[int, PageManifest] = {}

    def get_manifest(
        self,
        owner_id: str,
        job_id: str,
        page_number: int,
    ) -> PageManifest | None:
        if self.conflict_manifest is not None:
            return self.conflict_manifest
        return self.manifests.get(page_number)

    def create_manifest(self, owner_id: str, manifest: PageManifest) -> object:
        if self.conflict_manifest is not None:
            raise PersistenceConflictError("manifest already exists")
        self.manifests[manifest.page_number] = manifest
        return manifest


class RecordingRenderStore:
    def __init__(self, job: Job, manifest: PageManifest, page_png: bytes) -> None:
        self.output: tuple[str, bytes, str] | None = None
        self.manifest = manifest
        self.objects = {
            page_artifact_index_key(job.owner_id, job.id): serialized_index(
                job.model_copy(update={"page_count": 2})
            ),
            "users/user-456/jobs/job-123/artifacts/pages/1.png": page_png,
            "users/user-456/jobs/job-123/artifacts/pages/2.png": page_png,
        }

    def get_page_artifact_index(self, key: str) -> bytes:
        return self.objects[key]

    def get_page_artifact(self, key: str) -> bytes:
        return self.objects[key]

    def get_manifest(
        self,
        owner_id: str,
        job_id: str,
        page_number: int,
    ) -> PageManifest:
        return self.manifest.model_copy(update={"page_number": page_number})

    def put_output_object(
        self,
        key: str,
        content: bytes,
        *,
        content_type: str,
    ) -> None:
        self.output = (key, content, content_type)


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


def pdf_bytes(page_count: int = 2) -> bytes:
    objects = [
        "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        "2 0 obj\n<< /Type /Pages "
        f"/Kids [{' '.join(f'{number} 0 R' for number in range(3, page_count + 3))}] "
        f"/Count {page_count} >>\nendobj\n",
    ]
    objects.extend(
        f"{number} 0 obj\n"
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 72 72] >>\n"
        "endobj\n"
        for number in range(3, page_count + 3)
    )
    output = bytearray(b"%PDF-1.7\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(output))
        output.extend(obj.encode())
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode()
    )
    return bytes(output)


def render_pages():
    yield RenderedPage(1, 100, 50, b"\x89PNG\r\n\x1a\npage-1")
    yield RenderedPage(2, 100, 50, b"\x89PNG\r\n\x1a\npage-2")


def png_bytes() -> bytes:
    output = BytesIO()
    Image.new("RGB", (100, 100), "white").save(output, format="PNG")
    return output.getvalue()


def serialized_index(job: Job) -> bytes:
    index = PageArtifactIndex(
        job_id=job.id,
        key=page_artifact_index_key(job.owner_id, job.id),
        pages=(
            PageArtifact(
                1,
                100,
                50,
                "png",
                "users/user-456/jobs/job-123/artifacts/pages/1.png",
            ),
            PageArtifact(
                2,
                100,
                50,
                "png",
                "users/user-456/jobs/job-123/artifacts/pages/2.png",
            ),
        ),
    )
    from redact_api.worker import _serialize_page_artifact_index

    return _serialize_page_artifact_index(index)


def selected_manifest(job: Job) -> PageManifest:
    region = RedactionRegion(
        id="region-1",
        page_number=1,
        x=0,
        y=0,
        width=0.5,
        height=0.5,
        source=RegionSource.MANUAL,
        category="manual",
        selected=True,
    )
    return PageManifest(
        job_id=job.id,
        page_number=1,
        suggestions=(),
        regions=(region,),
        version=1,
        last_saved_at=NOW,
    )


def test_analyze_source_checkpoints_pages_and_marks_ready() -> None:
    job = make_job()
    jobs = RecordingJobs(job)
    engine = RecordingOcrEngine()
    detector = RecordingPiiDetector()

    ready = analyze_source(
        job,
        pdf_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=RecordingRasterWriter(),
        ocr_store=RecordingOcrStore(),
        ocr_engine=engine,
        pii_detector=detector,
        manifest_writer=RecordingManifestWriter(),
        render_pages=render_pages,
    )

    assert ready.status is JobStatus.READY
    assert ready.page_count == 2
    assert ready.completed_pages == 2
    assert [saved.status for saved, _ in jobs.saved] == [
        JobStatus.ANALYZING,
        JobStatus.ANALYZING,
        JobStatus.ANALYZING,
        JobStatus.READY,
    ]
    assert [saved.completed_pages for saved, _ in jobs.saved] == [0, 1, 2, 2]
    assert engine.pages == [1, 2]
    assert detector.pages == [1, 2]


def test_render_redacted_output_burns_regions_and_marks_complete() -> None:
    job = make_job(
        status=JobStatus.EXPORTING,
        page_count=2,
        completed_pages=2,
        version=5,
    )
    jobs = RecordingJobs(job)
    store = RecordingRenderStore(job, selected_manifest(job), png_bytes())

    complete = render_redacted_output(job, jobs=jobs, store=store, now=NOW)

    assert complete.status is JobStatus.COMPLETE
    assert store.output is not None
    key, content, content_type = store.output
    assert key == "users/user-456/jobs/job-123/output"
    assert content_type == "application/pdf"
    assert content.startswith(b"%PDF")


def test_render_redacted_image_output_burns_selected_pixels() -> None:
    job = make_job(
        source_type=SourceType.PNG,
        status=JobStatus.EXPORTING,
        page_count=2,
        completed_pages=2,
        version=5,
    )
    jobs = RecordingJobs(job)
    store = RecordingRenderStore(job, selected_manifest(job), png_bytes())

    render_redacted_output(job, jobs=jobs, store=store, now=NOW)

    assert store.output is not None
    _, content, content_type = store.output
    assert content_type == "image/png"
    with Image.open(BytesIO(content)) as image:
        assert image.getpixel((10, 10)) == (0, 0, 0)
        assert image.getpixel((75, 75)) == (255, 255, 255)


def test_analyze_source_resumes_after_completed_pages() -> None:
    job = make_job(page_count=2, completed_pages=1, version=4)
    jobs = RecordingJobs(job)
    engine = RecordingOcrEngine()
    detector = RecordingPiiDetector()

    ready = analyze_source(
        job,
        pdf_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=RecordingRasterWriter(),
        ocr_store=RecordingOcrStore(index=serialized_index(job)),
        ocr_engine=engine,
        pii_detector=detector,
        manifest_writer=RecordingManifestWriter(),
        render_pages=render_pages,
    )

    assert ready.status is JobStatus.READY
    assert ready.completed_pages == 2
    assert engine.pages == [2]
    assert detector.pages == [2]


def test_analyze_source_preserves_checkpoint_on_later_page_failure() -> None:
    job = make_job()
    jobs = RecordingJobs(job)

    failed = analyze_source(
        job,
        pdf_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=RecordingRasterWriter(),
        ocr_store=RecordingOcrStore(),
        ocr_engine=RecordingOcrEngine(),
        pii_detector=RecordingPiiDetector(fail_page=2),
        manifest_writer=RecordingManifestWriter(),
        render_pages=render_pages,
    )

    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is FailureCode.PROCESSING_FAILED
    assert failed.completed_pages == 1


def test_existing_initial_manifest_is_idempotent_for_checkpoint_retry() -> None:
    job = make_job(page_count=1, completed_pages=0, version=2)
    expected = PageManifest(
        job_id=job.id,
        page_number=1,
        suggestions=(),
        regions=(),
        version=1,
        last_saved_at=NOW,
    )
    jobs = RecordingJobs(job)

    ready = analyze_source(
        job,
        pdf_bytes(page_count=1),
        jobs=jobs,
        now=NOW,
        raster_writer=RecordingRasterWriter(),
        ocr_store=RecordingOcrStore(),
        ocr_engine=RecordingOcrEngine(),
        pii_detector=RecordingPiiDetector(),
        manifest_writer=RecordingManifestWriter(conflict_manifest=expected),
        render_pages=lambda: (RenderedPage(1, 100, 50, b"\x89PNG\r\n\x1a\npage"),),
    )

    assert ready.status is JobStatus.READY
    assert ready.completed_pages == 1


def test_missing_resume_index_fails_safely() -> None:
    job = make_job(page_count=2, completed_pages=1, version=4)
    jobs = RecordingJobs(job)

    failed = analyze_source(
        job,
        pdf_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=RecordingRasterWriter(),
        ocr_store=RecordingOcrStore(index=None),
        ocr_engine=RecordingOcrEngine(),
        pii_detector=RecordingPiiDetector(),
        manifest_writer=RecordingManifestWriter(),
        render_pages=render_pages,
    )

    assert failed.status is JobStatus.FAILED
    assert failed.failure_code is FailureCode.PROCESSING_FAILED
    assert failed.completed_pages == 1


def test_retry_after_final_checkpoint_marks_ready_without_index() -> None:
    job = make_job(page_count=2, completed_pages=2, version=5)
    jobs = RecordingJobs(job)

    ready = analyze_source(
        job,
        pdf_bytes(),
        jobs=jobs,
        now=NOW,
        raster_writer=RecordingRasterWriter(),
        ocr_store=RecordingOcrStore(index=None),
        ocr_engine=RecordingOcrEngine(),
        pii_detector=RecordingPiiDetector(),
        manifest_writer=RecordingManifestWriter(),
        render_pages=render_pages,
    )

    assert ready.status is JobStatus.READY
    assert ready.completed_pages == 2
