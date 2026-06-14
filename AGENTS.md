# Project Working Agreement

This file applies recursively to the entire repository. All contributors and
agents must follow it unless a more specific `AGENTS.md` exists in a
subdirectory.

## Collaboration Platform

Use GitHub as the project collaboration platform:

| Need | Tool |
| --- | --- |
| Codebase | GitHub repository |
| Ticketing | GitHub Issues |
| Board and roadmap | GitHub Projects |
| Code review and merge | GitHub Pull Requests |
| Exploratory and long-form notes | GitHub Wiki |
| CI/CD | GitHub Actions |
| Dependency and security updates | Dependabot |

GitHub Projects uses these states:

`Backlog -> Ready -> In Progress -> In Review -> Done`

Repository documentation is authoritative for shipped behavior, operations,
and architecture. The Wiki is supplementary and may hold exploratory notes or
collaborative knowledge, but it must not replace versioned documentation or
architecture decision records.

## Change Workflow

Use OpenSpec for the specification and implementation of every non-trivial
change.

A non-trivial change affects runtime behavior, public or internal APIs, data
models, infrastructure, security, dependencies, or architecture. Typo-only and
similarly mechanical documentation fixes may skip OpenSpec, but they still
require an issue branch and pull request.

For non-trivial work:

1. Create or link a GitHub Issue and ensure the work is represented in GitHub
   Projects.
2. Move the issue to `In Progress`.
3. Create an OpenSpec change named `gh-<issue-number>-<slug>`.
4. Complete the OpenSpec proposal, specs, design, and tasks before
   implementation.
5. Implement the tasks incrementally, updating tests and documentation with
   the code.
6. Run OpenSpec verification and resolve critical findings before requesting
   review.
7. Open a pull request containing `Closes #<issue-number>` and move the issue
   to `In Review`.
8. Run OpenSpec verification, resolve critical findings, and archive the
   OpenSpec change as the final content update in the pull request.
9. Merge only after all required CI checks pass on the archived change, then
   move the issue to `Done`.

Do not bypass required checks. Solo maintainers may merge their own pull
requests after all required checks pass.

## Git Conventions

The protected default branch is `main`. Work on an issue branch named:

`<type>/<issue-number>-<slug>`

Examples:

- `feat/123-upload-flow`
- `fix/148-expired-download`
- `docs/172-redaction-guide`
- `chore/190-update-dependencies`

Use descriptive commit messages. Conventional Commits are not required.

## Documentation as Code

Use MkDocs with Material for MkDocs for versioned project documentation.

- Validate the MkDocs build on every pull request.
- Publish the documentation to GitHub Pages after merges to `main`.
- Update the relevant documentation in the same pull request as the behavior
  it describes.
- Treat a feature pull request as incomplete unless it includes the relevant
  code, tests, documentation, and architecture decision record when required.

Record architecture decisions as numbered MADR documents under `docs/adr/`.
Each ADR must include:

- Status
- Context
- Decision
- Consequences
- Considered alternatives
- References

When a decision changes, supersede the previous ADR rather than rewriting its
history.

## Definition of Done

A pull request is complete only when:

- Tests cover the changed behavior and pass locally and in CI.
- Relevant MkDocs pages are updated.
- Architecture changes add or supersede a numbered ADR under `docs/adr/`.
- OpenSpec artifacts match the implementation and verification is complete.
- The pull request explains its scope, testing, documentation impact, ADR
  impact, and linked issue.
- All required CI checks pass.
- OpenSpec verification is complete and the change is archived.

Generated output and local tooling must not be committed unless the repository
explicitly treats them as shared assets or the issue requires them.

This repository intentionally versions:

- `.codex/`, which contains the project's OpenSpec agent workflows.
- `graphify-out/`, which contains the shared project knowledge graph.

Refresh Graphify when indexed source or architecture documentation changes.
Commit the refreshed report and graph with the source change. If no refresh is
needed, explain why in the pull request.

## Engineering Guidance

Before changing files:

- Inspect the repository, existing guidance, and current OpenSpec state.
- State assumptions and surface material ambiguity or tradeoffs.
- Convert the requested outcome into verifiable checks.

While implementing:

- Prefer the smallest change that satisfies the issue and OpenSpec artifacts.
- Avoid unrelated refactoring, formatting churn, and speculative features.
- Preserve changes made by others.
- Follow existing project patterns when they exist.
- Update OpenSpec task checkboxes as each task is completed.

Before finishing:

- Run the relevant tests, static checks, and documentation build.
- Review the diff for unrelated or generated files.
- Verify implementation, tests, documentation, and ADRs remain consistent.
- Report any checks that could not be run.
