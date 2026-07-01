## Why

The worker now produces page-local OCR text and line geometry, but review cannot
begin until sensitive spans are converted into normalized redaction regions.
This slice adds model-backed PII detection and creates the initial page
manifests used by human review.

## What Changes

- Run GLiNER2 PII detection over each OCR page after successful OCR extraction.
- Use `fastino/gliner2-privacy-filter-PII-multi` with all supported PII labels,
  threshold `0.5`, and bundled model assets for offline worker execution.
- Map detected character spans to normalized automatic `RedactionRegion`
  suggestions using OCR block offsets and line geometry.
- Create one review `PageManifest` per page with detected automatic regions as
  immutable suggestions and initially selected regions.
- Classify post-OCR PII detection, geometry mapping, or manifest creation
  failures as safe `processing_failed` failures.
- Keep frontend review UI, export rendering, checkpoint/resume behavior, public
  APIs, AWS Batch infrastructure, and raw detected PII persistence out of scope.

## Capabilities

### New Capabilities

- `worker-pii-region-mapping`: Worker-side model-backed PII detection, span to
  region mapping, and review manifest creation from OCR artifacts.

### Modified Capabilities

None.

## Impact

- Adds worker PII detection contracts, GLiNER2 adapter code, span geometry
  mapping, manifest writer boundaries, focused tests, architecture
  documentation, and worker runtime dependencies.
- Reuses existing OCR page artifacts, normalized redaction-region contracts,
  S3-style owner/job namespaces, and safe failure-code contracts.
- Does not change public HTTP APIs, DynamoDB job fields, rendering behavior, or
  production infrastructure resources.
