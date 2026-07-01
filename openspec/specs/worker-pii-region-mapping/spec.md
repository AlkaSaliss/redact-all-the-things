## Purpose

Define worker-side model-backed PII detection, normalized redaction-region
mapping, and review manifest creation from OCR page artifacts.

## Requirements

### Requirement: Worker detects PII from OCR artifacts
The analysis worker SHALL run model-backed PII detection over each OCR page
artifact after successful OCR extraction and before review manifest creation.

#### Scenario: Detect PII for each OCR page
- **WHEN** OCR extraction succeeds for a source with multiple OCR page artifacts
- **THEN** PII detection runs once for each page in page-number order

#### Scenario: Use configured GLiNER2 detector
- **WHEN** production PII detection runs
- **THEN** the worker uses the bundled `fastino/gliner2-privacy-filter-PII-multi` GLiNER2 model without downloading model assets during job execution

#### Scenario: Keep PII after OCR
- **WHEN** source validation, rasterization, or OCR extraction fails
- **THEN** the worker does not run PII detection or write review manifests

### Requirement: PII spans become normalized redaction regions
The analysis worker SHALL convert accepted PII spans into automatic
`RedactionRegion` contracts with normalized geometry, safe categories, detector
confidence, and selected state.

#### Scenario: Map detected span to region
- **WHEN** a detector returns a span with confidence at least `0.5`
- **THEN** the worker creates an automatic selected redaction region with the detector label as category and confidence copied from the detector score

#### Scenario: Approximate substring geometry
- **WHEN** a detected span overlaps part of one OCR line block
- **THEN** the worker derives the region rectangle from the block polygon and the span's character-offset ratio within that line

#### Scenario: Clamp region geometry
- **WHEN** mapped geometry is created near a page boundary
- **THEN** the worker clamps the normalized rectangle so contract validation keeps it within page bounds

#### Scenario: Avoid raw detected values in regions
- **WHEN** a PII region is persisted
- **THEN** it contains category, confidence, geometry, source, selected state, and identifiers, but not the raw detected text value

### Requirement: Worker creates review manifests from detected regions
The analysis worker SHALL create one `PageManifest` per OCR page using detected
automatic regions as immutable suggestions and initial selected regions.

#### Scenario: Create page manifest
- **WHEN** PII mapping succeeds for a page
- **THEN** the worker writes a page manifest with version `1`, an aware save timestamp, suggestions equal to the automatic regions, and regions equal to the same selected automatic regions

#### Scenario: Preserve empty pages
- **WHEN** a page has no accepted PII spans
- **THEN** the worker still writes a valid page manifest with empty suggestions and empty regions

### Requirement: PII mapping failures are safe permanent failures
The analysis worker SHALL classify post-OCR PII detection, geometry mapping, and
manifest creation failures as safe permanent processing failures.

#### Scenario: Persist safe failure on PII mapping error
- **WHEN** OCR succeeds but PII detection, region mapping, or manifest creation fails
- **THEN** the worker transitions the job to `failed` with safe failure code `processing_failed`

#### Scenario: Avoid partial downstream review state
- **WHEN** PII mapping fails before all manifests are created
- **THEN** the worker does not continue writing additional review manifests or user-selected redaction regions
