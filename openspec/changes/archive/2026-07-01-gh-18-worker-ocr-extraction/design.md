## Context

Issue #18 follows the worker rasterization slice. The worker already validates
PDF, JPEG, and PNG inputs, creates deterministic PNG page artifacts, and writes
a page-artifact index. Later slices need text spans that can be mapped to page
geometry, but PII detection, checkpointing, review-manifest integration, and
ready-state transitions remain separate child issues.

The technical scope requires CPU-only processing, PaddleOCR, no external OCR
APIs, no runtime model downloads in production jobs, and normalized coordinates
for downstream redaction geometry.

## Goals / Non-Goals

**Goals:**

- Extract ordered OCR text from every raster page artifact.
- Preserve page identity and normalized line polygons for later PII mapping.
- Persist one OCR JSON artifact per page under the owner/job namespace.
- Package the worker runtime with pinned PP-OCRv6 medium model artifacts.
- Normalize OCR failures into safe `processing_failed` job failures.

**Non-Goals:**

- Detect PII, map entity spans to redaction regions, or create review
  manifests.
- Add checkpoint/resume state or update job progress/readiness fields.
- Add AWS Batch job definitions, ECR publishing, or production infrastructure.
- Optimize with HPI, OpenVINO, ONNX Runtime, TensorRT, C++ deployment, or
  PaddleX serving in this slice.

## Decisions

### Use PP-OCRv6 medium through embedded Python

PP-OCRv6 medium is the initial quality-first choice for redaction recall. The
worker will call PaddleOCR in-process through an `OcrEngine` boundary so unit
tests can inject deterministic results and production can use the real engine.

The rejected alternatives are PP-OCRv6 small or older English/Latin-only models.
They may reduce footprint, but the first implementation should establish OCR
quality and artifact shape before optimizing model size.

### Start with standard local inference

The first implementation will use standard embedded Python inference. This
matches the worker's one-job-at-a-time sequential model and avoids operating a
local serving process inside the container.

HPI/OpenVINO/ONNX and PaddleX serving remain later optimizations. The local
sample PDF and JPEG should be used for opt-in smoke tests and benchmark notes
before adding those deployment engines.

### Persist one JSON artifact per page

Each OCR page artifact will contain page metadata, ordered page text, model
metadata, and line-level blocks. Blocks store text, confidence, normalized
four-point polygons, and `start`/`end` offsets into the page text. Blocks are
joined with newline separators so later PII mapping can translate page-local
character spans back to OCR line geometry without reconstructing order.

A single job-level OCR JSON was rejected because checkpoint/resume and page
manifest integration will need page-local artifacts. Returning OCR only in
memory was rejected because later slices need persisted S3 artifacts.

### Keep OCR artifacts separate from manifests

OCR artifacts are analysis artifacts, not review manifests. They must not write
detected PII, immutable suggestions, selected regions, or user edits. DynamoDB
continues to store only safe job metadata.

### Package models in the worker image

The Dockerfile will install the worker runtime as a non-root image and prepare
local model artifact paths. Runtime job execution must use local model paths and
must not download models dynamically. Production infrastructure wiring remains
out of scope.

## Risks / Trade-offs

- **PaddleOCR dependencies can make builds large or slow** -> Keep Docker scope
  minimal and defer HPI/serving engines until benchmarks justify them.
- **PP-OCRv6 medium may be slower on CPU than expected** -> Add opt-in sample
  smoke/benchmark commands using the provided PDF and JPEG.
- **OCR result shape can change across PaddleOCR versions** -> Normalize through
  a small adapter boundary and cover the internal JSON contract with fixtures.
- **Runtime model artifact acquisition can require network during image build**
  -> Allow build-time downloads only, then verify local paths exist for runtime.
- **OCR text is sensitive** -> Store only in namespaced S3-style artifacts and
  keep it out of DynamoDB and logs.

## Migration Plan

1. Add OCR contract fixtures and deterministic worker tests with injected OCR
   results.
2. Implement OCR dataclasses, serialization, per-page artifact keys, and the
   writer/engine protocols.
3. Integrate OCR after rasterization succeeds and before future downstream
   hooks.
4. Add the embedded PaddleOCR adapter and worker Dockerfile.
5. Update worker architecture documentation and run focused tests, OpenSpec
   validation, MkDocs, and Graphify refresh.

Rollback is reverting the OCR code, Dockerfile, dependencies, tests, docs, and
OpenSpec change. No production data migration is required.

## Open Questions

None.
