## Purpose

Define worker-side OCR extraction from raster page artifacts into per-page text
artifacts with geometry for later PII mapping.

## Requirements

### Requirement: Worker extracts OCR text from page artifacts
The analysis worker SHALL run OCR over each rasterized PNG page artifact after
successful rasterization and before PII detection or review-manifest creation.

#### Scenario: Extract OCR for each page artifact
- **WHEN** rasterization succeeds for a source object with multiple page artifacts
- **THEN** OCR runs once for each indexed page artifact in page-number order

#### Scenario: Keep OCR after rasterization
- **WHEN** source validation or rasterization fails
- **THEN** the worker does not run OCR or write OCR artifacts

### Requirement: OCR artifacts preserve page text and geometry
The analysis worker SHALL persist one OCR JSON artifact per page containing the
job identifier, page number, page dimensions, OCR model metadata, ordered page
text, and ordered OCR line blocks.

#### Scenario: Persist line-level OCR output
- **WHEN** OCR succeeds for a page artifact
- **THEN** the page OCR artifact contains one entry per recognized line with text, confidence, normalized four-point polygon geometry, and `start` and `end` offsets into the ordered page text

#### Scenario: Normalize OCR geometry
- **WHEN** an OCR engine returns pixel-space polygons for a page
- **THEN** the worker stores polygon coordinates normalized by the raster page width and height

#### Scenario: Store OCR separately from review manifests
- **WHEN** OCR writes per-page text artifacts
- **THEN** it does not write detected PII, redaction suggestions, page manifests, user-selected redaction regions, or DynamoDB job metadata fields

### Requirement: OCR runtime is packaged for offline worker execution
The worker image SHALL include the pinned PaddleOCR runtime configuration and
model artifacts needed for PP-OCRv6 medium OCR without downloading models during
job execution.

#### Scenario: Worker image contains OCR runtime assets
- **WHEN** the worker container image is built
- **THEN** it contains the configured OCR runtime dependencies and local model artifact paths used by the embedded OCR engine

#### Scenario: Keep deployment infrastructure out of OCR extraction
- **WHEN** OCR extraction is added
- **THEN** the change does not add AWS Batch job definitions, ECR publishing workflows, or production infrastructure resources

### Requirement: OCR failures are safe permanent failures
The analysis worker SHALL classify post-rasterization OCR extraction failures as
safe permanent processing failures.

#### Scenario: Persist safe failure on OCR error
- **WHEN** rasterization succeeds but OCR extraction fails before all page OCR artifacts are written
- **THEN** the worker transitions the job to `failed` with safe failure code `processing_failed`

#### Scenario: Avoid downstream artifacts after OCR failure
- **WHEN** OCR extraction fails
- **THEN** the worker does not write detected PII, page manifests, or user-selected redaction regions
