# Graph Report - redact-all-the-things  (2026-06-15)

## Corpus Check
- 52 files · ~18,520 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 622 nodes · 1288 edges · 46 communities (37 shown, 9 thin omitted)
- Extraction: 62% EXTRACTED · 38% INFERRED · 0% AMBIGUOUS · INFERRED: 492 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d6414cf3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Project Architecture|Project Architecture]]
- [[_COMMUNITY_Technical Scope|Technical Scope]]
- [[_COMMUNITY_Working Agreement|Working Agreement]]
- [[_COMMUNITY_Governance Specification|Governance Specification]]
- [[_COMMUNITY_OpenSpec Change Lifecycle|OpenSpec Change Lifecycle]]
- [[_COMMUNITY_Archived Governance Requirements|Archived Governance Requirements]]
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
- [[_COMMUNITY_OpenSpec Bulk Archive|OpenSpec Bulk Archive]]
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
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]

## God Nodes (most connected - your core abstractions)
1. `PageManifest` - 55 edges
2. `Job` - 51 edges
3. `ControlPlaneService` - 49 edges
4. `RedactionRegion` - 46 edges
5. `SourceType` - 42 edges
6. `InvalidRequestError` - 41 edges
7. `JobNotFoundError` - 37 edges
8. `JobStatus` - 36 edges
9. `ManifestConflictError` - 35 edges
10. `FailureCode` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `Issue-to-PR lifecycle` --semantically_similar_to--> `OpenSpec change workflow`  [INFERRED] [semantically similar]
  CONTRIBUTING.md → AGENTS.md
- `Job` --uses--> `SourceType`  [INFERRED]
  tests/domain/test_jobs.py → src/redact_api/domain.py
- `FailureCode` --uses--> `SourceType`  [INFERRED]
  tests/domain/test_lifecycle.py → src/redact_api/domain.py

## Import Cycles
- 1-file cycle: `src/redact_api/domain.py -> src/redact_api/domain.py`
- 1-file cycle: `src/redact_api/services.py -> src/redact_api/services.py`
- 1-file cycle: `src/redact_api/http.py -> src/redact_api/http.py`
- 1-file cycle: `tests/services/test_control_plane.py -> tests/services/test_control_plane.py`

## Hyperedges (group relationships)
- **Repository quality enforcement** — agents_definition_of_done, repository_governance_spec_automated_quality, workflows_quality_quality_workflow, pre_commit_config_pre_commit_checks [INFERRED 0.95]
- **Versioned documentation delivery** — agents_documentation_as_code, repository_governance_spec_published_documentation, workflows_pages_strict_mkdocs_build, workflows_pages_github_pages_deployment [INFERRED 0.95]
- **Tracked knowledge asset lifecycle** — agents_tracked_knowledge_assets, agents_graphify_workflow, repository_governance_spec_tracked_assets, 2026_06_14_gh_1_bootstrap_governance_tasks_completed_bootstrap [INFERRED 0.85]

## Communities (46 total, 9 thin omitted)

### Community 0 - "Project Architecture"
Cohesion: 0.07
Nodes (28): 24-hour job retention, Assisted File Redaction technical scope, Private AWS architecture, Official AWS ECS regional price index, Checkpoint recovery, AWS Batch Fargate Spot processing, Mandatory human review, Normalized redaction regions (+20 more)

### Community 1 - "Technical Scope"
Cohesion: 0.05
Nodes (38): 10. Acceptance Criteria, 11. Principal Risks, 12. References, 1. Objective, 2. Scope, 3. Functional Requirements, 4. System Architecture, 5. Core Data Model (+30 more)

### Community 2 - "Working Agreement"
Cohesion: 0.05
Nodes (47): Repository governance proposal, Repository governance capability, Completed governance bootstrap tasks, ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Change Workflow (+39 more)

### Community 3 - "Governance Specification"
Cohesion: 0.08
Nodes (25): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+17 more)

### Community 4 - "OpenSpec Change Lifecycle"
Cohesion: 0.12
Nodes (22): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+14 more)

