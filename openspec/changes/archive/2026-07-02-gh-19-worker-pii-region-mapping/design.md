## Context

Issue #19 follows the OCR extraction slice. The worker already validates
sources, rasterizes them into page PNG artifacts, and stores OCR JSON artifacts
with ordered page text, normalized line polygons, and page-local character
offsets. Review manifests already exist as the control-plane contract, but the
worker does not yet create them from detected PII.

The technical scope requires model-backed PII detection, no job-time model
downloads, safe persisted categories instead of raw detected values, normalized
geometry within page bounds, and deterministic unit tests through injected
detector results.

## Goals / Non-Goals

**Goals:**

- Detect PII spans from OCR page text using GLiNER2.
- Use all 42 labels supported by `fastino/gliner2-privacy-filter-PII-multi`.
- Convert accepted spans into automatic `RedactionRegion` suggestions.
- Create one page manifest per OCR page with suggestions selected by default.
- Normalize PII and manifest write failures into safe `processing_failed`
  failures.

**Non-Goals:**

- Change OCR artifact shape or require word-level OCR geometry.
- Persist raw detected PII text outside existing OCR artifacts.
- Add frontend review UI, export rendering, checkpoint/resume, progress updates,
  AWS Batch job definitions, ECR publishing, or new public API routes.
- Tune per-label thresholds or add domain-specific false-positive filters.

## Decisions

### Use GLiNER2 PII with bundled assets

The worker will use `fastino/gliner2-privacy-filter-PII-multi` through a small
`PiiDetector` boundary. Production will load the model from bundled worker image
assets, while tests inject deterministic detector results. Job execution must
not download model assets dynamically.

The model card documents a GLiNER2 PII model with 42 fine-grained labels,
span output, confidence output, and a `0.5` threshold example. This matches the
slice's need for model-backed detection and character spans.

### Persist safe categories, not raw detected values

Detected text is sensitive. The detector may return matched values, but the
worker will persist only the normalized category label, confidence, geometry,
identifier, page number, and selected state in manifests. Raw OCR text remains
limited to the existing owner/job-namespaced OCR artifacts.

### Start with threshold 0.5 and selected suggestions

The first implementation will accept detector spans with confidence at or above
`0.5`. Automatic regions will be selected by default because export still
requires human review, and missed redactions are worse than review-time
over-selection for this workflow.

### Approximate substring geometry from line polygons

OCR artifacts currently expose line-level polygons. The mapping will find OCR
blocks overlapping a detected character span and convert each overlap into an
axis-aligned rectangle. For a span inside one line, the rectangle's horizontal
start and width are estimated by character ratio within that block's text. The
rectangle uses the block polygon's vertical bounds and is clamped to normalized
page bounds.

Word-level OCR geometry was rejected for this slice because it would change the
OCR contract and expand issue #19 beyond PII mapping.

### Create review manifests directly

For each OCR page, the worker will create a `PageManifest` with automatic
suggestions and initial selected regions equal to the detected regions. This
makes the successful analyze output directly reviewable through the existing
control-plane manifest APIs.

Persisting only detected-region artifacts was rejected because it would require
another slice before review could consume the analysis output.

## Risks / Trade-offs

- **Model dependency size and build time** -> Keep the adapter behind a protocol
  and use deterministic unit tests; only worker image packaging pays the model
  cost.
- **Model precision is imperfect** -> Keep threshold behavior explicit and
  selected suggestions reviewable by the user.
- **Line-level geometry can over- or under-cover text** -> Use conservative
  clamping and contract tests; defer word-level geometry until OCR output
  supports it.
- **All-label policy can change with the external model** -> Store category
  strings as model output labels and test representative labels instead of
  snapshotting external model internals.

## Migration Plan

1. Add the PII mapping spec and deterministic tests for synthetic OCR spans and
   normalized regions.
2. Implement detector result contracts, GLiNER2 adapter, span-to-region mapping,
   manifest creation, and manifest writer boundary.
3. Integrate PII mapping after OCR succeeds and before later downstream hooks.
4. Add worker runtime dependencies and documentation for model packaging.
5. Run focused tests, strict OpenSpec validation, MkDocs, and Graphify refresh.

Rollback is reverting the PII code, dependency additions, tests, docs, and
OpenSpec change. No data migration is required because the feature only creates
new per-page manifests for new analysis runs.

## Open Questions

None.
