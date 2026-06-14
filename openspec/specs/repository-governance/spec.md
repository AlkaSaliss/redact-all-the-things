# Repository Governance Specification

## Purpose

Define the reproducible tooling, documentation, automation, contribution
controls, and roadmap practices required before application development begins.

## Requirements

### Requirement: Reproducible repository tooling
The repository SHALL define a Python 3.12 tooling environment in
`pyproject.toml`, commit its uv lock file, and provide pre-commit checks for
repository text and configuration files.

#### Scenario: Install locked tooling
- **WHEN** a contributor runs `uv sync --locked`
- **THEN** the documented MkDocs and repository validation tools install without changing the lock file

### Requirement: Versioned project documentation
The repository SHALL publish authoritative project documentation with MkDocs
and Material for MkDocs, including development guidance, the technical scope,
and architecture decision records.

#### Scenario: Build documentation locally
- **WHEN** a contributor runs the documented strict MkDocs build command
- **THEN** the complete documentation site builds without warnings

### Requirement: Architecture decision records
Architecture changes SHALL add or supersede numbered MADR documents under
`docs/adr/` containing status, context, decision, consequences, considered
alternatives, and references.

#### Scenario: Record bootstrap architecture
- **WHEN** repository governance and documentation architecture are introduced
- **THEN** ADR 0001 records the decisions and links to the bootstrap issue and OpenSpec change

### Requirement: Automated pull request quality
GitHub Actions SHALL validate locked dependencies, pre-commit checks, strict
MkDocs output, and strict OpenSpec artifacts for pull requests and `main`.

#### Scenario: Pull request changes repository content
- **WHEN** a pull request updates tracked files
- **THEN** the Quality workflow reports a required pass or failure before merge

### Requirement: Published documentation
GitHub Actions SHALL deploy the strict MkDocs build to GitHub Pages after
successful changes reach `main`.

#### Scenario: Documentation reaches main
- **WHEN** a commit is merged into `main`
- **THEN** the Pages workflow publishes the current versioned documentation

### Requirement: Repository contribution metadata
The repository SHALL provide structured bug and feature issue forms, a pull
request checklist, CODEOWNERS, contribution guidance, security reporting
instructions, and an Apache-2.0 license.

#### Scenario: Contributor proposes a change
- **WHEN** a contributor opens an issue or pull request
- **THEN** GitHub presents templates that require scope, validation, documentation, ADR, OpenSpec, and Graphify impact

### Requirement: Dependency and security automation
The repository SHALL configure Dependabot for Python tooling and GitHub Actions
and enable GitHub vulnerability alerts and automated security fixes.

#### Scenario: Supported dependency update exists
- **WHEN** GitHub detects an eligible dependency or vulnerable version
- **THEN** Dependabot can propose or apply the configured update

### Requirement: Protected main workflow
The public repository SHALL require pull requests and the current Quality check
for `main`, block force pushes and deletion, allow zero required approvals for
solo development, and use squash-only merges with branch deletion.

#### Scenario: Owner merges a change
- **WHEN** the pull request is current with `main` and the required Quality check passes
- **THEN** the owner can squash merge without a separate reviewer approval

### Requirement: Tracked agent knowledge assets
The repository SHALL treat `.codex/` and `graphify-out/` as intentional tracked
assets and require Graphify regeneration when indexed source or architecture
content changes.

#### Scenario: Architecture documentation changes
- **WHEN** a pull request changes indexed architecture or source content
- **THEN** the pull request includes refreshed Graphify output or explains why no refresh is needed

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
