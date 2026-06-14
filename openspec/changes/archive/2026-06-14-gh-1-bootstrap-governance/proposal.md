## Why

The repository has an approved product scope and working agreement but lacks
the tooling, documentation structure, automation, and GitHub configuration
needed to apply that agreement consistently. Establishing those controls now
keeps later application and infrastructure changes reproducible, reviewable,
and documented from their first pull request.

## What Changes

- Add a reproducible Python-based documentation toolchain using uv, MkDocs, and
  Material for MkDocs.
- Establish versioned project documentation, contribution guidance, security
  reporting, and MADR architecture decision records.
- Add GitHub issue and pull request templates, CODEOWNERS, Dependabot, quality
  checks, and GitHub Pages deployment.
- Update the working agreement for solo development, intentional tracking of
  agent and Graphify assets, and OpenSpec archival before merge.
- Configure the GitHub repository for public visibility, squash-only merges,
  security alerts, Wiki, Pages, protected `main`, and a project roadmap.
- Seed implementation roadmap issues without creating application,
  container, or infrastructure runtime code.

## Capabilities

### New Capabilities

- `repository-governance`: Reproducible documentation tooling, contribution
  workflow, CI/CD checks, security automation, repository settings, and roadmap
  management.

### Modified Capabilities

None.

## Impact

- Adds root tooling and governance files, versioned documentation, GitHub
  metadata, and Actions workflows.
- Moves the existing technical scope into the published documentation tree.
- Updates `AGENTS.md`, `.codex/` workflow expectations, and committed
  `graphify-out/` artifacts.
- Changes GitHub repository visibility and settings, creates a Project, and
  creates roadmap Issues.
- Introduces no application API, runtime service, container, or AWS
  infrastructure implementation.
