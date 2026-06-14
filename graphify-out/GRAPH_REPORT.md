# Graph Report - redact-all-the-things  (2026-06-14)

## Corpus Check
- 22 files · ~8,634 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 306 nodes · 309 edges · 29 communities (26 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f826c5a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Project Architecture|Project Architecture]]
- [[_COMMUNITY_Technical Scope|Technical Scope]]
- [[_COMMUNITY_Working Agreement|Working Agreement]]
- [[_COMMUNITY_Governance Specification|Governance Specification]]
- [[_COMMUNITY_OpenSpec Change Lifecycle|OpenSpec Change Lifecycle]]
- [[_COMMUNITY_Archived Governance Requirements|Archived Governance Requirements]]
- [[_COMMUNITY_Governance Automation|Governance Automation]]
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

## God Nodes (most connected - your core abstractions)
1. `Project Working Agreement` - 17 edges
2. `Technical Scope: Assisted File Redaction Application` - 13 edges
3. `Development workflow` - 12 edges
4. `Requirements` - 11 edges
5. `ADDED Requirements` - 11 edges
6. `Assisted File Redaction technical scope` - 11 edges
7. `ADR 0001: Documentation and GitHub governance` - 10 edges
8. `Quality workflow` - 8 edges
9. `3. Functional Requirements` - 7 edges
10. `9. Testing Strategy` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Local validation suite` --semantically_similar_to--> `Quality workflow`  [INFERRED] [semantically similar]
  docs/development.md → .github/workflows/quality.yml
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `Issue-to-PR lifecycle` --semantically_similar_to--> `OpenSpec change workflow`  [INFERRED] [semantically similar]
  CONTRIBUTING.md → AGENTS.md
- `Completed governance bootstrap tasks` --records_update_to--> `Project Working Agreement`  [EXTRACTED]
  openspec/changes/archive/2026-06-14-gh-1-bootstrap-governance/tasks.md → AGENTS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Repository quality enforcement** — agents_definition_of_done, repository_governance_spec_automated_quality, workflows_quality_quality_workflow, pre_commit_config_pre_commit_checks [INFERRED 0.95]
- **Versioned documentation delivery** — agents_documentation_as_code, repository_governance_spec_published_documentation, workflows_pages_strict_mkdocs_build, workflows_pages_github_pages_deployment [INFERRED 0.95]
- **Tracked knowledge asset lifecycle** — agents_tracked_knowledge_assets, agents_graphify_workflow, repository_governance_spec_tracked_assets, 2026_06_14_gh_1_bootstrap_governance_tasks_completed_bootstrap [INFERRED 0.85]

## Communities (29 total, 3 thin omitted)

### Community 0 - "Project Architecture"
Cohesion: 0.14
Nodes (16): 24-hour job retention, Assisted File Redaction technical scope, Private AWS architecture, Official AWS ECS regional price index, Checkpoint recovery, AWS Batch Fargate Spot processing, Mandatory human review, Normalized redaction regions (+8 more)

### Community 1 - "Technical Scope"
Cohesion: 0.08
Nodes (23): 10. Acceptance Criteria, 11. Principal Risks, 12. References, 1. Objective, 2. Scope, 5. Core Data Model, 6. Security Requirements, 7. Cost Controls (+15 more)

### Community 2 - "Working Agreement"
Cohesion: 0.09
Nodes (29): ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Append-only decision history, Architecture decision record index, Decision trade-off structure, MADR template (+21 more)

### Community 3 - "Governance Specification"
Cohesion: 0.08
Nodes (25): Requirement: Managed roadmap, Scenario: Milestone completes, Scenario: Next milestone is selected, Scenario: Roadmap order is published, Purpose, Repository Governance Specification, Requirement: Architecture decision records, Requirement: Automated pull request quality (+17 more)

### Community 4 - "OpenSpec Change Lifecycle"
Cohesion: 0.12
Nodes (22): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+14 more)

### Community 5 - "Archived Governance Requirements"
Cohesion: 0.09
Nodes (21): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+13 more)

### Community 6 - "Governance Automation"
Cohesion: 0.10
Nodes (24): Repository governance proposal, Repository governance capability, Completed governance bootstrap tasks, Architecture and documentation alignment, Local validation suite, Architecture decisions, Change lifecycle, Development workflow (+16 more)

### Community 7 - "OpenSpec Onboarding"
Cohesion: 0.18
Nodes (10): Context, Decisions, Encode gates in milestone issues, Goals / Non-Goals, Keep the versioned roadmap authoritative, Limit solo work in progress, Migration Plan, Open Questions (+2 more)

### Community 8 - "Bootstrap Execution"
Cohesion: 0.14
Nodes (12): 1. Reproducible Tooling, 2. Documentation, 3. GitHub Repository Files, 4. Knowledge Graph and Local Verification, 5. GitHub Publication, 6. Completion, Contributing, Documentation (+4 more)

### Community 9 - "Security Reporting"
Cohesion: 0.15
Nodes (12): Privacy-preserving logging, Bug report issue template, Reproducible bug reports, Synthetic or sanitized bug fixtures, Issue template configuration, GitHub private vulnerability reporting, Coordinated vulnerability disclosure, Reporting a vulnerability (+4 more)

### Community 10 - "Governance Design"
Cohesion: 0.17
Nodes (11): Configure GitHub as part of bootstrap, Context, Decisions, Goals / Non-Goals, Keep agent and Graphify assets versioned, Migration Plan, Open Questions, Publish documentation from `docs/` (+3 more)

### Community 11 - "OpenSpec Exploration"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 12 - "AWS System Architecture"
Cohesion: 0.25
Nodes (8): 4. System Architecture, Amazon DynamoDB, Amazon S3, Control Plane, Frontend, Persistence, Processing, Region

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
Cohesion: 0.29
Nodes (7): 3. Functional Requirements, Analysis, Authentication, Export, Retention, Review, Upload

### Community 28 - "Community 28"
Cohesion: 0.50
Nodes (3): 1. Versioned Roadmap, 2. GitHub Roadmap Metadata, 3. Verification and Completion

## Knowledge Gaps
- **169 isolated node(s):** `Context`, `Goals / Non-Goals`, `Use a numeric Project field`, `Keep the versioned roadmap authoritative`, `Encode gates in milestone issues` (+164 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assisted File Redaction technical scope` connect `Project Architecture` to `Security Reporting`, `Working Agreement`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `ADR 0001: Documentation and GitHub governance` connect `Working Agreement` to `Project Architecture`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Project Working Agreement` connect `Working Agreement` to `Governance Automation`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **What connects `Context`, `Goals / Non-Goals`, `Use a numeric Project field` to the rest of the system?**
  _183 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._
- **Should `Technical Scope` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._
- **Should `Working Agreement` be split into smaller, more focused modules?**
  _Cohesion score 0.08735632183908046 - nodes in this community are weakly interconnected._