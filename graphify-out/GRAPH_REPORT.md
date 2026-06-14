# Graph Report - .  (2026-06-14)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 302 nodes · 299 edges · 33 communities (32 shown, 1 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c9ab4084`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_OpenSpec Change Lifecycle|OpenSpec Change Lifecycle]]
- [[_COMMUNITY_Documentation and Contribution Policy|Documentation and Contribution Policy]]
- [[_COMMUNITY_Redaction System Architecture|Redaction System Architecture]]
- [[_COMMUNITY_Security Reporting and Fixtures|Security Reporting and Fixtures]]
- [[_COMMUNITY_Automated Quality and Pages|Automated Quality and Pages]]
- [[_COMMUNITY_Protected Main and Publication|Protected Main and Publication]]
- [[_COMMUNITY_Repository Linting|Repository Linting]]
- [[_COMMUNITY_Architecture Decision Records|Architecture Decision Records]]
- [[_COMMUNITY_Feature Request Intake|Feature Request Intake]]
- [[_COMMUNITY_Dependency Automation|Dependency Automation]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]

## God Nodes (most connected - your core abstractions)
1. `Project Working Agreement` - 14 edges
2. `Development workflow` - 14 edges
3. `Technical Scope: Assisted File Redaction Application` - 13 edges
4. `Assisted File Redaction technical scope` - 13 edges
5. `ADDED Requirements` - 11 edges
6. `Requirements` - 11 edges
7. `ADR 0001: Documentation and GitHub governance` - 11 edges
8. `3. Functional Requirements` - 7 edges
9. `9. Testing Strategy` - 7 edges
10. `OpenSpec Onboarding` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `Local validation suite` --semantically_similar_to--> `Quality workflow`  [INFERRED] [semantically similar]
  docs/development.md → .github/workflows/quality.yml
- `Issue-to-PR lifecycle` --semantically_similar_to--> `OpenSpec change workflow`  [INFERRED] [semantically similar]
  CONTRIBUTING.md → AGENTS.md
- `Markdown and YAML linting` --references--> `PyMarkdown lint configuration`  [EXTRACTED]
  .pre-commit-config.yaml → .pymarkdown.json

## Import Cycles
- None detected.

## Communities (33 total, 1 thin omitted)

### Community 1 - "OpenSpec Change Lifecycle"
Cohesion: 0.12
Nodes (22): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+14 more)

### Community 2 - "Documentation and Contribution Policy"
Cohesion: 0.08
Nodes (32): ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Change Workflow, Collaboration Platform, Definition of Done, Documentation as Code (+24 more)

### Community 3 - "Redaction System Architecture"
Cohesion: 0.10
Nodes (23): Append-only decision history, Architecture decision record index, Decision trade-off structure, MADR template, 24-hour job retention, Assisted File Redaction technical scope, Private AWS architecture, Official AWS ECS regional price index (+15 more)

### Community 5 - "Security Reporting and Fixtures"
Cohesion: 0.15
Nodes (12): Privacy-preserving logging, Bug report issue template, Reproducible bug reports, Synthetic or sanitized bug fixtures, Issue template configuration, GitHub private vulnerability reporting, Coordinated vulnerability disclosure, Reporting a vulnerability (+4 more)

### Community 6 - "Automated Quality and Pages"
Cohesion: 0.29
Nodes (7): Local validation suite, GitHub Pages deployment, GitHub Pages workflow, Strict MkDocs build, OpenSpec strict validation, Pre-commit validation, Quality workflow

### Community 7 - "Protected Main and Publication"
Cohesion: 0.06
Nodes (30): 10. Acceptance Criteria, 11. Principal Risks, 12. References, 1. Objective, 2. Scope, 3. Functional Requirements, 5. Core Data Model, 6. Security Requirements (+22 more)

### Community 8 - "Repository Linting"
Cohesion: 0.33
Nodes (6): Markdown and YAML linting, Pre-commit configuration, Repository hygiene hooks, PyMarkdown lint configuration, Relaxed Markdown rules, YAML lint configuration

### Community 9 - "Architecture Decision Records"
Cohesion: 0.09
Nodes (21): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+13 more)

### Community 10 - "Feature Request Intake"
Cohesion: 0.67
Nodes (3): Feature request issue template, Observable success, Scope boundaries

### Community 13 - "Community 13"
Cohesion: 0.08
Nodes (23): Requirement: Architecture decision records, Requirement: Automated pull request quality, Requirement: Dependency and security automation, Requirement: Managed roadmap, Requirement: Protected main workflow, Requirement: Published documentation, Requirement: Repository contribution metadata, Requirement: Reproducible repository tooling (+15 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (19): Codebase Analysis, Graceful Exit Handling, Guardrails, Phase 10: Archive, Phase 11: Recap & Next Steps, Phase 1: Welcome, Phase 2: Task Selection, Phase 3: Explore Demo (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.17
Nodes (11): Configure GitHub as part of bootstrap, Context, Decisions, Goals / Non-Goals, Keep agent and Graphify assets versioned, Migration Plan, Open Questions, Publish documentation from `docs/` (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (10): Check for context, Ending Discovery, Guardrails, Handling Different Entry Points, OpenSpec Awareness, The Stance, What You Don't Have To Do, What You Might Do (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.25
Nodes (8): 4. System Architecture, Amazon DynamoDB, Amazon S3, Control Plane, Frontend, Persistence, Processing, Region

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (6): Capabilities, Impact, Modified Capabilities, New Capabilities, What Changes, Why

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (6): 1. Reproducible Tooling, 2. Documentation, 3. GitHub Repository Files, 4. Knowledge Graph and Local Verification, 5. GitHub Publication, 6. Completion

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (6): ADR 0001: Adopt documentation-as-code and GitHub governance, Consequences, Considered alternatives, Context, Decision, References

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (6): ADR NNNN: Decision title, Consequences, Considered alternatives, Context, Decision, References

### Community 22 - "Community 22"
Cohesion: 0.29
Nodes (6): Contributing, Documentation, License, Local setup, Redact All The Things, Security

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (5): Before starting, Contributing, Local checks, Pull requests, Workflow

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (5): Documentation and architecture, OpenSpec, Security and privacy, Summary, Validation

### Community 25 - "Community 25"
Cohesion: 0.50
Nodes (3): Architecture decision records, Creating a record, Records

### Community 26 - "Community 26"
Cohesion: 0.50
Nodes (3): Project principles, Redact All The Things, Start here

## Knowledge Gaps
- **166 isolated node(s):** `The Stance`, `What You Might Do`, `Check for context`, `When no change exists`, `When a change exists` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assisted File Redaction technical scope` connect `Redaction System Architecture` to `Documentation and Contribution Policy`, `Security Reporting and Fixtures`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Development workflow` connect `Documentation and Contribution Policy` to `Redaction System Architecture`, `Automated Quality and Pages`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `Privacy-preserving logging` connect `Security Reporting and Fixtures` to `Redaction System Architecture`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **What connects `The Stance`, `What You Might Do`, `Check for context` to the rest of the system?**
  _180 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `OpenSpec Change Lifecycle` be split into smaller, more focused modules?**
  _Cohesion score 0.12121212121212122 - nodes in this community are weakly interconnected._
- **Should `Documentation and Contribution Policy` be split into smaller, more focused modules?**
  _Cohesion score 0.0766488413547237 - nodes in this community are weakly interconnected._
- **Should `Redaction System Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.10276679841897234 - nodes in this community are weakly interconnected._