# Analysis worker

The analysis worker consumes owner-scoped `analyze` submissions from the
control plane and reuses the shared job, source-type, and failure-code
contracts from `redact_api.domain`.

This slice implements only the validation boundary before analysis work starts.
Rasterization, OCR, PII detection, checkpoints, previews, page manifests, and
rendering remain later worker slices.

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

The current implementation uses standard-library byte parsing for PDF and image
content. No PDF or image parser dependency is required for this validation-only
slice.

## Safe failures

Unsupported signatures or decoded content fail with `unsupported_content`.
Malformed, encrypted, oversized, over-page-limit, or over-pixel-limit content
fails with `validation_failed`.

Both failure codes are permanent and non-retryable. On validation failure the
worker persists only the safe job failure state and does not write previews,
OCR text, detected PII, analysis artifacts, or page manifests.
