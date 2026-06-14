# Graph Report - .  (2026-06-14)

## Corpus Check
- Corpus is ~11,607 words - fits in a single context window. You may not need a graph.

## Summary
- 36 nodes · 45 edges · 6 communities
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_OpenSpec Validation Lifecycle|OpenSpec Validation Lifecycle]]
- [[_COMMUNITY_Redaction Safety Workflow|Redaction Safety Workflow]]
- [[_COMMUNITY_OpenSpec Implementation Flow|OpenSpec Implementation Flow]]
- [[_COMMUNITY_Spec Archival and Sync|Spec Archival and Sync]]
- [[_COMMUNITY_AWS Processing and Cost|AWS Processing and Cost]]
- [[_COMMUNITY_OpenSpec Artifact Creation|OpenSpec Artifact Creation]]

## God Nodes (most connected - your core abstractions)
1. `Assisted File Redaction Application` - 10 edges
2. `OpenSpec Onboarding` - 7 edges
3. `OpenSpec Apply Change` - 6 edges
4. `OpenSpec Archive Change` - 6 edges
5. `Serverless AWS Architecture` - 6 edges
6. `OpenSpec Propose` - 5 edges
7. `OpenSpec Bulk Archive Change` - 3 edges
8. `OpenSpec Continue Change` - 3 edges
9. `OpenSpec Explore` - 3 edges
10. `OpenSpec Fast-Forward Change` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Task-Driven Implementation` --conceptually_related_to--> `Assisted File Redaction Application`  [INFERRED]
  .codex/skills/openspec-apply-change/SKILL.md → docs/superpowers/specs/2026-06-14-assisted-file-redaction-design.md
- `Three-Dimension Verification` --semantically_similar_to--> `Quality and Redaction Security Testing`  [INFERRED] [semantically similar]
  .codex/skills/openspec-verify-change/SKILL.md → docs/superpowers/specs/2026-06-14-assisted-file-redaction-design.md
- `OpenSpec Verify Change` --conceptually_related_to--> `OpenSpec Archive Change`  [INFERRED]
  .codex/skills/openspec-verify-change/SKILL.md → .codex/skills/openspec-archive-change/SKILL.md
- `OpenSpec Propose` --semantically_similar_to--> `OpenSpec Fast-Forward Change`  [INFERRED] [semantically similar]
  .codex/skills/openspec-propose/SKILL.md → .codex/skills/openspec-ff-change/SKILL.md
- `OpenSpec Apply Change` --references--> `OpenSpec Archive Change`  [EXTRACTED]
  .codex/skills/openspec-apply-change/SKILL.md → .codex/skills/openspec-archive-change/SKILL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **OpenSpec Artifact Workflow** — openspec_new_change_skill_openspec_new_change, openspec_continue_change_skill_openspec_continue_change, openspec_ff_change_skill_openspec_fast_forward_change, openspec_propose_skill_openspec_propose [INFERRED 0.95]
- **OpenSpec Change Lifecycle** — openspec_explore_skill_openspec_explore, openspec_new_change_skill_openspec_new_change, openspec_apply_change_skill_openspec_apply_change, openspec_verify_change_skill_openspec_verify_change, openspec_archive_change_skill_openspec_archive_change [EXTRACTED 1.00]
- **Assisted Redaction Safety Model** — specs_2026_06_14_assisted_file_redaction_design_pii_detection_pipeline, specs_2026_06_14_assisted_file_redaction_design_human_review_editor, specs_2026_06_14_assisted_file_redaction_design_permanent_rasterized_redaction, specs_2026_06_14_assisted_file_redaction_design_quality_and_security_testing [EXTRACTED 1.00]

## Communities (6 total, 0 thin omitted)

### Community 0 - "OpenSpec Validation Lifecycle"
Cohesion: 0.29
Nodes (7): OpenSpec Explore, Thinking, Not Implementation, Complete OpenSpec Change Cycle, OpenSpec Onboarding, OpenSpec Verify Change, Three-Dimension Verification, Quality and Redaction Security Testing

### Community 1 - "Redaction Safety Workflow"
Cohesion: 0.33
Nodes (7): Assisted File Redaction Application, Human Review Redaction Editor, Permanent Rasterized Redaction, PII Detection Pipeline, Private Invited Access, Security and Privacy Controls, 24-Hour Job Retention

### Community 2 - "OpenSpec Implementation Flow"
Cohesion: 0.40
Nodes (6): OpenSpec Apply Change, Task-Driven Implementation, Apply-Ready Artifacts, OpenSpec Fast-Forward Change, Complete Change Artifacts, OpenSpec Propose

### Community 3 - "Spec Archival and Sync"
Cohesion: 0.40
Nodes (6): Archive Validation, OpenSpec Archive Change, OpenSpec Bulk Archive Change, Spec Conflict Resolution, Intelligent Delta Spec Merge, OpenSpec Sync Specs

### Community 4 - "AWS Processing and Cost"
Cohesion: 0.33
Nodes (6): AWS Batch Pricing, AWS ECS Regional Price Index, AWS Fargate Pricing, AWS Lambda Quotas, Checkpointed Sequential Processing, Serverless AWS Architecture

### Community 5 - "OpenSpec Artifact Creation"
Cohesion: 0.50
Nodes (4): Artifact Dependency Order, OpenSpec Continue Change, Artifact-Driven Workflow, OpenSpec New Change

## Knowledge Gaps
- **13 isolated node(s):** `Artifact Dependency Order`, `Apply-Ready Artifacts`, `Artifact-Driven Workflow`, `Complete OpenSpec Change Cycle`, `Complete Change Artifacts` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Assisted File Redaction Application` connect `Redaction Safety Workflow` to `OpenSpec Validation Lifecycle`, `OpenSpec Implementation Flow`, `AWS Processing and Cost`?**
  _High betweenness centrality (0.561) - this node is a cross-community bridge._
- **Why does `OpenSpec Apply Change` connect `OpenSpec Implementation Flow` to `OpenSpec Validation Lifecycle`, `Spec Archival and Sync`, `OpenSpec Artifact Creation`?**
  _High betweenness centrality (0.522) - this node is a cross-community bridge._
- **Why does `Task-Driven Implementation` connect `OpenSpec Implementation Flow` to `Redaction Safety Workflow`?**
  _High betweenness centrality (0.425) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `OpenSpec Archive Change` (e.g. with `OpenSpec Bulk Archive Change` and `OpenSpec Verify Change`) actually correct?**
  _`OpenSpec Archive Change` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Archive Validation`, `Spec Conflict Resolution`, `Artifact Dependency Order` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._