# Graph Report - .  (2026-06-14)

## Corpus Check
- 26 files · ~16,285 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 142 nodes · 174 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Bootstrap Governance Requirements|Bootstrap Governance Requirements]]
- [[_COMMUNITY_OpenSpec Change Lifecycle|OpenSpec Change Lifecycle]]
- [[_COMMUNITY_Documentation and Contribution Policy|Documentation and Contribution Policy]]
- [[_COMMUNITY_Redaction System Architecture|Redaction System Architecture]]
- [[_COMMUNITY_Redaction Safety Workflow|Redaction Safety Workflow]]
- [[_COMMUNITY_Security Reporting and Fixtures|Security Reporting and Fixtures]]
- [[_COMMUNITY_Automated Quality and Pages|Automated Quality and Pages]]
- [[_COMMUNITY_Protected Main and Publication|Protected Main and Publication]]
- [[_COMMUNITY_Repository Linting|Repository Linting]]
- [[_COMMUNITY_Architecture Decision Records|Architecture Decision Records]]
- [[_COMMUNITY_Feature Request Intake|Feature Request Intake]]
- [[_COMMUNITY_OpenSpec Change Metadata|OpenSpec Change Metadata]]
- [[_COMMUNITY_Dependency Automation|Dependency Automation]]

## God Nodes (most connected - your core abstractions)
1. `Assisted File Redaction technical scope` - 13 edges
2. `Repository Governance Specification` - 12 edges
3. `ADR 0001: Documentation and GitHub governance` - 11 edges
4. `Assisted File Redaction Application` - 10 edges
5. `Project Working Agreement` - 8 edges
6. `OpenSpec Onboarding` - 7 edges
7. `Development workflow` - 7 edges
8. `OpenSpec Apply Change` - 6 edges
9. `OpenSpec Archive Change` - 6 edges
10. `Serverless AWS Architecture` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Pull request definition of done` --semantically_similar_to--> `Project Working Agreement`  [INFERRED] [semantically similar]
  .github/PULL_REQUEST_TEMPLATE.md → AGENTS.md
- `Task-Driven Implementation` --conceptually_related_to--> `Assisted File Redaction Application`  [INFERRED]
  .codex/skills/openspec-apply-change/SKILL.md → docs/superpowers/specs/2026-06-14-assisted-file-redaction-design.md
- `Three-Dimension Verification` --semantically_similar_to--> `Quality and Redaction Security Testing`  [INFERRED] [semantically similar]
  .codex/skills/openspec-verify-change/SKILL.md → docs/superpowers/specs/2026-06-14-assisted-file-redaction-design.md
- `Sensitive data exclusion` --semantically_similar_to--> `Synthetic or sanitized bug fixtures`  [INFERRED] [semantically similar]
  SECURITY.md → .github/ISSUE_TEMPLATE/bug.yml
- `Local validation suite` --semantically_similar_to--> `Quality workflow`  [INFERRED] [semantically similar]
  docs/development.md → .github/workflows/quality.yml

## Import Cycles
- None detected.

## Communities (13 total, 2 thin omitted)

### Community 0 - "Bootstrap Governance Requirements"
Cohesion: 0.10
Nodes (26): Authoritative Documentation with Supplementary Wiki, Bootstrap Governance Design, Graphify Refresh Rule, Managed GitHub Project Roadmap, GitHub Pages Workflow, Required Quality Workflow, Reproducible Repository Tooling, Tracked Agent and Graphify Assets (+18 more)

### Community 1 - "OpenSpec Change Lifecycle"
Cohesion: 0.11
Nodes (23): OpenSpec Apply Change, Task-Driven Implementation, Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Artifact Dependency Order, OpenSpec Continue Change (+15 more)

### Community 2 - "Documentation and Contribution Policy"
Cohesion: 0.14
Nodes (21): ADR 0001: Documentation and GitHub governance, Apache License 2.0, Reproducible governance controls before application code, Solo-maintainer merge policy, Documentation as code, GitHub collaboration platform, MADR architecture decisions, OpenSpec change workflow (+13 more)

### Community 3 - "Redaction System Architecture"
Cohesion: 0.13
Nodes (19): 24-hour job retention, Assisted File Redaction technical scope, Private AWS architecture, Official AWS ECS regional price index, Checkpoint recovery, AWS Batch Fargate Spot processing, Mandatory human review, Normalized redaction regions (+11 more)

### Community 4 - "Redaction Safety Workflow"
Cohesion: 0.18
Nodes (13): Assisted File Redaction Application, AWS Batch Pricing, AWS ECS Regional Price Index, AWS Fargate Pricing, AWS Lambda Quotas, Checkpointed Sequential Processing, Human Review Redaction Editor, Permanent Rasterized Redaction (+5 more)

### Community 5 - "Security Reporting and Fixtures"
Cohesion: 0.22
Nodes (9): Privacy-preserving logging, Bug report issue template, Reproducible bug reports, Synthetic or sanitized bug fixtures, Issue template configuration, GitHub private vulnerability reporting, Coordinated vulnerability disclosure, Security policy (+1 more)

### Community 6 - "Automated Quality and Pages"
Cohesion: 0.29
Nodes (7): Local validation suite, GitHub Pages deployment, GitHub Pages workflow, Strict MkDocs build, OpenSpec strict validation, Pre-commit validation, Quality workflow

### Community 7 - "Protected Main and Publication"
Cohesion: 0.33
Nodes (7): OpenSpec Archive Before Merge, Protected Main Workflow, Public Repository Security Controls, Solo Maintainer Review Trade-off, OpenSpec Change Completion, GitHub Publication, Protected Main Workflow Requirement

### Community 8 - "Repository Linting"
Cohesion: 0.33
Nodes (6): Markdown and YAML linting, Pre-commit configuration, Repository hygiene hooks, PyMarkdown lint configuration, Relaxed Markdown rules, YAML lint configuration

### Community 9 - "Architecture Decision Records"
Cohesion: 0.50
Nodes (4): Append-only decision history, Architecture decision record index, Decision trade-off structure, MADR template

### Community 10 - "Feature Request Intake"
Cohesion: 0.67
Nodes (3): Feature request issue template, Observable success, Scope boundaries

## Knowledge Gaps
- **39 isolated node(s):** `Artifact Dependency Order`, `Apply-Ready Artifacts`, `Artifact-Driven Workflow`, `Complete OpenSpec Change Cycle`, `Complete Change Artifacts` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assisted File Redaction technical scope` connect `Redaction System Architecture` to `Documentation and Contribution Policy`, `Security Reporting and Fixtures`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `ADR 0001: Documentation and GitHub governance` connect `Documentation and Contribution Policy` to `Architecture Decision Records`, `Redaction System Architecture`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Development workflow` connect `Documentation and Contribution Policy` to `Redaction System Architecture`, `Automated Quality and Pages`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **What connects `Archive Validation`, `Spec Conflict Resolution`, `Artifact Dependency Order` to the rest of the system?**
  _56 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Bootstrap Governance Requirements` be split into smaller, more focused modules?**
  _Cohesion score 0.09846153846153846 - nodes in this community are weakly interconnected._
- **Should `OpenSpec Change Lifecycle` be split into smaller, more focused modules?**
  _Cohesion score 0.11462450592885376 - nodes in this community are weakly interconnected._
- **Should `Documentation and Contribution Policy` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._