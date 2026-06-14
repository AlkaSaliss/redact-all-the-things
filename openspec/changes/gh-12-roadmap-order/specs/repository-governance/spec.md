## MODIFIED Requirements

### Requirement: Managed roadmap
The repository SHALL maintain a GitHub Project with Backlog, Ready, In
Progress, In Review, and Done states and SHALL keep an authoritative
dependency-aware implementation roadmap in versioned documentation, milestone
issues, and numeric Project ordering.

The approved milestone sequence SHALL be control-plane API and job contracts,
analysis worker, frontend authentication shell, review and export, AWS
infrastructure, then end-to-end verification. For solo development, only the
next unblocked milestone SHALL be `Ready`; later milestones SHALL remain in
`Backlog`.

#### Scenario: Roadmap order is published
- **WHEN** a contributor views the versioned roadmap, milestone issues, or GitHub Project
- **THEN** each surface presents the same six-step implementation sequence and dependency gates

#### Scenario: Next milestone is selected
- **WHEN** no implementation milestone is in progress
- **THEN** issue #7 is `Ready` and issues #6, #8, #5, #4, and #3 remain in `Backlog`

#### Scenario: Milestone completes
- **WHEN** the current implementation milestone reaches `Done`
- **THEN** the next dependency-satisfied milestone may move to `Ready` while later milestones remain in `Backlog`
