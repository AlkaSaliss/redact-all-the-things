## MODIFIED Requirements

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

Repository-maintainer-approved roadmap exceptions SHALL be recorded in
versioned documentation and represented by child implementation issues. Issue #4
Floci-backed infrastructure child slices MAY proceed before the original
prerequisite epics are complete, but real AWS deployment remains deferred to
the dedicated real-AWS swap child issue.

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

#### Scenario: Execute approved issue 4 infrastructure slices early
- **GIVEN** issue #4 has child implementation issues for Floci-backed infrastructure work
- **WHEN** those child issues are implemented before issues #5, #6, and #8 are complete
- **THEN** the work remains valid only if each child issue keeps its own OpenSpec change, branch, pull request, tests, and documentation updates
- **AND** the docs state that real AWS deployment remains deferred to the dedicated real-AWS swap ticket
