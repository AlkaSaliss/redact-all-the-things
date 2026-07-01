"""Run a local OCR smoke test over sample files without printing OCR text."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from redact_api.domain import Job, JobStatus, SourceType
from redact_api.worker import (
    OcrPageText,
    PageArtifactIndex,
    PaddleOcrEngine,
    WorkerValidationConfig,
    validate_source,
    rasterize_source,
    extract_ocr_text,
)


NOW = datetime(2026, 7, 1, 12, 0, tzinfo=UTC)


@dataclass
class MemoryArtifactStore:
    objects: dict[str, bytes]

    def put_page_artifact(self, key: str, content: bytes) -> None:
        self.objects[key] = content

    def put_page_artifact_index(self, key: str, content: bytes) -> None:
        self.objects[key] = content

    def get_page_artifact(self, key: str) -> bytes:
        return self.objects[key]

    def put_ocr_page_text(self, key: str, content: bytes) -> None:
        self.objects[key] = content


def main(paths: list[str]) -> int:
    if not paths:
        print("usage: worker_ocr_smoke.py <sample-file> [<sample-file> ...]", file=sys.stderr)
        return 2

    engine = PaddleOcrEngine()
    for index, raw_path in enumerate(paths, start=1):
        path = Path(raw_path)
        source_type = source_type_for(path)
        source = path.read_bytes()
        job = make_job(f"smoke-{index}", source_type)
        store = MemoryArtifactStore({})

        validated = validate_source(
            source_type,
            source,
            config=WorkerValidationConfig(),
        )
        page_index = rasterize_source(job, source, validated, writer=store)
        pages = extract_ocr_text(job, page_index, store=store, engine=engine)

        print(summary(path, page_index, pages))
    return 0


def source_type_for(path: Path) -> SourceType:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return SourceType.PDF
    if suffix in {".jpg", ".jpeg"}:
        return SourceType.JPEG
    if suffix == ".png":
        return SourceType.PNG
    raise ValueError(f"unsupported sample file type: {path}")


def make_job(job_id: str, source_type: SourceType) -> Job:
    return Job(
        id=job_id,
        owner_id="local-smoke",
        source_type=source_type,
        source_key=f"users/local-smoke/jobs/{job_id}/source",
        output_key=f"users/local-smoke/jobs/{job_id}/output",
        status=JobStatus.QUEUED,
        page_count=0,
        completed_pages=0,
        created_at=NOW,
        expires_at=NOW + timedelta(hours=24),
        model_versions={},
        version=1,
    )


def summary(path: Path, page_index: PageArtifactIndex, pages: tuple[OcrPageText, ...]) -> str:
    payload = {
        "file": str(path),
        "pages": len(page_index.pages),
        "ocr_blocks": [len(page.blocks) for page in pages],
        "ocr_text_lengths": [len(page.page_text) for page in pages],
    }
    return json.dumps(payload, sort_keys=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
