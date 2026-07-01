# Graph Report - redact-all-the-things  (2026-07-02)

## Corpus Check
- 89 files · ~46,244 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1223 nodes · 2705 edges · 84 communities (75 shown, 9 thin omitted)
- Extraction: 61% EXTRACTED · 39% INFERRED · 0% AMBIGUOUS · INFERRED: 1056 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `174d05e4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Project Architecture|Project Architecture]]
- [[_COMMUNITY_Technical Scope|Technical Scope]]
- [[_COMMUNITY_Working Agreement|Working Agreement]]
- [[_COMMUNITY_Governance Specification|Governance Specification]]
- [[_COMMUNITY_OpenSpec Change Lifecycle|OpenSpec Change Lifecycle]]
- [[_COMMUNITY_Archived Governance Requirements|Archived Governance Requirements]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_OpenSpec Onboarding|OpenSpec Onboarding]]
- [[_COMMUNITY_Bootstrap Execution|Bootstrap Execution]]
- [[_COMMUNITY_Security Reporting|Security Reporting]]
- [[_COMMUNITY_Governance Design|Governance Design]]
- [[_COMMUNITY_OpenSpec Exploration|OpenSpec Exploration]]
- [[_COMMUNITY_AWS System Architecture|AWS System Architecture]]
- [[_COMMUNITY_Governance Proposal|Governance Proposal]]
- [[_COMMUNITY_Governance ADR|Governance ADR]]
- [[_COMMUNITY_MADR Template|MADR Template]]
- [[_COMMUNITY_Contribution Workflow|Contribution Workflow]]
- [[_COMMUNITY_Pull Request Checklist|Pull Request Checklist]]
- [[_COMMUNITY_Repository Linting|Repository Linting]]
- [[_COMMUNITY_Bootstrap Decisions|Bootstrap Decisions]]
- [[_COMMUNITY_ADR Index|ADR Index]]
- [[_COMMUNITY_Documentation Home|Documentation Home]]
- [[_COMMUNITY_Feature Requests|Feature Requests]]
- [[_COMMUNITY_Dependency Updates|Dependency Updates]]
- [[_COMMUNITY_OpenSpec Apply|OpenSpec Apply]]
- [[_COMMUNITY_OpenSpec Archive|OpenSpec Archive]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]

## God Nodes (most connected - your core abstractions)
1. `Job` - 112 edges
2. `SourceType` - 103 edges
3. `PageManifest` - 99 edges
4. `JobStatus` - 97 edges
5. `FailureCode` - 88 edges
6. `RedactionRegion` - 73 edges
7. `RegionSource` - 54 edges
8. `ControlPlaneService` - 50 edges
9. `ValidatedSource` - 46 edges
10. `RenderedPage` - 41 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `Job` --uses--> `ValidatedSource`  [INFERRED]
  tests/worker/test_rasterization.py → src/redact_api/worker.py
- `SourceType` --uses--> `ValidatedSource`  [INFERRED]
  tests/worker/test_rasterization.py → src/redact_api/worker.py
- `Job` --uses--> `ValidatedSource`  [INFERRED]
  tests/worker/test_validation.py → src/redact_api/worker.py

## Import Cycles
- 1-file cycle: `src/redact_api/worker.py -> src/redact_api/worker.py`
- 1-file cycle: `src/redact_api/domain.py -> src/redact_api/domain.py`
- 1-file cycle: `src/redact_api/services.py -> src/redact_api/services.py`
- 1-file cycle: `src/redact_api/http.py -> src/redact_api/http.py`
- 1-file cycle: `tests/services/test_control_plane.py -> tests/services/test_control_plane.py`

## Hyperedges (group relationships)
- **Repository quality enforcement** — agents_definition_of_done, repository_governance_spec_automated_quality, workflows_quality_quality_workflow, pre_commit_config_pre_commit_checks [INFERRED 0.95]
- **Versioned documentation delivery** — agents_documentation_as_code, repository_governance_spec_published_documentation, workflows_pages_strict_mkdocs_build, workflows_pages_github_pages_deployment [INFERRED 0.95]
- **Tracked knowledge asset lifecycle** — agents_tracked_knowledge_assets, agents_graphify_workflow, repository_governance_spec_tracked_assets, 2026_06_14_gh_1_bootstrap_governance_tasks_completed_bootstrap [INFERRED 0.85]

## Communities (84 total, 9 thin omitted)

### Community 0 - "Project Architecture"
Cohesion: 0.22
Nodes (11): 24-hour job retention, Assisted File Redaction technical scope, Official AWS ECS regional price index, Mandatory human review, Normalized redaction regions, Optimistic page-manifest versioning, Assisted redaction application, GLiNER2 (+3 more)

### Community 1 - "Technical Scope"
Cohesion: 0.06
Nodes (126): AwsBatchSubmitter, BaseModel, test_permanent_failures_are_not_retryable(), test_retryable_failures_select_the_worker_mode(), DynamoJobRepository, FastAPI, Image, LookupError (+118 more)

### Community 2 - "Working Agreement"
Cohesion: 0.17
Nodes (16): Repository governance proposal, Repository governance capability, Completed governance bootstrap tasks, Archived repository governance requirements, Automated pull request quality requirement, Protected main workflow requirement, Published documentation requirement, Tracked agent knowledge assets requirement (+8 more)

### Community 3 - "Governance Specification"
Cohesion: 0.06
Nodes (86): Any, datetime, OcrLine, PageArtifact, PiiEntity, analyze_source(), _build_ocr_page_text(), _clamp_region() (+78 more)

### Community 4 - "OpenSpec Change Lifecycle"
Cohesion: 0.12
Nodes (22): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+14 more)

### Community 5 - "Archived Governance Requirements"
Cohesion: 0.08
Nodes (43): FailureCode, PageArtifactIndex, Gliner2PiiDetector, PaddleOcrEngine, Tunable validation limits loaded from YAML., Raised when source validation maps to a safe failure code., Validate source bytes before any analysis artifact can be created., GLiNER2 adapter for the worker image runtime. (+35 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (38): 10. Acceptance Criteria, 11. Principal Risks, 12. References, 1. Objective, 2. Scope, 3. Functional Requirements, 4. System Architecture, 5. Core Data Model (+30 more)

### Community 7 - "OpenSpec Onboarding"
Cohesion: 0.10
Nodes (30): _image_to_rendered_page(), page_artifact_index_key(), page_artifact_key(), RasterizationError, rasterize_source(), Tunable rasterization settings., Persist one PNG page artifact., Persist the JSON page-artifact index. (+22 more)

### Community 8 - "Bootstrap Execution"
Cohesion: 0.05
Nodes (36): Job Contracts Specification, Purpose, Requirements, Requirement: Job status lifecycle, Requirement: Optimistic job updates, Requirement: Optimistic page-manifest persistence, Requirement: Ownership and access expiry, Requirement: Page manifest contract (+28 more)

### Community 9 - "Security Reporting"
Cohesion: 0.06
Nodes (34): Control-Plane API Specification, Purpose, Requirements, Requirement: Authenticated control-plane boundary, Requirement: Authorize completed download, Requirement: Complete upload and submit analysis, Requirement: Confirm export and submit rendering, Requirement: Create job and authorize upload (+26 more)

### Community 10 - "Governance Design"
Cohesion: 0.11
Nodes (26): make_job(), test_expiry_is_exact_at_the_deadline(), test_invalid_transition_is_rejected(), test_normal_transitions_increment_version(), test_only_expired_jobs_can_transition_to_expired(), test_processing_can_fail(), test_retry_transition_clears_failure_code(), test_submission_token_is_stable_for_the_transition_version() (+18 more)

### Community 11 - "OpenSpec Exploration"
Cohesion: 0.06
Nodes (32): ADDED Requirements, Requirement: Authenticated control-plane boundary, Requirement: Authorize completed download, Requirement: Complete upload and submit analysis, Requirement: Confirm export and submit rendering, Requirement: Create job and authorize upload, Requirement: List and retrieve jobs, Requirement: Locally testable service boundaries (+24 more)

### Community 12 - "AWS System Architecture"
Cohesion: 0.06
Nodes (30): ADDED Requirements, Requirement: Job status lifecycle, Requirement: Optimistic job updates, Requirement: Optimistic page-manifest persistence, Requirement: Ownership and access expiry, Requirement: Page manifest contract, Requirement: Persistent job record, Requirement: Privacy-preserving persistence (+22 more)

### Community 13 - "Governance Proposal"
Cohesion: 0.07
Nodes (27): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+19 more)

### Community 14 - "Governance ADR"
Cohesion: 0.09
Nodes (21): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+13 more)

### Community 15 - "MADR Template"
Cohesion: 0.11
Nodes (17): Requirement: PII mapping failures are safe permanent failures, Requirement: PII spans become normalized redaction regions, Requirement: Worker creates review manifests from detected regions, Requirement: Worker detects PII from OCR artifacts, Scenario: Approximate substring geometry, Scenario: Avoid partial downstream review state, Scenario: Avoid raw detected values in regions, Scenario: Clamp region geometry (+9 more)

### Community 16 - "Contribution Workflow"
Cohesion: 0.12
Nodes (16): Requirement: PII mapping failures are safe permanent failures, Requirement: PII spans become normalized redaction regions, Requirement: Worker creates review manifests from detected regions, Requirement: Worker detects PII from OCR artifacts, Scenario: Approximate substring geometry, Scenario: Avoid partial downstream review state, Scenario: Avoid raw detected values in regions, Scenario: Clamp region geometry (+8 more)

### Community 17 - "Pull Request Checklist"
Cohesion: 0.12
Nodes (16): Requirement: Rejected validation produces no analysis artifacts, Requirement: Worker rejects invalid source content safely, Requirement: Worker validates supported source content, Scenario: Accept valid JPEG content, Scenario: Accept valid PDF content, Scenario: Accept valid PNG content, Scenario: Preserve storage on validation failure, Scenario: Reject encrypted PDF content (+8 more)

### Community 19 - "Bootstrap Decisions"
Cohesion: 0.50
Nodes (4): Bootstrap governance architecture, Reproducible uv documentation toolchain, Required Quality workflow design, Spec-driven bootstrap governance change

### Community 20 - "ADR Index"
Cohesion: 0.12
Nodes (15): Requirement: OCR artifacts preserve page text and geometry, Requirement: OCR failures are safe permanent failures, Requirement: OCR runtime is packaged for offline worker execution, Requirement: Worker extracts OCR text from page artifacts, Scenario: Avoid downstream artifacts after OCR failure, Scenario: Extract OCR for each page artifact, Scenario: Keep deployment infrastructure out of OCR extraction, Scenario: Keep OCR after rasterization (+7 more)

### Community 21 - "Documentation Home"
Cohesion: 0.28
Nodes (15): clock(), create_ready_manifest(), service(), set_status(), test_create_list_get_ownership_and_exact_expiry(), test_create_rejects_invalid_sizes(), test_download_requires_complete_existing_output(), test_export_requires_acknowledgement_and_is_idempotent() (+7 more)

### Community 22 - "Feature Requests"
Cohesion: 0.67
Nodes (3): Feature request issue template, Observable success, Scope boundaries

### Community 24 - "OpenSpec Apply"
Cohesion: 0.13
Nodes (14): Context, Decisions, Enforce lifecycle transitions with compare-and-set updates, Goals / Non-Goals, Keep the initial HTTP surface task-oriented, Migration Plan, Open Questions, Risks / Trade-offs (+6 more)

### Community 25 - "OpenSpec Archive"
Cohesion: 0.13
Nodes (14): Requirement: Rejected validation produces no analysis artifacts, Requirement: Worker rejects invalid source content safely, Requirement: Worker validates supported source content, Scenario: Accept valid JPEG content, Scenario: Accept valid PDF content, Scenario: Accept valid PNG content, Scenario: Preserve storage on validation failure, Scenario: Reject encrypted PDF content (+6 more)

### Community 26 - "Community 26"
Cohesion: 0.13
Nodes (14): Requirement: OCR artifacts preserve page text and geometry, Requirement: OCR failures are safe permanent failures, Requirement: OCR runtime is packaged for offline worker execution, Requirement: Worker extracts OCR text from page artifacts, Scenario: Avoid downstream artifacts after OCR failure, Scenario: Extract OCR for each page artifact, Scenario: Keep deployment infrastructure out of OCR extraction, Scenario: Keep OCR after rasterization (+6 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (12): Privacy-preserving logging, Bug report issue template, Reproducible bug reports, Synthetic or sanitized bug fixtures, Issue template configuration, GitHub private vulnerability reporting, Coordinated vulnerability disclosure, Reporting a vulnerability (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.14
Nodes (12): 1. Reproducible Tooling, 2. Documentation, 3. GitHub Repository Files, 4. Knowledge Graph and Local Verification, 5. GitHub Publication, 6. Completion, Contributing, Documentation (+4 more)

### Community 30 - "Community 30"
Cohesion: 0.14
Nodes (13): Requirement: Page artifact metadata preserves downstream ordering, Requirement: Rasterization failures are safe permanent failures, Requirement: Rasterization remains memory bounded, Requirement: Worker rasterizes accepted sources into page artifacts, Scenario: Avoid downstream artifacts after rasterization failure, Scenario: Keep rasterization metadata separate from review manifests, Scenario: Persist safe failure on rasterization error, Scenario: Process PDF pages sequentially (+5 more)

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (12): Requirement: Page artifact metadata preserves downstream ordering, Requirement: Rasterization failures are safe permanent failures, Requirement: Rasterization remains memory bounded, Requirement: Worker rasterizes accepted sources into page artifacts, Scenario: Avoid downstream artifacts after rasterization failure, Scenario: Keep rasterization metadata separate from review manifests, Scenario: Persist safe failure on rasterization error, Scenario: Process PDF pages sequentially (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (11): Configure GitHub as part of bootstrap, Context, Decisions, Goals / Non-Goals, Keep agent and Graphify assets versioned, Migration Plan, Open Questions, Publish documentation from `docs/` (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.17
Nodes (11): Context, Decisions, Goals / Non-Goals, Keep processing sequential and writer-driven, Migration Plan, Normalize all page artifacts to PNG, Open Questions, Risks / Trade-offs (+3 more)

### Community 34 - "Community 34"
Cohesion: 0.17
Nodes (11): Context, Decisions, Goals / Non-Goals, Keep OCR artifacts separate from manifests, Migration Plan, Open Questions, Package models in the worker image, Persist one JSON artifact per page (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.17
Nodes (11): Approximate substring geometry from line polygons, Context, Create review manifests directly, Decisions, Goals / Non-Goals, Migration Plan, Open Questions, Persist safe categories, not raw detected values (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.18
Nodes (10): Context, Decisions, Encode gates in milestone issues, Goals / Non-Goals, Keep the versioned roadmap authoritative, Limit solo work in progress, Migration Plan, Open Questions (+2 more)

### Community 38 - "Community 38"
Cohesion: 0.18
Nodes (10): Add a small worker package that consumes shared contracts, Context, Decisions, Goals / Non-Goals, Keep artifact prevention explicit, Migration Plan, Open Questions, Risks / Trade-offs (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.33
Nodes (10): make_job(), test_failed_job_requires_a_safe_failure_code(), test_job_accepts_the_persistent_contract(), test_job_rejects_foreign_object_namespaces(), test_job_rejects_invalid_limits(), test_job_rejects_progress_beyond_page_count(), test_job_rejects_unknown_fields(), test_job_rejects_unsupported_source_types() (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.40
Nodes (9): client(), create_job(), create_manifest(), set_status(), test_create_list_retrieve_and_non_disclosing_not_found(), test_identity_validation_and_request_validation(), test_openapi_contains_the_public_contract(), test_upload_complete_export_retry_manifest_and_download_routes() (+1 more)

### Community 41 - "Community 41"
Cohesion: 0.20
Nodes (9): MODIFIED Requirements, Requirement: Managed roadmap, Requirement: Repository contribution metadata, Scenario: Contributor creates an implementation slice, Scenario: Contributor proposes a change, Scenario: Implementation slice completes, Scenario: Next implementation slice is selected, Scenario: Parent epic tracks child work (+1 more)

### Community 42 - "Community 42"
Cohesion: 0.22
Nodes (8): Architecture decisions, Change lifecycle, Development workflow, Documentation requirements, Install tooling, Local validation, Prerequisites, Work item model

### Community 43 - "Community 43"
Cohesion: 0.17
Nodes (11): Change Workflow, Collaboration Platform, Definition of Done, Engineering Guidance, Git Conventions, graphify, Project Working Agreement, Tooling (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.22
Nodes (8): #6 PDF and image analysis worker, #8 React frontend and authentication shell, Contract ownership, Delivery policy, Dependency flow, Epic decomposition, Implementation roadmap, Sequence

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 46 - "Community 46"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 48 - "Community 48"
Cohesion: 0.29
Nodes (6): 1. Application Setup, 2. Domain Contracts, 3. Application Services, 4. HTTP API, 5. AWS Persistence Integration, 6. Documentation and Verification

### Community 49 - "Community 49"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 50 - "Community 50"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 51 - "Community 51"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 52 - "Community 52"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 53 - "Community 53"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 54 - "Community 54"
Cohesion: 0.29
Nodes (6): ADR 0001: Adopt documentation-as-code and GitHub governance, Consequences, Considered alternatives, Context, Decision, References

### Community 55 - "Community 55"
Cohesion: 0.29
Nodes (6): ADR 0002: Define control-plane boundaries and persistence, Consequences, Considered alternatives, Context, Decision, References

### Community 56 - "Community 56"
Cohesion: 0.29
Nodes (6): ADR NNNN: Decision title, Consequences, Considered alternatives, Context, Decision, References

### Community 57 - "Community 57"
Cohesion: 0.29
Nodes (6): Analysis worker, OCR extraction, PII detection and region mapping, Rasterization, Safe failures, Source validation

### Community 58 - "Community 58"
Cohesion: 0.29
Nodes (6): Authentication, Control-plane API, Endpoints, Local development, Persistence, Runtime configuration

### Community 59 - "Community 59"
Cohesion: 0.33
Nodes (5): Context, Decisions, Goals / Non-Goals, Migration Plan, Risks / Trade-offs

### Community 60 - "Community 60"
Cohesion: 0.33
Nodes (5): 1. Planning Artifacts, 2. Workflow Documentation, 3. Issue Templates, 4. Seed GitHub Issues, 5. Validation and Archival

### Community 61 - "Community 61"
Cohesion: 0.33
Nodes (5): 1. Test Fixtures, 2. Worker Validation Tests, 3. Worker Validation Implementation, 4. Contract and Documentation Updates, 5. Verification

### Community 62 - "Community 62"
Cohesion: 0.33
Nodes (5): 1. Test Fixtures, 2. Worker Rasterization Tests, 3. Worker Rasterization Implementation, 4. Documentation Updates, 5. Verification

### Community 63 - "Community 63"
Cohesion: 0.33
Nodes (5): 1. OpenSpec and Fixtures, 2. Worker OCR Tests, 3. Worker OCR Implementation, 4. Worker Runtime Packaging, 5. Documentation and Verification

### Community 64 - "Community 64"
Cohesion: 0.33
Nodes (5): 1. OpenSpec and Fixtures, 2. Worker PII Tests, 3. Worker PII Implementation, 4. Worker Runtime Packaging, 5. Documentation and Verification

### Community 65 - "Community 65"
Cohesion: 0.33
Nodes (5): Before starting, Contributing, Local checks, Pull requests, Workflow

### Community 66 - "Community 66"
Cohesion: 0.33
Nodes (5): Documentation and architecture, OpenSpec, Security and privacy, Summary, Validation

### Community 67 - "Community 67"
Cohesion: 0.47
Nodes (5): make_job(), make_manifest(), test_dynamodb_round_trip_listing_ttl_and_conflict(), test_recording_batch_fake_is_idempotent(), test_s3_presigning_objects_and_manifest_conflicts()

### Community 68 - "Community 68"
Cohesion: 0.33
Nodes (5): MODIFIED Requirements, Requirement: Managed roadmap, Scenario: Roadmap order is published, Scenario: Milestone completes, Scenario: Next milestone is selected

### Community 69 - "Community 69"
Cohesion: 0.33
Nodes (5): ADDED Requirements, Requirement: Permanent worker validation failures, Scenario: Persist unsupported content safely, Scenario: Persist validation failure safely, Scenario: Reject retry for permanent validation failures

### Community 70 - "Community 70"
Cohesion: 0.60
Nodes (4): main(), Path, Strip execution output from Jupyter notebooks before commit., strip_notebook()

### Community 71 - "Community 71"
Cohesion: 0.50
Nodes (3): 1. Versioned Roadmap, 2. GitHub Roadmap Metadata, 3. Verification and Completion

### Community 72 - "Community 72"
Cohesion: 0.50
Nodes (3): Architecture decision records, Creating a record, Records

### Community 73 - "Community 73"
Cohesion: 0.50
Nodes (3): Project principles, Redact All The Things, Start here

### Community 74 - "Community 74"
Cohesion: 0.83
Nodes (3): load(), test_shared_job_fixtures_match_the_contract(), test_shared_manifest_and_worker_fixtures_match_the_contract()

### Community 92 - "Community 92"
Cohesion: 0.40
Nodes (5): ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Documentation as Code

### Community 93 - "Community 93"
Cohesion: 0.40
Nodes (5): Private AWS architecture, Checkpoint recovery, AWS Batch Fargate Spot processing, Scale-to-zero cost controls, Serverless control plane

## Knowledge Gaps
- **491 isolated node(s):** `Source validation`, `Rasterization`, `OCR extraction`, `PII detection and region mapping`, `Safe failures` (+486 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Job` connect `Technical Scope` to `Governance Design`, `Governance Specification`, `Archived Governance Requirements`, `OpenSpec Onboarding`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `PageManifest` connect `Technical Scope` to `Governance Specification`, `Archived Governance Requirements`, `OpenSpec Onboarding`, `Community 40`, `Governance Design`, `Documentation Home`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `SourceType` connect `Technical Scope` to `Governance Specification`, `Archived Governance Requirements`, `OpenSpec Onboarding`, `Governance Design`, `Documentation Home`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 105 inferred relationships involving `Job` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`Job` has 105 INFERRED edges - model-reasoned connections that need verification._
- **Are the 100 inferred relationships involving `SourceType` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`SourceType` has 100 INFERRED edges - model-reasoned connections that need verification._
- **Are the 94 inferred relationships involving `PageManifest` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`PageManifest` has 94 INFERRED edges - model-reasoned connections that need verification._
- **Are the 92 inferred relationships involving `JobStatus` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`JobStatus` has 92 INFERRED edges - model-reasoned connections that need verification._