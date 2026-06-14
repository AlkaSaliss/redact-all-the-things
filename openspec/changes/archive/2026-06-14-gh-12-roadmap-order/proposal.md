## Why

The six implementation milestones exist in GitHub Projects, but issue numbering
does not reflect their dependency order and the repository does not document
which contracts and verification gates unlock later work. Making the sequence
explicit prevents parallel work from stabilizing incompatible interfaces or
provisioning AWS before local behavior is proven.

## What Changes

- Publish an authoritative roadmap page with the approved milestone order,
  dependency flow, completion gates, and solo-development work-in-progress
  policy.
- Add a numeric `Roadmap Order` field to the GitHub Project and assign values
  one through six to the implementation milestones.
- Update each milestone issue with prerequisites, completion gates, and the
  next milestone it unlocks.
- Move issue #7 to `Ready` and keep the other implementation milestones in
  `Backlog`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `repository-governance`: Require an authoritative, dependency-aware roadmap
  whose documentation, issue metadata, Project order, and workflow status
  agree.

## Impact

- Adds a roadmap page to the MkDocs navigation.
- Updates the GitHub Project schema and milestone item values.
- Updates GitHub issues #3 through #8.
- Introduces no application runtime, API, data model, container, or AWS
  infrastructure implementation.
