## 1. Test Fixtures

- [ ] 1.1 Add minimal non-sensitive PDF fixtures that exercise multi-page rasterization ordering.
- [ ] 1.2 Add minimal JPEG and PNG fixtures that exercise one-page image normalization.
- [ ] 1.3 Add renderer or writer test doubles for sequential processing and failure-path coverage without large source artifacts.

## 2. Worker Rasterization Tests

- [ ] 2.1 Write failing worker tests proving multi-page PDFs produce ordered PNG artifacts numbered `1` through page count.
- [ ] 2.2 Write failing worker tests proving JPEG and PNG inputs each produce exactly one PNG page artifact.
- [ ] 2.3 Write failing tests proving the page-artifact index records page number, dimensions, format `png`, and owner/job-namespaced storage keys.
- [ ] 2.4 Write failing tests proving rasterization renders and writes pages sequentially instead of returning all page bytes at once.
- [ ] 2.5 Write failing tests proving post-validation rasterization failures persist `processing_failed` and do not write OCR, PII, page-manifest, or user-region artifacts.

## 3. Worker Rasterization Implementation

- [ ] 3.1 Add `pypdfium2` and any minimal image support needed to render PDF pages and normalize JPEG/PNG sources to PNG bytes.
- [ ] 3.2 Add rasterization result and page-artifact metadata types using shared source-type, job, and storage namespace contracts.
- [ ] 3.3 Implement fixed-DPI PDF page rasterization that writes one PNG artifact per page in source order.
- [ ] 3.4 Implement JPEG and PNG source normalization into the same one-page PNG artifact contract.
- [ ] 3.5 Implement page-artifact index writing after successful rasterization.
- [ ] 3.6 Integrate rasterization into the analyze path after source validation and before later OCR or PII hooks.
- [ ] 3.7 Normalize renderer/decode exceptions into safe `processing_failed` job failures without exposing file content or parser details.

## 4. Documentation Updates

- [ ] 4.1 Update worker architecture documentation with the rasterization boundary, fixed-DPI PNG artifact contract, and page-artifact index.
- [ ] 4.2 Document that OCR, PII detection, checkpoint/resume behavior, review manifests, and render-mode export remain out of scope for this slice.
- [ ] 4.3 Document the `pypdfium2` dependency and any fixed rasterization limit or DPI configuration added by the implementation.

## 5. Verification

- [ ] 5.1 Run focused worker tests for validation and rasterization behavior.
- [ ] 5.2 Run strict OpenSpec validation for `gh-17-worker-rasterization`.
- [ ] 5.3 Run the strict MkDocs build.
- [ ] 5.4 Run `graphify update .` if implementation or architecture documentation changes are made.
