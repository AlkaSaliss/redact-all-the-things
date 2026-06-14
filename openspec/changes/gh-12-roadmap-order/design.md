## Context

The Project contains six implementation milestones, all in `Backlog`. Their
issue numbers reflect creation order rather than technical dependency order,
and no Project field currently expresses sequence. The technical scope implies
that shared contracts precede workers and clients, local behavior precedes AWS
integration, and system verification follows deployment.

## Goals / Non-Goals

**Goals:**

- Make one implementation sequence authoritative across MkDocs, GitHub Issues,
  and GitHub Projects.
- State prerequisites, completion gates, and unlock relationships for every
  milestone.
- Keep only the next solo-development milestone in `Ready`.

**Non-Goals:**

- Implement any application or infrastructure milestone.
- Split or expand the six approved milestone scopes.
- Add scheduling estimates, deadlines, or additional environments.

## Decisions

### Use a numeric Project field

Add `Roadmap Order` as a number field and assign values one through six. A
numeric field remains sortable even though issue numbers are intentionally out
of sequence. Renaming issues with numeric prefixes was rejected because the
titles should continue to describe outcomes rather than board mechanics.

### Keep the versioned roadmap authoritative

Add `docs/roadmap.md` and include it in MkDocs navigation. The page records the
sequence, dependency graph, entry criteria, completion gates, and
parallelization rule. Issue bodies and Project fields are operational views of
the same versioned policy.

### Encode gates in milestone issues

Append a standard `Roadmap` section to issues #3 through #8 containing order,
prerequisites, completion gate, and unlocks. This keeps the dependency context
visible when an issue is viewed without the board.

### Limit solo work in progress

Move #7 to `Ready`; leave all later milestones in `Backlog`. Completing a
milestone permits, but does not automatically perform, promotion of the next
dependency-satisfied milestone.

## Risks / Trade-offs

- **Project metadata can drift from repository documentation** -> Make
  consistency part of the governance specification and milestone maintenance.
- **Issue body edits are not versioned in Git** -> Keep full sequencing policy
  in MkDocs and use issue metadata as a concise operational mirror.
- **Parallel work could violate the solo sequence** -> Document that #6 and #8
  may run in parallel only when separate contributors are available and #7 is
  complete.

## Migration Plan

1. Publish the roadmap page and navigation entry.
2. Add and populate the Project numeric field.
3. Update the six milestone issues.
4. Move #7 to `Ready` and verify all later statuses remain `Backlog`.
5. Refresh Graphify and validate documentation and OpenSpec.

Rollback removes the roadmap page and field values, restores issue bodies, and
returns #7 to `Backlog`.

## Open Questions

None.
