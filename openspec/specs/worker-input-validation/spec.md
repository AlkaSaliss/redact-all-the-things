# Worker Input Validation Specification

## Purpose

Define the analysis worker validation boundary for uploaded PDF, JPEG, and PNG
source content before rasterization, OCR, PII detection, or artifact creation.

## Requirements

### Requirement: Worker validates supported source content
The analysis worker SHALL validate uploaded PDF, JPEG, and PNG source content
before rasterization, OCR, PII detection, or artifact creation begins.

#### Scenario: Accept valid PDF content
- **WHEN** an analyze worker receives a source object whose job source type is `pdf` and whose bytes decode as an unencrypted PDF with 1 through 200 pages
- **THEN** validation succeeds and returns the PDF page count for later analysis

#### Scenario: Accept valid JPEG content
- **WHEN** an analyze worker receives a source object whose job source type is `jpeg` and whose bytes decode as a JPEG image with positive dimensions and no more than 50,000,000 pixels
- **THEN** validation succeeds and returns a one-page image source for later analysis

#### Scenario: Accept valid PNG content
- **WHEN** an analyze worker receives a source object whose job source type is `png` and whose bytes decode as a PNG image with positive dimensions and no more than 50,000,000 pixels
- **THEN** validation succeeds and returns a one-page image source for later analysis

### Requirement: Worker rejects invalid source content safely
The analysis worker SHALL reject unsupported formats, malformed files, encrypted
PDFs, files above 100 MB, PDFs above 200 pages, and images above 50,000,000
decoded pixels with safe permanent failure codes.

Validation limits SHALL be loaded from YAML configuration so tests and local
workers can use smaller limits without large source artifacts.

#### Scenario: Reject source type mismatch
- **WHEN** an analyze worker receives source bytes whose file signature or decoded content does not match the job source type
- **THEN** validation fails with safe failure code `unsupported_content`

#### Scenario: Reject malformed source content
- **WHEN** an analyze worker receives a declared PDF, JPEG, or PNG source whose bytes cannot be decoded as that format
- **THEN** validation fails with safe failure code `validation_failed`

#### Scenario: Reject encrypted PDF content
- **WHEN** an analyze worker receives a PDF source that requires decryption before page inspection
- **THEN** validation fails with safe failure code `validation_failed`

#### Scenario: Reject oversized source content
- **WHEN** an analyze worker receives a source object larger than 100 MB
- **THEN** validation fails with safe failure code `validation_failed`

#### Scenario: Reject over-limit PDF page count
- **WHEN** an analyze worker receives a valid PDF source with more than 200 pages
- **THEN** validation fails with safe failure code `validation_failed`

#### Scenario: Reject over-limit image pixel count
- **WHEN** an analyze worker receives a valid JPEG or PNG source whose decoded width multiplied by height exceeds 50,000,000 pixels
- **THEN** validation fails with safe failure code `validation_failed`

### Requirement: Rejected validation produces no analysis artifacts
The analysis worker SHALL fail validation before writing previews, OCR output,
detected PII, analysis artifacts, or page manifests.

#### Scenario: Preserve storage on validation failure
- **WHEN** source validation fails for an analyze worker request
- **THEN** the worker persists only the safe job failure state and does not write previews, OCR text, detected PII, analysis artifacts, or page manifests
