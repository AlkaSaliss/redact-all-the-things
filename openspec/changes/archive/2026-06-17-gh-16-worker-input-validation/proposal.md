## Why

The analysis worker must reject invalid or unsafe source objects before any
analysis work starts so malformed, unsupported, or oversized inputs do not
produce partial artifacts or leak sensitive content. This slice establishes the
worker-side validation boundary before rasterization, OCR, and PII detection are
implemented in later slices.

## What Changes

- Add worker input validation for uploaded PDF, JPEG, and PNG source objects.
- Accept valid supported sources for later analysis without performing OCR,
  rasterization, or PII detection in this slice.
- Reject unsupported formats, malformed files, oversized files, and PDF page
  count violations with safe failure codes.
- Ensure rejected inputs do not create analysis artifacts, previews, OCR text,
  detected PII, or page manifests.
- Keep failure persistence limited to the existing job lifecycle and safe
  failure-code contract.

## Capabilities

### New Capabilities

- `worker-input-validation`: Worker-side source validation and safe failure
  behavior before analysis begins.

### Modified Capabilities

- `job-contracts`: Clarify safe failure-code behavior for permanent worker
  validation and content failures produced before analysis artifacts exist.

## Impact

- Adds analysis-worker validation code and focused unit/contract tests.
- Uses existing shared job-domain failure-code values used by the control plane
  and worker.
- Does not add OCR, rasterization, PII detection, rendering, new APIs, or new
  infrastructure.
