## Why

The analysis worker currently stops after source validation, but later OCR work
needs deterministic page images with stable ordering. This slice adds the
rasterization boundary so accepted PDF, JPEG, and PNG sources become
page-numbered artifacts without introducing OCR, PII detection, checkpointing,
or review manifests.

## What Changes

- Rasterize each accepted PDF page into a deterministic PNG page artifact at a
  fixed DPI.
- Normalize accepted JPEG and PNG uploads into the same one-page PNG artifact
  contract.
- Write a small page-artifact index containing page number, image dimensions,
  raster format, and owner/job-namespaced storage key for each page.
- Process pages sequentially so implementation can stay within documented
  worker memory constraints.
- Classify post-validation rasterization failures as permanent
  `processing_failed` failures.
- Keep OCR, PII detection, checkpoint/resume behavior, page manifests, render
  mode, public APIs, and infrastructure out of scope.

## Capabilities

### New Capabilities

- `worker-rasterization`: Worker-side source rasterization into deterministic
  page image artifacts and metadata for downstream OCR.

### Modified Capabilities

None.

## Impact

- Adds analysis-worker rasterization code, artifact metadata types, focused
  worker tests, and worker architecture documentation.
- Adds `pypdfium2` as the PDFium-backed PDF rasterization dependency.
- Reuses existing shared source-type, job lifecycle, storage namespace, and
  safe failure-code contracts.
- Does not change public HTTP APIs, DynamoDB job fields, review manifests, OCR,
  PII detection, rendering, or AWS infrastructure.
