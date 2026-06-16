## Context

The roadmap has six macro implementation issues. Issue #7 demonstrated that a
single macro issue can produce a large OpenSpec change and a large PR even when
the implementation is disciplined. The repository needs a smaller unit of
planning and review while preserving dependency-aware roadmap visibility.

## Goals / Non-Goals

**Goals:**

- Keep macro roadmap issues as parent epics.
- Make child implementation issues the OpenSpec and PR unit.
- Seed the next worker and frontend work without implementing product code.
- Keep Project status meaningful for solo development.

**Non-Goals:**

- No runtime, frontend, worker, or infrastructure implementation.
- No mandatory label taxonomy.
- No release milestone system.
- No custom automation for parent/sub-issue synchronization.

## Decisions

1. Use parent epics plus implementation-slice child issues.
   - Rationale: parent issues preserve roadmap context while child issues keep
     OpenSpec changes and PRs reviewable.
   - Alternative rejected: one PR per milestone, which produced oversized
     review scope.

2. Require full OpenSpec only for child implementation issues.
   - Rationale: parent epics are planning containers; child issues change
     behavior, docs, contracts, or process.
   - Alternative rejected: OpenSpec at both parent and child level, which would
     duplicate planning artifacts.

3. Use GitHub issue templates and body links as the durable baseline.
   - Rationale: the local GitHub CLI does not expose native sub-issue commands.
     Parent links in bodies and Project status are stable and easy to audit.
   - Alternative considered: labels or milestones. Labels are weaker for
     hierarchy; milestones fit releases better than roadmap epics.

4. Seed #6 in detail and #8 lightly.
   - Rationale: #6 is the next solo-development track. #8 only needs enough
     child issues to coordinate API/client contract consumption.

## Risks / Trade-offs

- More issues and OpenSpec changes -> mitigated by one to two day slice targets.
- Parent issue progress may drift from child issue state -> mitigated by
  parent body child checklists and Project status review.
- Native GitHub sub-issues may later become available through tooling ->
  existing parent links can be upgraded without changing the workflow.

## Migration Plan

1. Update workflow docs and issue templates.
2. Seed child issues for #6 and #8.
3. Add all seeded issues to the Project.
4. Move only the #6 file-validation child issue to Ready.
5. Keep parent epics in Backlog until their first child starts.
