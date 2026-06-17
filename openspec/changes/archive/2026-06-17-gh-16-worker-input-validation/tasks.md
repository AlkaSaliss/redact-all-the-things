## 1. Test Fixtures

- [x] 1.1 Add minimal non-sensitive PDF, JPEG, and PNG fixtures for accepted validation paths.
- [x] 1.2 Add invalid fixture inputs for signature mismatch, malformed content, encrypted PDF, oversized source metadata, over-limit image pixel count, and over-limit PDF page count using small test-config limits.

## 2. Worker Validation Tests

- [x] 2.1 Write failing worker tests that accept valid PDF, JPEG, and PNG sources and return the expected page count.
- [x] 2.2 Write failing worker tests that map signature/type mismatches to `unsupported_content`.
- [x] 2.3 Write failing worker tests that map malformed, encrypted, oversized, over-pixel-limit, and over-page-limit sources to `validation_failed`.
- [x] 2.4 Write failing tests proving rejected validation does not call any analysis artifact writer.

## 3. Worker Validation Implementation

- [x] 3.1 Add the worker validation module, YAML config loader, and result types using shared source-type and failure-code contracts.
- [x] 3.2 Implement YAML-backed size, signature, PDF page-count, PDF encryption, image decode, and 50,000,000-pixel image limit validation.
- [x] 3.3 Normalize parser and validation errors into safe failure codes without exposing file content or sensitive parser details.
- [x] 3.4 Add the validation-only analyze entry point that persists `failed` jobs with the safe failure code before rasterization, OCR, PII detection, previews, analysis artifacts, or page manifests.

## 4. Contract and Documentation Updates

- [x] 4.1 Add or update contract tests proving `validation_failed` and `unsupported_content` are permanent, non-retryable worker failures.
- [x] 4.2 Update worker architecture documentation with the validation-only boundary and safe failure behavior.
- [x] 4.3 Document the 50,000,000-pixel JPEG/PNG validation limit and any parser dependency added for PDF or image validation.

## 5. Verification

- [x] 5.1 Run the focused worker and domain tests for validation and failure-code behavior.
- [x] 5.2 Run strict OpenSpec validation for `gh-16-worker-input-validation`.
- [x] 5.3 Run the strict MkDocs build.
- [x] 5.4 Run `graphify update .` because source or architecture documentation changes are expected.
