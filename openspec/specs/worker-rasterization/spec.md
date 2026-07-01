## Purpose
Define how the analysis worker converts validated PDF, JPEG, and PNG sources
into deterministic PNG page artifacts for downstream processing.

## Requirements

### Requirement: Worker rasterizes accepted sources into page artifacts
The analysis worker SHALL convert each validated PDF page and each validated
JPEG or PNG image source into deterministic PNG page artifacts before OCR or
PII detection begins.

#### Scenario: Rasterize PDF pages in order
- **WHEN** an analyze worker receives a validated PDF source with multiple pages
- **THEN** rasterization produces one PNG page artifact per PDF page with page numbers `1` through the PDF page count in source order

#### Scenario: Rasterize uploaded image as one page
- **WHEN** an analyze worker receives a validated JPEG or PNG source
- **THEN** rasterization produces exactly one PNG page artifact with page number `1`

### Requirement: Page artifact metadata preserves downstream ordering
The analysis worker SHALL write a page-artifact index that records the page
number, raster image width, raster image height, raster format, and storage key
for each page artifact.

#### Scenario: Record page artifact metadata
- **WHEN** rasterization succeeds for a source object
- **THEN** the page-artifact index contains one metadata entry for each produced page artifact with stable page number, positive image dimensions, format `png`, and an owner/job-namespaced storage key

#### Scenario: Keep rasterization metadata separate from review manifests
- **WHEN** rasterization writes page artifacts and their index
- **THEN** it does not write OCR text, detected PII, page manifests, or user-selected redaction regions

### Requirement: Rasterization remains memory bounded
The analysis worker SHALL rasterize and persist page artifacts sequentially so
implementation does not need to hold all rendered pages in memory at once.

#### Scenario: Process PDF pages sequentially
- **WHEN** rasterizing a multi-page PDF source
- **THEN** the worker renders and writes each page artifact independently before proceeding to the next page

### Requirement: Rasterization failures are safe permanent failures
The analysis worker SHALL classify post-validation rasterization failures as
safe permanent processing failures.

#### Scenario: Persist safe failure on rasterization error
- **WHEN** source validation succeeds but rasterization fails before all page artifacts are produced
- **THEN** the worker transitions the job to `failed` with safe failure code `processing_failed`

#### Scenario: Avoid downstream artifacts after rasterization failure
- **WHEN** rasterization fails
- **THEN** the worker does not write OCR output, detected PII, page manifests, or user-selected redaction regions
