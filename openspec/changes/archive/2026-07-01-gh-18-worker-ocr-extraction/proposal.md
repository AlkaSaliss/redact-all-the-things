## Why

The worker now produces deterministic page PNG artifacts, but later PII mapping
needs ordered OCR text with page identity and geometry. This slice adds the OCR
artifact boundary before PII detection, checkpointing, or review manifests.

## What Changes

- Run PaddleOCR over each rasterized page artifact after successful
  rasterization.
- Persist one owner/job-namespaced OCR JSON artifact per page containing ordered
  line text, confidence, normalized polygons, and offsets into the page text.
- Use PP-OCRv6 medium through embedded Python standard local inference, with
  text-line orientation enabled and heavier document preprocessing disabled.
- Add a minimal worker Dockerfile that installs the OCR runtime and bakes pinned
  model artifacts into the image for offline job execution.
- Keep PII classification, redaction suggestions, page manifests,
  checkpoint/resume behavior, public APIs, AWS Batch infrastructure, and job
  lifecycle/progress updates out of scope.

## Capabilities

### New Capabilities

- `worker-ocr-extraction`: Worker-side OCR extraction from raster page artifacts
  into per-page text artifacts with geometry for later PII mapping.

### Modified Capabilities

None.

## Impact

- Adds analysis-worker OCR contracts, extraction code, focused worker tests,
  an OCR JSON contract fixture, worker architecture documentation, and a worker
  Dockerfile.
- Adds PaddleOCR/Paddle runtime dependencies for the worker image.
- Reuses existing job, failure-code, raster page artifact, and owner/job storage
  namespace contracts.
- Does not change public HTTP APIs, DynamoDB job fields, review manifests,
  PII detection, rendering, or production AWS infrastructure.
