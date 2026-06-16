## Why

The roadmap currently maps broad product milestones to single GitHub issues,
OpenSpec changes, branches, and pull requests. That makes each implementation
round too large to review and weakens OpenSpec as a focused change contract.

## What Changes

- Reclassify macro roadmap issues as parent epics rather than implementation
  containers.
- Define implementation-slice child issues as the unit for OpenSpec changes,
  branches, pull requests, tests, and reviews.
- Target each implementation slice at one to two days of focused work.
- Keep only one child implementation issue active for solo development.
- Add issue templates for epics and implementation slices.
- Seed child issues for the next analysis-worker epic and light frontend
  coordination work.

## Capabilities

### New Capabilities

### Modified Capabilities

- `repository-governance`: Roadmap and contribution requirements now distinguish
  parent epics from implementation-slice child issues.

## Impact

- Repository workflow documentation.
- GitHub issue templates.
- GitHub Project issue structure and status metadata.
- OpenSpec repository-governance specification.
