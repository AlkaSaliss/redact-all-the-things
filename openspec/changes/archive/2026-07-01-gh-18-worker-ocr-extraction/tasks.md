## 1. OpenSpec and Fixtures

- [x] 1.1 Add the worker OCR extraction capability spec with page-ordering, artifact-shape, packaging, and failure requirements.
- [x] 1.2 Add an OCR JSON contract fixture that documents the per-page artifact shape.

## 2. Worker OCR Tests

- [x] 2.1 Write deterministic worker tests proving OCR runs for each raster page in page-number order.
- [x] 2.2 Write tests proving per-page OCR JSON artifacts contain page metadata, ordered text, line confidence, normalized polygons, and offsets.
- [x] 2.3 Write tests proving OCR artifacts stay separate from PII, page manifests, user regions, and job metadata updates.
- [x] 2.4 Write tests proving OCR failures persist `processing_failed` and stop downstream hooks.

## 3. Worker OCR Implementation

- [x] 3.1 Add OCR result, page text, engine, and artifact-writer contracts.
- [x] 3.2 Implement OCR artifact key generation and JSON serialization.
- [x] 3.3 Implement OCR extraction over a `PageArtifactIndex` using page artifact bytes supplied by the storage boundary.
- [x] 3.4 Integrate OCR into the analyze path after successful rasterization and before later PII hooks.
- [x] 3.5 Add the embedded PaddleOCR adapter configured for PP-OCRv6 medium with text-line orientation enabled and heavier preprocessing disabled.
- [x] 3.6 Normalize OCR engine, decode, and write errors into safe `processing_failed` job failures.

## 4. Worker Runtime Packaging

- [x] 4.1 Add a minimal non-root worker Dockerfile for the OCR runtime.
- [x] 4.2 Ensure the Dockerfile prepares local PP-OCRv6 medium model artifact paths for runtime use without job-time downloads.
- [x] 4.3 Document that AWS Batch infrastructure and ECR publishing remain out of scope.

## 5. Documentation and Verification

- [x] 5.1 Update worker architecture documentation with the OCR artifact contract, selected PaddleOCR model/runtime mode, and opt-in sample smoke-test role.
- [x] 5.2 Run focused worker OCR/rasterization tests.
- [x] 5.3 Run strict OpenSpec validation for `gh-18-worker-ocr-extraction`.
- [x] 5.4 Run the strict MkDocs build.
- [x] 5.5 Run `graphify update .` after source or architecture documentation changes.
