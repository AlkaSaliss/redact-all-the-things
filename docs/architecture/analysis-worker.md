# Analysis worker

The analysis worker consumes owner-scoped `analyze` submissions from the
control plane and reuses the shared job, source-type, and failure-code
contracts from `redact_api.domain`.

The worker currently implements source validation and page rasterization.
OCR, PII detection, checkpoints, review page manifests, and render-mode export
remain later worker slices.

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
  through 200 page objects.
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

The validation boundary uses standard-library byte parsing for PDF and image
metadata so invalid content can fail before renderer or OCR work starts.

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