### Community 5 - "Archived Governance Requirements"
Cohesion: 0.09
Nodes (21): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+13 more)

### Community 7 - "OpenSpec Onboarding"
Cohesion: 0.18
Nodes (10): Context, Decisions, Encode gates in milestone issues, Goals / Non-Goals, Keep the versioned roadmap authoritative, Limit solo work in progress, Migration Plan, Open Questions (+2 more)

### Community 8 - "Bootstrap Execution"
Cohesion: 0.14
Nodes (12): 1. Reproducible Tooling, 2. Documentation, 3. GitHub Repository Files, 4. Knowledge Graph and Local Verification, 5. GitHub Publication, 6. Completion, Contributing, Documentation (+4 more)

### Community 9 - "Security Reporting"
Cohesion: 0.12
Nodes (41): Any, AwsBatchSubmitter, BaseModel, DynamoJobRepository, RecordingBatchSubmitter, AwsBatchSubmitter, DynamoJobRepository, PersistenceConflictError (+33 more)

### Community 10 - "Governance Design"
Cohesion: 0.17
Nodes (11): Configure GitHub as part of bootstrap, Context, Decisions, Goals / Non-Goals, Keep agent and Graphify assets versioned, Migration Plan, Open Questions, Publish documentation from `docs/` (+3 more)

### Community 11 - "OpenSpec Exploration"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 12 - "AWS System Architecture"
Cohesion: 0.16
Nodes (41): FastAPI, LookupError, PageManifest, RedactionRegion, RegionSource, SourceType, ApiModel, AuthenticationError (+33 more)

### Community 13 - "Governance Proposal"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 14 - "Governance ADR"
Cohesion: 0.29
Nodes (6): ADR 0001: Adopt documentation-as-code and GitHub governance, Consequences, Considered alternatives, Context, Decision, References

### Community 15 - "MADR Template"
Cohesion: 0.29
Nodes (6): ADR NNNN: Decision title, Consequences, Considered alternatives, Context, Decision, References

### Community 16 - "Contribution Workflow"
Cohesion: 0.33
Nodes (5): Before starting, Contributing, Local checks, Pull requests, Workflow

### Community 17 - "Pull Request Checklist"
Cohesion: 0.33
Nodes (5): Documentation and architecture, OpenSpec, Security and privacy, Summary, Validation

### Community 19 - "Bootstrap Decisions"
Cohesion: 0.50
Nodes (4): Bootstrap governance architecture, Reproducible uv documentation toolchain, Required Quality workflow design, Spec-driven bootstrap governance change

### Community 20 - "ADR Index"
Cohesion: 0.50
Nodes (3): Architecture decision records, Creating a record, Records

### Community 21 - "Documentation Home"
Cohesion: 0.50
Nodes (3): Project principles, Redact All The Things, Start here

### Community 22 - "Feature Requests"
Cohesion: 0.67
Nodes (3): Feature request issue template, Observable success, Scope boundaries

### Community 24 - "OpenSpec Apply"
Cohesion: 0.33
Nodes (5): Contract ownership, Delivery policy, Dependency flow, Implementation roadmap, Sequence

### Community 25 - "OpenSpec Archive"
Cohesion: 0.33
Nodes (5): Requirement: Managed roadmap, Scenario: Milestone completes, Scenario: Next milestone is selected, Scenario: Roadmap order is published, MODIFIED Requirements

### Community 26 - "OpenSpec Bulk Archive"
Cohesion: 0.06
Nodes (32): ADDED Requirements, Requirement: Authenticated control-plane boundary, Requirement: Authorize completed download, Requirement: Complete upload and submit analysis, Requirement: Confirm export and submit rendering, Requirement: Create job and authorize upload, Requirement: List and retrieve jobs, Requirement: Locally testable service boundaries (+24 more)

### Community 28 - "Community 28"
Cohesion: 0.50
Nodes (3): 1. Versioned Roadmap, 2. GitHub Roadmap Metadata, 3. Verification and Completion

