# Graph Report - redact-all-the-things  (2026-06-18)

## Corpus Check
- 73 files · ~29,835 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 943 nodes · 1799 edges · 72 communities (62 shown, 10 thin omitted)
- Extraction: 66% EXTRACTED · 34% INFERRED · 0% AMBIGUOUS · INFERRED: 606 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1a6fb1a4`
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
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
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
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]

## God Nodes (most connected - your core abstractions)
1. `Job` - 73 edges
2. `SourceType` - 64 edges
3. `JobStatus` - 58 edges
4. `PageManifest` - 56 edges
5. `FailureCode` - 55 edges
6. `ControlPlaneService` - 50 edges
7. `RedactionRegion` - 47 edges
8. `InvalidRequestError` - 41 edges
9. `JobNotFoundError` - 37 edges
10. `ManifestConflictError` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `RecordingJobs` --uses--> `FailureCode`  [INFERRED]
  tests/worker/test_rasterization.py → src/redact_api/domain.py
- `RecordingJobs` --uses--> `Job`  [INFERRED]
  tests/worker/test_rasterization.py → src/redact_api/domain.py
- `RecordingJobs` --uses--> `JobStatus`  [INFERRED]
  tests/worker/test_rasterization.py → src/redact_api/domain.py

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

## Communities (72 total, 10 thin omitted)

### Community 0 - "Project Architecture"
Cohesion: 0.22
Nodes (11): 24-hour job retention, Assisted File Redaction technical scope, Official AWS ECS regional price index, Mandatory human review, Normalized redaction regions, Optimistic page-manifest versioning, Assisted redaction application, GLiNER2 (+3 more)

### Community 1 - "Technical Scope"
Cohesion: 0.07
Nodes (109): set_status(), AwsBatchSubmitter, BaseModel, test_permanent_failures_are_not_retryable(), test_retryable_failures_select_the_worker_mode(), DynamoJobRepository, FastAPI, Image (+101 more)

### Community 2 - "Working Agreement"
Cohesion: 0.17
Nodes (16): Repository governance proposal, Repository governance capability, Completed governance bootstrap tasks, Archived repository governance requirements, Automated pull request quality requirement, Protected main workflow requirement, Published documentation requirement, Tracked agent knowledge assets requirement (+8 more)

### Community 3 - "Governance Specification"
Cohesion: 0.27
Nodes (16): clock(), create_ready_manifest(), service(), set_status(), test_create_list_get_ownership_and_exact_expiry(), test_create_rejects_invalid_sizes(), test_download_requires_complete_existing_output(), test_export_requires_acknowledgement_and_is_idempotent() (+8 more)

### Community 4 - "OpenSpec Change Lifecycle"
Cohesion: 0.12
Nodes (22): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+14 more)

### Community 5 - "Archived Governance Requirements"
Cohesion: 0.06
Nodes (73): Any, datetime, FailureCode, Protocol, analyze_source(), _image_to_rendered_page(), page_artifact_index_key(), page_artifact_key() (+65 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (28): make_job(), test_expiry_is_exact_at_the_deadline(), test_invalid_transition_is_rejected(), test_normal_transitions_increment_version(), test_only_expired_jobs_can_transition_to_expired(), test_processing_can_fail(), test_retry_transition_clears_failure_code(), test_submission_token_is_stable_for_the_transition_version() (+20 more)

### Community 7 - "OpenSpec Onboarding"
Cohesion: 0.05
Nodes (38): 10. Acceptance Criteria, 11. Principal Risks, 12. References, 1. Objective, 2. Scope, 3. Functional Requirements, 4. System Architecture, 5. Core Data Model (+30 more)

### Community 8 - "Bootstrap Execution"
Cohesion: 0.05
Nodes (36): Job Contracts Specification, Purpose, Requirements, Requirement: Job status lifecycle, Requirement: Optimistic job updates, Requirement: Optimistic page-manifest persistence, Requirement: Ownership and access expiry, Requirement: Page manifest contract (+28 more)

### Community 9 - "Security Reporting"
Cohesion: 0.06
Nodes (34): Control-Plane API Specification, Purpose, Requirements, Requirement: Authenticated control-plane boundary, Requirement: Authorize completed download, Requirement: Complete upload and submit analysis, Requirement: Confirm export and submit rendering, Requirement: Create job and authorize upload (+26 more)

### Community 10 - "Governance Design"
Cohesion: 0.06
Nodes (32): ADDED Requirements, Requirement: Authenticated control-plane boundary, Requirement: Authorize completed download, Requirement: Complete upload and submit analysis, Requirement: Confirm export and submit rendering, Requirement: Create job and authorize upload, Requirement: List and retrieve jobs, Requirement: Locally testable service boundaries (+24 more)

### Community 11 - "OpenSpec Exploration"
Cohesion: 0.06
Nodes (30): ADDED Requirements, Requirement: Job status lifecycle, Requirement: Optimistic job updates, Requirement: Optimistic page-manifest persistence, Requirement: Ownership and access expiry, Requirement: Page manifest contract, Requirement: Persistent job record, Requirement: Privacy-preserving persistence (+22 more)

### Community 12 - "AWS System Architecture"
Cohesion: 0.13
Nodes (14): Requirement: Rejected validation produces no analysis artifacts, Requirement: Worker rejects invalid source content safely, Requirement: Worker validates supported source content, Scenario: Accept valid JPEG content, Scenario: Accept valid PDF content, Scenario: Accept valid PNG content, Scenario: Preserve storage on validation failure, Scenario: Reject encrypted PDF content (+6 more)

### Community 13 - "Governance Proposal"
Cohesion: 0.07
Nodes (27): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+19 more)

### Community 14 - "Governance ADR"
Cohesion: 0.09
Nodes (21): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+13 more)

### Community 15 - "MADR Template"
Cohesion: 0.12
Nodes (16): Requirement: Rejected validation produces no analysis artifacts, Requirement: Worker rejects invalid source content safely, Requirement: Worker validates supported source content, Scenario: Accept valid JPEG content, Scenario: Accept valid PDF content, Scenario: Accept valid PNG content, Scenario: Preserve storage on validation failure, Scenario: Reject encrypted PDF content (+8 more)

### Community 16 - "Contribution Workflow"
Cohesion: 0.13
Nodes (14): Context, Decisions, Enforce lifecycle transitions with compare-and-set updates, Goals / Non-Goals, Keep the initial HTTP surface task-oriented, Migration Plan, Open Questions, Risks / Trade-offs (+6 more)

### Community 17 - "Pull Request Checklist"
Cohesion: 0.14
Nodes (12): 1. Reproducible Tooling, 2. Documentation, 3. GitHub Repository Files, 4. Knowledge Graph and Local Verification, 5. GitHub Publication, 6. Completion, Contributing, Documentation (+4 more)

### Community 19 - "Bootstrap Decisions"
Cohesion: 0.50
Nodes (4): Bootstrap governance architecture, Reproducible uv documentation toolchain, Required Quality workflow design, Spec-driven bootstrap governance change

### Community 20 - "ADR Index"
Cohesion: 0.17
Nodes (11): Configure GitHub as part of bootstrap, Context, Decisions, Goals / Non-Goals, Keep agent and Graphify assets versioned, Migration Plan, Open Questions, Publish documentation from `docs/` (+3 more)

### Community 21 - "Documentation Home"
Cohesion: 0.18
Nodes (10): Context, Decisions, Encode gates in milestone issues, Goals / Non-Goals, Keep the versioned roadmap authoritative, Limit solo work in progress, Migration Plan, Open Questions (+2 more)

### Community 22 - "Feature Requests"
Cohesion: 0.67
Nodes (3): Feature request issue template, Observable success, Scope boundaries

### Community 24 - "OpenSpec Apply"
Cohesion: 0.18
Nodes (10): Add a small worker package that consumes shared contracts, Context, Decisions, Goals / Non-Goals, Keep artifact prevention explicit, Migration Plan, Open Questions, Risks / Trade-offs (+2 more)

### Community 25 - "OpenSpec Archive"
Cohesion: 0.33
Nodes (10): make_job(), test_failed_job_requires_a_safe_failure_code(), test_job_accepts_the_persistent_contract(), test_job_rejects_foreign_object_namespaces(), test_job_rejects_invalid_limits(), test_job_rejects_progress_beyond_page_count(), test_job_rejects_unknown_fields(), test_job_rejects_unsupported_source_types() (+2 more)

### Community 26 - "Community 26"
Cohesion: 0.83
Nodes (3): load(), test_shared_job_fixtures_match_the_contract(), test_shared_manifest_and_worker_fixtures_match_the_contract()

### Community 28 - "Community 28"
Cohesion: 0.44
Nodes (8): client(), create_job(), create_manifest(), test_create_list_retrieve_and_non_disclosing_not_found(), test_identity_validation_and_request_validation(), test_openapi_contains_the_public_contract(), test_upload_complete_export_retry_manifest_and_download_routes(), TestClient

### Community 29 - "Community 29"
Cohesion: 0.20
Nodes (9): MODIFIED Requirements, Requirement: Managed roadmap, Requirement: Repository contribution metadata, Scenario: Contributor creates an implementation slice, Scenario: Contributor proposes a change, Scenario: Implementation slice completes, Scenario: Next implementation slice is selected, Scenario: Parent epic tracks child work (+1 more)

### Community 30 - "Community 30"
Cohesion: 0.22
Nodes (8): Architecture decisions, Change lifecycle, Development workflow, Documentation requirements, Install tooling, Local validation, Prerequisites, Work item model

### Community 31 - "Community 31"
Cohesion: 0.22
Nodes (8): #6 PDF and image analysis worker, #8 React frontend and authentication shell, Contract ownership, Delivery policy, Dependency flow, Epic decomposition, Implementation roadmap, Sequence

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 33 - "Community 33"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 34 - "Community 34"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 36 - "Community 36"
Cohesion: 0.29
Nodes (6): 1. Application Setup, 2. Domain Contracts, 3. Application Services, 4. HTTP API, 5. AWS Persistence Integration, 6. Documentation and Verification

### Community 37 - "Community 37"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): ADR 0001: Adopt documentation-as-code and GitHub governance, Consequences, Considered alternatives, Context, Decision, References

### Community 40 - "Community 40"
Cohesion: 0.29
Nodes (6): ADR 0002: Define control-plane boundaries and persistence, Consequences, Considered alternatives, Context, Decision, References

### Community 41 - "Community 41"
Cohesion: 0.29
Nodes (6): ADR NNNN: Decision title, Consequences, Considered alternatives, Context, Decision, References

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (6): Authentication, Control-plane API, Endpoints, Local development, Persistence, Runtime configuration

### Community 43 - "Community 43"
Cohesion: 0.18
Nodes (10): Change Workflow, Collaboration Platform, Definition of Done, Engineering Guidance, Git Conventions, graphify, Project Working Agreement, Pull request definition of done (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (5): Context, Decisions, Goals / Non-Goals, Migration Plan, Risks / Trade-offs

### Community 46 - "Community 46"
Cohesion: 0.33
Nodes (5): 1. Planning Artifacts, 2. Workflow Documentation, 3. Issue Templates, 4. Seed GitHub Issues, 5. Validation and Archival

### Community 47 - "Community 47"
Cohesion: 0.33
Nodes (5): 1. Test Fixtures, 2. Worker Validation Tests, 3. Worker Validation Implementation, 4. Contract and Documentation Updates, 5. Verification

### Community 48 - "Community 48"
Cohesion: 0.33
Nodes (5): Before starting, Contributing, Local checks, Pull requests, Workflow

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (5): Documentation and architecture, OpenSpec, Security and privacy, Summary, Validation

### Community 51 - "Community 51"
Cohesion: 0.47
Nodes (5): make_job(), make_manifest(), test_dynamodb_round_trip_listing_ttl_and_conflict(), test_recording_batch_fake_is_idempotent(), test_s3_presigning_objects_and_manifest_conflicts()

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (5): ADDED Requirements, Requirement: Permanent worker validation failures, Scenario: Persist unsupported content safely, Scenario: Persist validation failure safely, Scenario: Reject retry for permanent validation failures

### Community 53 - "Community 53"
Cohesion: 0.25
Nodes (7): Issue template configuration, GitHub private vulnerability reporting, Coordinated vulnerability disclosure, Reporting a vulnerability, Security policy, Sensitive documents, Supported versions

### Community 55 - "Community 55"
Cohesion: 0.33
Nodes (5): MODIFIED Requirements, Requirement: Managed roadmap, Scenario: Roadmap order is published, Scenario: Milestone completes, Scenario: Next milestone is selected

### Community 56 - "Community 56"
Cohesion: 0.50
Nodes (3): 1. Versioned Roadmap, 2. GitHub Roadmap Metadata, 3. Verification and Completion

### Community 57 - "Community 57"
Cohesion: 0.50
Nodes (3): Architecture decision records, Creating a record, Records

### Community 58 - "Community 58"
Cohesion: 0.40
Nodes (4): Analysis worker, Rasterization, Safe failures, Source validation

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (3): Project principles, Redact All The Things, Start here

### Community 67 - "Community 67"
Cohesion: 0.15
Nodes (12): ADDED Requirements, Requirement: Page artifact metadata preserves downstream ordering, Requirement: Rasterization failures are safe permanent failures, Requirement: Rasterization remains memory bounded, Requirement: Worker rasterizes accepted sources into page artifacts, Scenario: Avoid downstream artifacts after rasterization failure, Scenario: Keep rasterization metadata separate from review manifests, Scenario: Persist safe failure on rasterization error (+4 more)

### Community 68 - "Community 68"
Cohesion: 0.17
Nodes (11): Context, Decisions, Goals / Non-Goals, Keep processing sequential and writer-driven, Migration Plan, Normalize all page artifacts to PNG, Open Questions, Risks / Trade-offs (+3 more)

### Community 69 - "Community 69"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 71 - "Community 71"
Cohesion: 0.33
Nodes (5): 1. Test Fixtures, 2. Worker Rasterization Tests, 3. Worker Rasterization Implementation, 4. Documentation Updates, 5. Verification

### Community 92 - "Community 92"
Cohesion: 0.40
Nodes (5): ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Documentation as Code

### Community 93 - "Community 93"
Cohesion: 0.40
Nodes (5): Private AWS architecture, Checkpoint recovery, AWS Batch Fargate Spot processing, Scale-to-zero cost controls, Serverless control plane

### Community 94 - "Community 94"
Cohesion: 0.40
Nodes (5): Privacy-preserving logging, Bug report issue template, Reproducible bug reports, Synthetic or sanitized bug fixtures, Sensitive data exclusion

## Knowledge Gaps
- **397 isolated node(s):** `Source validation`, `Rasterization`, `Safe failures`, `1. Test Fixtures`, `2. Worker Rasterization Tests` (+392 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Job` connect `Technical Scope` to `Community 70`, `Archived Governance Requirements`, `Community 6`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Why does `JobStatus` connect `Technical Scope` to `Governance Specification`, `Community 28`, `Archived Governance Requirements`, `Community 6`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `SourceType` connect `Technical Scope` to `Governance Specification`, `Archived Governance Requirements`, `Community 6`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 66 inferred relationships involving `Job` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`Job` has 66 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `SourceType` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`SourceType` has 61 INFERRED edges - model-reasoned connections that need verification._
- **Are the 53 inferred relationships involving `JobStatus` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`JobStatus` has 53 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `PageManifest` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`PageManifest` has 51 INFERRED edges - model-reasoned connections that need verification._