## Context

Issue #16 is the first implementation slice for the analysis-worker epic. The
control plane already creates jobs for declared PDF, JPEG, and PNG inputs,
stores source objects in owner/job-namespaced S3 keys, and submits `analyze`
worker requests through the shared `WorkerSubmission` contract.

The worker does not exist yet. This change introduces only the pre-analysis
validation boundary: it confirms that the uploaded source object is a supported
and bounded document before later slices add rasterization, OCR, PII detection,
checkpointing, or manifest creation.

## Goals / Non-Goals

**Goals:**

- Validate source bytes against the job's declared `SourceType` instead of
  trusting filenames, client MIME types, or extensions.
- Accept valid PDF, JPEG, and PNG inputs for later analysis.
- Reject unsupported, malformed, oversized, encrypted, over-page-limit, or
  over-pixel-limit inputs with safe non-retryable failure codes.
- Keep rejected-input persistence limited to the existing job failure contract
  and avoid creating analysis artifacts.
- Provide focused tests for supported and rejected validation paths.

**Non-Goals:**

- Rasterize PDFs or images.
- Run OCR, PII detection, model loading, or confidence thresholding.
- Create page previews, analysis artifacts, OCR output, detected PII, or page
  manifests.
- Add production Batch infrastructure, container packaging, or new public API
  routes.
- Build export/render behavior.

## Decisions

### Add a small worker package that consumes shared contracts

The new worker code will live under the existing Python source tree and import
`Job`, `SourceType`, `FailureCode`, and lifecycle helpers from
`redact_api.domain`. The validation entry point will accept the job metadata,
source bytes, and validation limits loaded with PyYAML from
`config/worker-validation.yml`, then return a small validation result containing
source type and page count.

Keeping validation in a worker-focused module avoids pushing file-content
inspection into the control-plane API, where only upload authorization and
object existence are in scope. Reusing shared contracts prevents drift in
source types, page limits, and safe failure codes.

### Validate decoded content, not client metadata

Validation will check file signatures and minimal decoded structure for the
declared source type:

- PDFs must have a PDF signature, be parseable enough to determine encryption
  and page count, and contain 1 through 200 pages.
- JPEG and PNG files must match their signatures, be parseable as images, and
  decode to positive dimensions whose width multiplied by height is at most
  50,000,000 pixels.
- Source bytes above the existing 100 MB object limit fail before parser work.
- Validation limits are loaded from YAML so tests can use smaller thresholds
  without creating large source artifacts.
- A signature/type mismatch or unsupported decoded content maps to
  `unsupported_content`.
- Malformed, encrypted, oversized, over-page-limit, or over-pixel-limit
  supported content maps to `validation_failed`.

The rejected alternative is trusting the source type recorded at job creation.
That is insufficient because uploaded object bytes can differ from the
metadata used to authorize the upload.

### Treat validation failures as permanent analysis failures

Worker validation failures will transition and persist the job as `failed` with
a safe failure code and no artifact writes. They are permanent and not eligible
for automatic retry. Transient infrastructure and Spot failures remain
represented by the existing retryable analyze/render codes.

Adding highly specific user-facing failure codes for every parser outcome was
rejected for this slice. The current safe code set is enough to distinguish
unsupported content, validation failures, and unexpected processing failures
without persisting sensitive parser details.

### Keep artifact prevention explicit

The validation function will not receive output writers for previews, OCR,
detection manifests, or page manifests. Tests will assert that rejected
validation returns a failure classification before any artifact-writing path
can run.

This keeps the first worker slice small and makes the privacy boundary easy to
review. Later slices can add artifact writers after validation succeeds.

## Risks / Trade-offs

- **Parser dependencies may be needed for reliable PDF/image validation** ->
  Start with the smallest dependency footprint that can safely parse page
  count, encryption, dimensions, and malformed content; document any added
  dependency in the implementation PR.
- **Malformed files can trigger parser-specific exceptions** -> Normalize all
  parser errors into safe failure codes and do not log exception messages that
  may include file content.
- **Image decompression checks can be incomplete if only signatures are read**
  -> Require decoded image metadata validation and reject JPEG/PNG inputs above
  50,000,000 decoded pixels rather than accepting signature matches alone.
- **Validation-only code may feel temporary** -> Keep the result shape aligned
  with later rasterization inputs so later slices can call it before doing work
  without refactoring contracts.
- **Failure code granularity is intentionally coarse** -> Use the existing
  permanent code set now and add new codes only if a later UX or retry decision
  requires them.

## Migration Plan

1. Add worker validation tests for accepted PDF, JPEG, and PNG inputs.
2. Add worker validation tests for unsupported signatures, malformed content,
   encrypted PDFs, oversized sources, image pixel-count violations, and PDF
   page-count violations.
3. Implement the validation module and failure mapping.
4. Add YAML-backed validation configuration and use smaller test limits for
   oversized, over-page-limit, and over-pixel-limit cases.
5. Add tests proving permanent validation/content failures persist only safe job
   failure state, are not retryable, and do not require sensitive payload
   persistence.
6. Update worker architecture documentation for the validation-only boundary.
7. Run relevant unit tests, OpenSpec validation, MkDocs, and Graphify refresh.

No production data migration is required. Rollback is reverting the worker
validation module, tests, docs, and any added dependency.

## Open Questions

None.