### Community 29 - "Community 29"
Cohesion: 0.06
Nodes (30): ADDED Requirements, Requirement: Job status lifecycle, Requirement: Optimistic job updates, Requirement: Optimistic page-manifest persistence, Requirement: Ownership and access expiry, Requirement: Page manifest contract, Requirement: Persistent job record, Requirement: Privacy-preserving persistence (+22 more)

### Community 30 - "Community 30"
Cohesion: 0.13
Nodes (14): Context, Decisions, Enforce lifecycle transitions with compare-and-set updates, Goals / Non-Goals, Keep the initial HTTP surface task-oriented, Migration Plan, Open Questions, Risks / Trade-offs (+6 more)

### Community 31 - "Community 31"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (6): 1. Application Setup, 2. Domain Contracts, 3. Application Services, 4. HTTP API, 5. AWS Persistence Integration, 6. Documentation and Verification

### Community 33 - "Community 33"
Cohesion: 0.11
Nodes (31): load(), test_shared_job_fixtures_match_the_contract(), test_shared_manifest_and_worker_fixtures_match_the_contract(), make_job(), test_expiry_is_exact_at_the_deadline(), test_invalid_transition_is_rejected(), test_normal_transitions_increment_version(), test_only_expired_jobs_can_transition_to_expired() (+23 more)

### Community 34 - "Community 34"
Cohesion: 0.28
Nodes (15): clock(), create_ready_manifest(), service(), set_status(), test_create_list_get_ownership_and_exact_expiry(), test_create_rejects_invalid_sizes(), test_download_requires_complete_existing_output(), test_export_requires_acknowledgement_and_is_idempotent() (+7 more)

### Community 36 - "Community 36"
Cohesion: 0.33
Nodes (10): make_job(), test_failed_job_requires_a_safe_failure_code(), test_job_accepts_the_persistent_contract(), test_job_rejects_foreign_object_namespaces(), test_job_rejects_invalid_limits(), test_job_rejects_progress_beyond_page_count(), test_job_rejects_unknown_fields(), test_job_rejects_unsupported_source_types() (+2 more)

### Community 37 - "Community 37"
Cohesion: 0.40
Nodes (9): client(), create_job(), create_manifest(), set_status(), test_create_list_retrieve_and_non_disclosing_not_found(), test_identity_validation_and_request_validation(), test_openapi_contains_the_public_contract(), test_upload_complete_export_retry_manifest_and_download_routes() (+1 more)

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): ADR 0002: Define control-plane boundaries and persistence, Consequences, Considered alternatives, Context, Decision, References

### Community 40 - "Community 40"
Cohesion: 0.29
Nodes (6): Authentication, Control-plane API, Endpoints, Local development, Persistence, Runtime configuration

### Community 42 - "Community 42"
Cohesion: 0.47
Nodes (5): make_job(), make_manifest(), test_dynamodb_round_trip_listing_ttl_and_conflict(), test_recording_batch_fake_is_idempotent(), test_s3_presigning_objects_and_manifest_conflicts()

## Knowledge Gaps
- **246 isolated node(s):** `Context`, `Decision`, `Consequences`, `Considered alternatives`, `References` (+241 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PageManifest` connect `AWS System Architecture` to `Security Reporting`, `Community 34`, `Community 37`, `Community 33`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `Job` connect `Security Reporting` to `Community 33`, `AWS System Architecture`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `ControlPlaneService` connect `AWS System Architecture` to `Security Reporting`, `Community 34`, `Community 37`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `PageManifest` (e.g. with `Any` and `AwsBatchSubmitter`) actually correct?**
  _`PageManifest` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `Job` (e.g. with `Any` and `AwsBatchSubmitter`) actually correct?**
  _`Job` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `ControlPlaneService` (e.g. with `FastAPI` and `ApiModel`) actually correct?**
  _`ControlPlaneService` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `RedactionRegion` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`RedactionRegion` has 41 INFERRED edges - model-reasoned connections that need verification._