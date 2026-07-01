## Context

Issue #17 is the second implementation slice for the analysis-worker epic. The
worker already validates PDF, JPEG, and PNG source bytes and returns source type
and page count before any artifact creation. Later OCR and PII slices need a
stable set of page images to consume, but OCR, PII detection, checkpointing,
and page-manifest integration remain separate child issues.

The technical scope requires CPU-only PDF rasterization with PDFium through
`pypdfium2`, one-page handling for uploaded images, sequential processing, and
an 8 GB memory ceiling.

## Goals / Non-Goals

**Goals:**

- Convert validated PDF, JPEG, and PNG sources into deterministic PNG page
  artifacts.
- Preserve source page ordering with stable 1-based page numbers.
- Write a small page-artifact index with page number, dimensions, format, and
  storage key for downstream OCR.
- Process pages sequentially to avoid retaining all rendered pages in memory.
- Normalize rasterization failures into safe `processing_failed` job failures.

**Non-Goals:**

- Run OCR, PII detection, model loading, or confidence thresholding.
- Create review page manifests, suggestions, selected redaction regions, or
  checkpoint/resume state.
- Add render-mode export behavior, public API routes, production AWS
  infrastructure, or frontend behavior.
- Change DynamoDB job fields or the public job lifecycle.

## Decisions

### Use PDFium through pypdfium2 for PDF rasterization

The worker will add `pypdfium2` and use it to open already-validated PDFs and
render each page at a fixed DPI. This matches the architecture scope and avoids
introducing a different PDF rendering engine in the implementation slice.

The rejected alternative is extending the current PDF byte inspection into a
homegrown renderer. That is not viable for real PDF rendering and would create
more risk than a focused dependency.

### Normalize all page artifacts to PNG

PDF pages and uploaded JPEG/PNG images will all produce PNG artifacts. A fixed
DPI will be used for PDF pages so dimensions are predictable for tests and
downstream OCR. Uploaded images will be decoded and re-encoded as PNG page
artifacts so later stages consume one format.

JPEG output was rejected because lossy compression can make OCR and regression
tests less stable. Preserving source image format was rejected because it would
force downstream OCR to handle inconsistent artifact formats immediately.

### Store an explicit page-artifact index

Rasterization will write one index for the job containing ordered entries with
page number, width, height, format `png`, and storage key. Artifact keys will
stay under the existing owner/job namespace, for example beneath an analysis
artifacts or page preview prefix, so the worker does not leak data outside the
job boundary.

The index is not a page manifest. It contains image metadata needed by OCR, not
OCR text, detected PII, suggestions, or user-selected regions.

### Keep processing sequential and writer-driven

The rasterization entry point will render one page, write its PNG bytes, record
its metadata, release page-specific resources, and then continue. Tests should
use a recording writer or renderer stub to prove ordering and avoid requiring
large source artifacts for memory-sensitive behavior.

The rejected alternative is returning all rendered page bytes from
rasterization. That would make the API simpler but violates the sequential
memory constraint for large PDFs.

### Treat renderer failures as permanent processing failures

Source validation already classifies malformed and unsupported inputs before
rasterization. If an accepted source still fails during rendering, the worker
will persist `failed` with `processing_failed`. Transient infrastructure and
Spot interruption failures remain separate retryable failure categories and are
not expanded in this slice.

Partial page artifacts may exist if failure occurs after some writes. Later
checkpoint/resume or cleanup behavior can own recovery policy; this slice only
guarantees that no downstream OCR, PII, or review-manifest artifacts are written
after rasterization failure.

## Risks / Trade-offs

- **PDFium output can vary by renderer version** -> Pin `pypdfium2` in
  dependencies and use simple deterministic fixtures for tests.
- **Large PDFs can exhaust memory if pages accumulate** -> Design the worker
  interface around per-page rendering and immediate writes.
- **Image decoding can expose decompression risk** -> Reuse the existing
  validation limits before rasterization and avoid accepting unvalidated bytes.
- **Partial raster artifacts can remain after failure** -> Persist a safe job
  failure and leave cleanup/checkpoint policy to later storage lifecycle or
  checkpoint slices.
- **Artifact key naming can leak structure if inconsistent** -> Keep keys under
  existing owner/job namespaces and cover expected key shape in tests.

## Migration Plan

1. Add focused worker rasterization tests for multi-page PDF ordering, one-page
   JPEG/PNG normalization, page-artifact metadata, sequential writer calls, and
   safe failure persistence.
2. Add the `pypdfium2` dependency and implement rasterization types, fixed-DPI
   configuration, and writer interfaces using existing worker validation
   results.
3. Integrate successful rasterization into the analyze path after validation
   and before any later OCR/PII hooks.
4. Update worker architecture documentation with the raster artifact contract
   and out-of-scope downstream artifacts.
5. Run focused worker tests, strict OpenSpec validation, strict MkDocs, and
   Graphify refresh.

No production data migration is required. Rollback is reverting the
rasterization code, dependency, tests, docs, and OpenSpec change.

## Open Questions

None.
