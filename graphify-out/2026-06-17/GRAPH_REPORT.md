# Graph Report - redact-all-the-things  (2026-06-16)

## Corpus Check
- 58 files · ~22,658 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 831 nodes · 1478 edges · 96 communities (86 shown, 10 thin omitted)
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 490 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ee8ab2cb`
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
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]

## God Nodes (most connected - your core abstractions)
1. `PageManifest` - 56 edges
2. `Job` - 52 edges
3. `ControlPlaneService` - 50 edges
4. `RedactionRegion` - 47 edges
5. `SourceType` - 43 edges
6. `InvalidRequestError` - 41 edges
7. `JobStatus` - 37 edges
8. `JobNotFoundError` - 37 edges
9. `ManifestConflictError` - 35 edges
10. `FailureCode` - 34 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `JobStatus` --uses--> `SourceType`  [INFERRED]
  tests/domain/test_lifecycle.py → src/redact_api/domain.py
- `ControlPlaneService` --uses--> `SourceType`  [INFERRED]
  tests/services/test_control_plane.py → src/redact_api/domain.py
- `TestClient` --uses--> `JobStatus`  [INFERRED]
  tests/api/test_http.py → src/redact_api/domain.py

## Import Cycles
- 1-file cycle: `src/redact_api/domain.py -> src/redact_api/domain.py`
- 1-file cycle: `src/redact_api/services.py -> src/redact_api/services.py`
- 1-file cycle: `src/redact_api/http.py -> src/redact_api/http.py`
- 1-file cycle: `tests/services/test_control_plane.py -> tests/services/test_control_plane.py`

## Hyperedges (group relationships)
- **Repository quality enforcement** — agents_definition_of_done, repository_governance_spec_automated_quality, workflows_quality_quality_workflow, pre_commit_config_pre_commit_checks [INFERRED 0.95]
- **Versioned documentation delivery** — agents_documentation_as_code, repository_governance_spec_published_documentation, workflows_pages_strict_mkdocs_build, workflows_pages_github_pages_deployment [INFERRED 0.95]
- **Tracked knowledge asset lifecycle** — agents_tracked_knowledge_assets, agents_graphify_workflow, repository_governance_spec_tracked_assets, 2026_06_14_gh_1_bootstrap_governance_tasks_completed_bootstrap [INFERRED 0.85]

## Communities (96 total, 10 thin omitted)

### Community 0 - "Project Architecture"
Cohesion: 0.22
Nodes (11): 24-hour job retention, Assisted File Redaction technical scope, Official AWS ECS regional price index, Mandatory human review, Normalized redaction regions, Optimistic page-manifest versioning, Assisted redaction application, GLiNER2 (+3 more)

### Community 1 - "Technical Scope"
Cohesion: 0.05
Nodes (38): 10. Acceptance Criteria, 11. Principal Risks, 12. References, 1. Objective, 2. Scope, 3. Functional Requirements, 4. System Architecture, 5. Core Data Model (+30 more)

### Community 2 - "Working Agreement"
Cohesion: 0.17
Nodes (16): Repository governance proposal, Repository governance capability, Completed governance bootstrap tasks, Archived repository governance requirements, Automated pull request quality requirement, Protected main workflow requirement, Published documentation requirement, Tracked agent knowledge assets requirement (+8 more)

### Community 3 - "Governance Specification"
Cohesion: 0.07
Nodes (27): Requirement: Managed roadmap, Requirement: Repository contribution metadata, Scenario: Contributor creates an implementation slice, Scenario: Contributor proposes a change, Scenario: Implementation slice completes, Scenario: Next implementation slice is selected, Scenario: Parent epic tracks child work, Scenario: Roadmap order is published (+19 more)

### Community 4 - "OpenSpec Change Lifecycle"
Cohesion: 0.12
Nodes (22): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+14 more)

### Community 5 - "Archived Governance Requirements"
Cohesion: 0.09
Nodes (21): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+13 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (34): Control-Plane API Specification, Purpose, Requirements, Requirement: Authenticated control-plane boundary, Requirement: Authorize completed download, Requirement: Complete upload and submit analysis, Requirement: Confirm export and submit rendering, Requirement: Create job and authorize upload (+26 more)

### Community 7 - "OpenSpec Onboarding"
Cohesion: 0.18
Nodes (10): Context, Decisions, Encode gates in milestone issues, Goals / Non-Goals, Keep the versioned roadmap authoritative, Limit solo work in progress, Migration Plan, Open Questions (+2 more)

### Community 8 - "Bootstrap Execution"
Cohesion: 0.14
Nodes (12): 1. Reproducible Tooling, 2. Documentation, 3. GitHub Repository Files, 4. Knowledge Graph and Local Verification, 5. GitHub Publication, 6. Completion, Contributing, Documentation (+4 more)

### Community 9 - "Security Reporting"
Cohesion: 0.08
Nodes (102): Any, AwsBatchSubmitter, BaseModel, test_permanent_failures_are_not_retryable(), test_retryable_failures_select_the_worker_mode(), DynamoJobRepository, FastAPI, JobStatus (+94 more)

### Community 10 - "Governance Design"
Cohesion: 0.17
Nodes (11): Configure GitHub as part of bootstrap, Context, Decisions, Goals / Non-Goals, Keep agent and Graphify assets versioned, Migration Plan, Open Questions, Publish documentation from `docs/` (+3 more)

### Community 11 - "OpenSpec Exploration"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 12 - "AWS System Architecture"
Cohesion: 0.40
Nodes (9): client(), create_job(), create_manifest(), set_status(), test_create_list_retrieve_and_non_disclosing_not_found(), test_identity_validation_and_request_validation(), test_openapi_contains_the_public_contract(), test_upload_complete_export_retry_manifest_and_download_routes() (+1 more)

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
Cohesion: 0.22
Nodes (8): #6 PDF and image analysis worker, #8 React frontend and authentication shell, Contract ownership, Delivery policy, Dependency flow, Epic decomposition, Implementation roadmap, Sequence

### Community 25 - "OpenSpec Archive"
Cohesion: 0.13
Nodes (13): Requirement: Managed roadmap, Scenario: Milestone completes, Scenario: Next milestone is selected, Scenario: Roadmap order is published, Requirement: Managed roadmap, Requirement: Repository contribution metadata, Scenario: Contributor creates an implementation slice, Scenario: Contributor proposes a change (+5 more)

### Community 26 - "OpenSpec Bulk Archive"
Cohesion: 0.29
Nodes (5): ADDED Requirements, Requirement: Locally testable service boundaries, Scenario: Validate AWS integration locally, Requirement: Locally testable service boundaries, Scenario: Validate AWS integration locally

### Community 28 - "Community 28"
Cohesion: 0.50
Nodes (3): 1. Versioned Roadmap, 2. GitHub Roadmap Metadata, 3. Verification and Completion

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (4): ADDED Requirements, Requirement: Optimistic page-manifest persistence, Scenario: Save a stale manifest, Scenario: Save the current manifest

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
Cohesion: 0.12
Nodes (26): make_job(), test_expiry_is_exact_at_the_deadline(), test_invalid_transition_is_rejected(), test_normal_transitions_increment_version(), test_only_expired_jobs_can_transition_to_expired(), test_processing_can_fail(), test_retry_transition_clears_failure_code(), test_submission_token_is_stable_for_the_transition_version() (+18 more)

### Community 34 - "Community 34"
Cohesion: 0.06
Nodes (32): Job Contracts Specification, Purpose, Requirements, Requirement: Job status lifecycle, Requirement: Optimistic job updates, Requirement: Optimistic page-manifest persistence, Requirement: Ownership and access expiry, Requirement: Page manifest contract (+24 more)

### Community 36 - "Community 36"
Cohesion: 0.33
Nodes (10): make_job(), test_failed_job_requires_a_safe_failure_code(), test_job_accepts_the_persistent_contract(), test_job_rejects_foreign_object_namespaces(), test_job_rejects_invalid_limits(), test_job_rejects_progress_beyond_page_count(), test_job_rejects_unknown_fields(), test_job_rejects_unsupported_source_types() (+2 more)

### Community 37 - "Community 37"
Cohesion: 0.28
Nodes (15): clock(), create_ready_manifest(), service(), set_status(), test_create_list_get_ownership_and_exact_expiry(), test_create_rejects_invalid_sizes(), test_download_requires_complete_existing_output(), test_export_requires_acknowledgement_and_is_idempotent() (+7 more)

### Community 38 - "Community 38"
Cohesion: 0.50
Nodes (3): build_service(), AWS Lambda entry point., Construct the production service from Lambda environment settings.

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): ADR 0002: Define control-plane boundaries and persistence, Consequences, Considered alternatives, Context, Decision, References

### Community 40 - "Community 40"
Cohesion: 0.29
Nodes (6): Authentication, Control-plane API, Endpoints, Local development, Persistence, Runtime configuration

### Community 41 - "Community 41"
Cohesion: 0.13
Nodes (14): Context, Decisions, Enforce lifecycle transitions with compare-and-set updates, Goals / Non-Goals, Keep the initial HTTP surface task-oriented, Migration Plan, Open Questions, Risks / Trade-offs (+6 more)

### Community 42 - "Community 42"
Cohesion: 0.47
Nodes (5): make_job(), make_manifest(), test_dynamodb_round_trip_listing_ttl_and_conflict(), test_recording_batch_fake_is_idempotent(), test_s3_presigning_objects_and_manifest_conflicts()

### Community 43 - "Community 43"
Cohesion: 0.18
Nodes (10): Change Workflow, Collaboration Platform, Definition of Done, Engineering Guidance, Git Conventions, graphify, Project Working Agreement, Pull request definition of done (+2 more)

### Community 50 - "Community 50"
Cohesion: 0.22
Nodes (8): Architecture decisions, Change lifecycle, Development workflow, Documentation requirements, Install tooling, Local validation, Prerequisites, Work item model

### Community 51 - "Community 51"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 52 - "Community 52"
Cohesion: 0.29
Nodes (6): 1. Application Setup, 2. Domain Contracts, 3. Application Services, 4. HTTP API, 5. AWS Persistence Integration, 6. Documentation and Verification

### Community 53 - "Community 53"
Cohesion: 0.25
Nodes (7): Issue template configuration, GitHub private vulnerability reporting, Coordinated vulnerability disclosure, Reporting a vulnerability, Security policy, Sensitive documents, Supported versions

### Community 54 - "Community 54"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 55 - "Community 55"
Cohesion: 0.40
Nodes (5): Requirement: Worker submission contract, Scenario: Reject a permanent failure retry, Scenario: Retry an eligible failure, Scenario: Submit analysis, Scenario: Submit rendering

### Community 56 - "Community 56"
Cohesion: 0.40
Nodes (5): Requirement: Worker submission contract, Scenario: Reject a permanent failure retry, Scenario: Retry an eligible failure, Scenario: Submit analysis, Scenario: Submit rendering

### Community 57 - "Community 57"
Cohesion: 0.50
Nodes (4): Requirement: Complete upload and submit analysis, Scenario: Complete a missing upload, Scenario: Complete a valid upload, Scenario: Repeat upload completion

### Community 58 - "Community 58"
Cohesion: 0.50
Nodes (4): Requirement: Read and update page manifests, Scenario: Read a page manifest, Scenario: Resolve concurrent edits, Scenario: Save user changes

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (4): Requirement: Job status lifecycle, Scenario: Complete the normal lifecycle, Scenario: Record processing failure, Scenario: Reject an invalid transition

### Community 60 - "Community 60"
Cohesion: 0.50
Nodes (4): Requirement: Ownership and access expiry, Scenario: Another user accesses a job, Scenario: Owner accesses an active job, Scenario: Owner accesses an expired job

### Community 61 - "Community 61"
Cohesion: 0.50
Nodes (4): Requirement: Page manifest contract, Scenario: Preserve immutable suggestions, Scenario: Reject out-of-bounds geometry, Scenario: Validate a redaction region

### Community 62 - "Community 62"
Cohesion: 0.50
Nodes (4): Requirement: Complete upload and submit analysis, Scenario: Complete a missing upload, Scenario: Complete a valid upload, Scenario: Repeat upload completion

### Community 63 - "Community 63"
Cohesion: 0.50
Nodes (4): Requirement: Read and update page manifests, Scenario: Read a page manifest, Scenario: Resolve concurrent edits, Scenario: Save user changes

### Community 64 - "Community 64"
Cohesion: 0.50
Nodes (4): Requirement: Job status lifecycle, Scenario: Complete the normal lifecycle, Scenario: Record processing failure, Scenario: Reject an invalid transition

### Community 65 - "Community 65"
Cohesion: 0.50
Nodes (4): Requirement: Ownership and access expiry, Scenario: Another user accesses a job, Scenario: Owner accesses an active job, Scenario: Owner accesses an expired job

### Community 66 - "Community 66"
Cohesion: 0.50
Nodes (4): Requirement: Page manifest contract, Scenario: Preserve immutable suggestions, Scenario: Reject out-of-bounds geometry, Scenario: Validate a redaction region

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (3): Requirement: Authenticated control-plane boundary, Scenario: Authenticated request, Scenario: Missing identity

### Community 68 - "Community 68"
Cohesion: 0.67
Nodes (3): Requirement: Authorize completed download, Scenario: Download completed output, Scenario: Download unavailable output

### Community 69 - "Community 69"
Cohesion: 0.67
Nodes (3): Requirement: Confirm export and submit rendering, Scenario: Confirm export, Scenario: Omit export acknowledgement

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (3): Requirement: Create job and authorize upload, Scenario: Create a supported job, Scenario: Reject unsupported creation data

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (3): Requirement: List and retrieve jobs, Scenario: List recent jobs, Scenario: Retrieve an inaccessible job

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (3): Requirement: Presigned URL security, Scenario: Generate object authorization, Scenario: Record an API request

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (3): Requirement: Retry eligible processing, Scenario: Retry a transient failure, Scenario: Retry an ineligible failure

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (3): Requirement: Optimistic job updates, Scenario: Detect a stale job update, Scenario: Update the current version

### Community 75 - "Community 75"
Cohesion: 0.67
Nodes (3): Requirement: Persistent job record, Scenario: Reject an invalid job record, Scenario: Store a new job

### Community 76 - "Community 76"
Cohesion: 0.67
Nodes (3): Requirement: Privacy-preserving persistence, Scenario: Persist sensitive analysis output, Scenario: Serialize a safe job record

### Community 77 - "Community 77"
Cohesion: 0.67
Nodes (3): Requirement: Authenticated control-plane boundary, Scenario: Authenticated request, Scenario: Missing identity

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (3): Requirement: Authorize completed download, Scenario: Download completed output, Scenario: Download unavailable output

### Community 79 - "Community 79"
Cohesion: 0.67
Nodes (3): Requirement: Confirm export and submit rendering, Scenario: Confirm export, Scenario: Omit export acknowledgement

### Community 80 - "Community 80"
Cohesion: 0.67
Nodes (3): Requirement: Create job and authorize upload, Scenario: Create a supported job, Scenario: Reject unsupported creation data

### Community 81 - "Community 81"
Cohesion: 0.67
Nodes (3): Requirement: List and retrieve jobs, Scenario: List recent jobs, Scenario: Retrieve an inaccessible job

### Community 82 - "Community 82"
Cohesion: 0.67
Nodes (3): Requirement: Presigned URL security, Scenario: Generate object authorization, Scenario: Record an API request

### Community 83 - "Community 83"
Cohesion: 0.67
Nodes (3): Requirement: Retry eligible processing, Scenario: Retry a transient failure, Scenario: Retry an ineligible failure

### Community 84 - "Community 84"
Cohesion: 0.67
Nodes (3): Requirement: Optimistic job updates, Scenario: Detect a stale job update, Scenario: Update the current version

### Community 85 - "Community 85"
Cohesion: 0.67
Nodes (3): Requirement: Optimistic page-manifest persistence, Scenario: Save a stale manifest, Scenario: Save the current manifest

### Community 86 - "Community 86"
Cohesion: 0.67
Nodes (3): Requirement: Persistent job record, Scenario: Reject an invalid job record, Scenario: Store a new job

### Community 87 - "Community 87"
Cohesion: 0.67
Nodes (3): Requirement: Privacy-preserving persistence, Scenario: Persist sensitive analysis output, Scenario: Serialize a safe job record

### Community 89 - "Community 89"
Cohesion: 0.43
Nodes (3): A manifest paired with the S3 ETag used for optimistic writes., StoredManifest, PageManifest

### Community 90 - "Community 90"
Cohesion: 0.33
Nodes (5): Context, Decisions, Goals / Non-Goals, Migration Plan, Risks / Trade-offs

### Community 91 - "Community 91"
Cohesion: 0.33
Nodes (5): 1. Planning Artifacts, 2. Workflow Documentation, 3. Issue Templates, 4. Seed GitHub Issues, 5. Validation and Archival

### Community 92 - "Community 92"
Cohesion: 0.40
Nodes (5): ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Documentation as Code

### Community 93 - "Community 93"
Cohesion: 0.40
Nodes (5): Private AWS architecture, Checkpoint recovery, AWS Batch Fargate Spot processing, Scale-to-zero cost controls, Serverless control plane

### Community 94 - "Community 94"
Cohesion: 0.40
Nodes (5): Privacy-preserving logging, Bug report issue template, Reproducible bug reports, Synthetic or sanitized bug fixtures, Sensitive data exclusion

### Community 95 - "Community 95"
Cohesion: 0.83
Nodes (3): load(), test_shared_job_fixtures_match_the_contract(), test_shared_manifest_and_worker_fixtures_match_the_contract()

## Knowledge Gaps
- **385 isolated node(s):** `Collaboration Platform`, `Change Workflow`, `Git Conventions`, `Definition of Done`, `Engineering Guidance` (+380 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PageManifest` connect `Security Reporting` to `Community 33`, `Community 37`, `AWS System Architecture`, `Community 88`, `Community 89`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `Job` connect `Security Reporting` to `Community 88`, `Community 89`, `Community 33`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `ControlPlaneService` connect `Security Reporting` to `AWS System Architecture`, `Community 37`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Are the 51 inferred relationships involving `PageManifest` (e.g. with `Any` and `AwsBatchSubmitter`) actually correct?**
  _`PageManifest` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `Job` (e.g. with `Any` and `AwsBatchSubmitter`) actually correct?**
  _`Job` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `ControlPlaneService` (e.g. with `FastAPI` and `ApiModel`) actually correct?**
  _`ControlPlaneService` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `RedactionRegion` (e.g. with `AwsBatchSubmitter` and `DynamoJobRepository`) actually correct?**
  _`RedactionRegion` has 41 INFERRED edges - model-reasoned connections that need verification._