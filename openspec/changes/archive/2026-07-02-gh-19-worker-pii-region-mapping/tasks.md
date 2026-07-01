## 1. OpenSpec and Fixtures

- [x] 1.1 Add the worker PII region mapping capability spec with detection, geometry, manifest, packaging, and failure requirements.
- [x] 1.2 Add representative non-sensitive PII mapping fixtures if useful for contract documentation.

## 2. Worker PII Tests

- [x] 2.1 Write deterministic tests for synthetic OCR pages covering email, phone, person/name, ID, credential, and address-like labels.
- [x] 2.2 Write geometry tests for substring spans, multiple entities in one line, clamping near edges, and out-of-bounds prevention.
- [x] 2.3 Write contract tests proving generated `RedactionRegion` and `PageManifest` objects validate without raw detected values.
- [x] 2.4 Write analyze-path tests proving PII runs after OCR, creates manifests only after successful detection, and persists `processing_failed` on PII errors.

## 3. Worker PII Implementation

- [x] 3.1 Add detector result, detector protocol, manifest writer protocol, and PII mapping error contracts.
- [x] 3.2 Implement GLiNER2 adapter for `fastino/gliner2-privacy-filter-PII-multi` using threshold `0.5` and all supported labels.
- [x] 3.3 Implement span-to-region mapping from OCR block offsets and normalized line polygons.
- [x] 3.4 Implement page manifest creation with automatic suggestions selected by default.
- [x] 3.5 Integrate PII mapping into `analyze_source` after successful OCR extraction and before later downstream hooks.
- [x] 3.6 Normalize detector, geometry, and manifest write errors into safe `processing_failed` job failures.

## 4. Worker Runtime Packaging

- [x] 4.1 Add GLiNER2/model runtime dependencies using `uv`.
- [x] 4.2 Update worker image packaging so model assets are bundled for offline job execution.
- [x] 4.3 Extend the local worker smoke script to run OCR, PII mapping, and manifest creation without printing raw OCR or PII values.

## 5. Documentation and Verification

- [x] 5.1 Update worker architecture documentation with the PII detection, region mapping, manifest, and packaging behavior.
- [x] 5.2 Run focused worker/domain/control-plane manifest tests.
- [x] 5.3 Run strict OpenSpec validation for `gh-19-worker-pii-region-mapping`.
- [x] 5.4 Run the strict MkDocs build.
- [x] 5.5 Run `graphify update .` after source or architecture documentation changes.
