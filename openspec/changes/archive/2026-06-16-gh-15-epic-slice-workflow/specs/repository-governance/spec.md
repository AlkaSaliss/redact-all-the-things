## MODIFIED Requirements

### Requirement: Repository contribution metadata
The repository SHALL provide structured bug, feature, epic, and implementation
slice issue forms, a pull request checklist, CODEOWNERS, contribution guidance,
security reporting instructions, and an Apache-2.0 license.

#### Scenario: Contributor proposes a change
- **WHEN** a contributor opens an issue or pull request
- **THEN** GitHub presents templates that require scope, validation, documentation, ADR, OpenSpec, and Graphify impact appropriate to the work item type

#### Scenario: Contributor creates an implementation slice
- **WHEN** a contributor opens an implementation-slice issue
- **THEN** the issue template requires a parent epic, OpenSpec change name, acceptance criteria, test plan, and review-size checklist

### Requirement: Managed roadmap
The repository SHALL maintain a GitHub Project with Backlog, Ready, In
Progress, In Review, and Done states and SHALL keep an authoritative
dependency-aware implementation roadmap in versioned documentation, milestone
issues, child implementation issues, and numeric Project ordering.

The approved milestone sequence SHALL be control-plane API and job contracts,
analysis worker, frontend authentication shell, review and export, AWS
infrastructure, then end-to-end verification. Macro roadmap issues SHALL act as
parent epics. Implementation-slice child issues SHALL be the unit for OpenSpec
changes, branches, pull requests, tests, and reviews. For solo development,
only one dependency-satisfied child implementation issue SHALL be `Ready` or
`In Progress`; later child issues SHALL remain in `Backlog`.

#### Scenario: Roadmap order is published
- **WHEN** a contributor views the versioned roadmap, milestone issues, or GitHub Project
- **THEN** each surface presents the same six-step implementation sequence and dependency gates

#### Scenario: Next implementation slice is selected
- **WHEN** no implementation slice is in progress
- **THEN** exactly one dependency-satisfied child issue is `Ready` and later child issues remain in `Backlog`

#### Scenario: Parent epic tracks child work
- **WHEN** a macro roadmap issue is decomposed
- **THEN** the parent issue identifies its child implementation issues and the child issues link back to the parent epic

#### Scenario: Implementation slice completes
- **WHEN** the current implementation-slice child issue reaches `Done`
- **THEN** the next dependency-satisfied child issue may move to `Ready` while unrelated or later child issues remain in `Backlog`
