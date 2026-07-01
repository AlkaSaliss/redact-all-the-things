# Analysis worker

The analysis worker consumes owner-scoped `analyze` submissions from the
control plane and reuses the shared job, source-type, and failure-code
contracts from `redact_api.domain`.

The worker currently implements source validation, page rasterization, and OCR
text extraction. PII detection, checkpoints, review page manifests, and
render-mode export remain later worker slices.

## Source validation

The worker validates uploaded bytes against the job's declared source type
instead of trusting filenames, client MIME types, or file extensions.

Validation limits are loaded with PyYAML from `config/worker-validation.yml`:

```yaml
worker_validation:
  max_file_size_bytes: 104857600
  max_pdf_pages: 200
  max_image_pixels: 50000000
```

Tests may load smaller limits from temporary YAML files so limit behavior is
covered without creating large source artifacts.

Validation accepts:

- PDF sources with a PDF signature, no encryption marker, an EOF marker, and 1
  through 200 pages counted by PDFium.
- JPEG sources with a JPEG signature, a parseable Start of Frame segment,
  positive dimensions, and at most 50,000,000 decoded pixels.
- PNG sources with a PNG signature, a valid first IHDR chunk, positive
  dimensions, and at most 50,000,000 decoded pixels.

Validation rejects:

- source bytes above 100 MB;
- source signatures that do not match the job source type;
- malformed PDF, JPEG, or PNG content;
- encrypted PDFs;
- PDFs above 200 pages;
- JPEG or PNG images above 50,000,000 decoded pixels.

The validation boundary uses PDFium for PDF page counts and standard-library
byte parsing for image metadata so invalid content can fail before renderer or
OCR work starts.

## Rasterization

After validation succeeds, rasterization converts every accepted source into
PNG page artifacts under the owner/job namespace:

```text
users/{owner_id}/jobs/{job_id}/artifacts/pages/{page_number}.png
users/{owner_id}/jobs/{job_id}/artifacts/pages/index.json
```

PDF sources are rendered with PDFium through `pypdfium2` at a fixed 150 DPI.
JPEG and PNG sources are decoded with Pillow and re-encoded as the same
one-page PNG artifact contract. Page numbering is 1-based and preserves source
order.

The page-artifact index contains one entry per artifact with:

- page number;
- raster image width;
- raster image height;
- format `png`;
- owner/job-namespaced storage key.

The index is not a review manifest. It does not contain OCR text, detected PII,
suggestions, selected redaction regions, or user edits.

Rasterization renders and writes one page at a time so multi-page PDFs do not
require all page images to remain in memory at once. If validation succeeds but
rasterization fails, the worker persists `processing_failed` as a safe permanent
failure and does not write OCR output, detected PII, page manifests, or
user-selected redaction regions.

## OCR extraction

After rasterization succeeds, OCR extraction reads the page-artifact index and
runs OCR once for each PNG page artifact in page-number order. OCR output is
stored as per-page JSON artifacts:

```text
users/{owner_id}/jobs/{job_id}/artifacts/ocr/pages/{page_number}.json
```

Each OCR page artifact contains:

- job identifier;
- page number;
- raster page width and height;
- OCR engine and model identifiers;
- ordered page text;
- one block per recognized line with text, confidence, normalized four-point
  polygon geometry, and `start`/`end` offsets into the ordered page text.

The initial runtime is embedded Python PaddleOCR using PP-OCRv6 medium with
text-line orientation enabled. Document orientation classification and document
unwarping are disabled for this slice. Standard local inference is used first;
HPI, OpenVINO, ONNX Runtime, C++ deployment, and PaddleX serving remain later
optimizations if sample benchmarks justify them.

The worker image is built from `Dockerfile.worker`. It installs the PaddleOCR
runtime, runs as a non-root user, and initializes the configured OCR pipeline at
image build time so model assets are present before job execution. AWS Batch
job definitions, ECR publishing, and production infrastructure wiring remain
out of scope for this worker slice.

The files under `tests/samples/` are opt-in local smoke and benchmark inputs for
the worker OCR path. Deterministic CI tests use synthetic fixtures and injected
OCR results so they do not depend on OCR model inference.

Use `make worker-ocr-smoke` to build the local worker image and run OCR over the
sample PDF and JPEG. The Makefile builds and runs the image as `linux/amd64`,
matching the supported Paddle CPU runtime used for this worker slice.

## Safe failures

Unsupported signatures or decoded content fail with `unsupported_content`.
Malformed, encrypted, oversized, over-page-limit, or over-pixel-limit content
fails with `validation_failed`.

Both failure codes are permanent and non-retryable. On validation failure the
worker persists only the safe job failure state and does not write previews,
OCR text, detected PII, analysis artifacts, or page manifests.

Post-validation rasterization failures fail with `processing_failed`. That code
is also permanent for this slice; retryable infrastructure and Spot interruption
failures remain represented by the existing transient failure codes.

Post-rasterization OCR failures also fail with `processing_failed`. The worker
does not write detected PII, page manifests, or user-selected redaction regions
after an OCR failure.
