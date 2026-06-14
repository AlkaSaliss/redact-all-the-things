## Context

The repository currently contains the product technical scope, an empty README,
the OpenSpec Codex skills, and generated Graphify output. It has no
documentation build, dependency lock, contribution guidance, GitHub templates,
CI, Pages deployment, Dependabot configuration, branch rules, or roadmap.

The project is currently maintained by one GitHub collaborator. The repository
will become public, use pull requests and required automated checks, and permit
the owner to merge after checks pass without a separate approval.

## Goals / Non-Goals

**Goals:**

- Make documentation and governance reproducible locally and in CI.
- Publish versioned project documentation through GitHub Pages.
- Enforce pull-request-only changes and a required quality check on `main`.
- Enable dependency and security automation.
- Establish issue, ADR, OpenSpec, Graphify, and roadmap conventions.
- Seed the next implementation milestones as separate issues.

**Non-Goals:**

- Scaffold frontend, backend, worker, container, or AWS infrastructure code.
- Define application runtime dependencies or service APIs.
- Require a second reviewer for a solo-maintained repository.

## Decisions

### Use uv for repository tooling

The root `pyproject.toml` will define a Python 3.12 project with a development
dependency group containing exact MkDocs, Material, pre-commit, Markdown lint,
and YAML lint versions. `uv.lock` will be committed and CI will use
`uv sync --locked`.

This provides one reproducible toolchain without introducing application Python
packaging. Requirements files were rejected because dependency groups and a
lock file provide clearer future growth.

### Publish documentation from `docs/`

MkDocs will publish a small, navigable site containing the project overview,
development workflow, technical scope, ADR index, MADR template, and ADR 0001.
The existing scope will move to `docs/architecture/technical-scope.md` so there
is one canonical version.

GitHub Wiki remains supplementary. Its home page will point contributors to the
versioned documentation for authoritative behavior and architecture.

### Keep agent and Graphify assets versioned

`.codex/` and `graphify-out/` are intentional repository assets, overriding the
general generated/local-file exclusion. Changes to indexed source or
architecture documents require `graphify --update` or a full regeneration, and
the updated report and graph are committed with the source change.

### Use one required quality workflow

The `Quality` workflow will run pre-commit, strict MkDocs, and strict OpenSpec
validation. A separate Pages workflow will build and deploy the site from
`main`. Branch rules will require pull requests and the observed Quality check
context, with zero approvals.

### Configure GitHub as part of bootstrap

The repository will become public under Apache-2.0, enable Wiki, Pages,
vulnerability alerts, and automated security fixes, allow squash merges only,
and delete merged branches. A GitHub Project will use Backlog, Ready, In
Progress, In Review, and Done.

## Risks / Trade-offs

- **Public visibility exposes project history and future source** -> Review the
  tracked tree for secrets before changing visibility and keep secret scanning
  enabled.
- **Zero approvals reduces independent review** -> Require pull requests,
  current green checks, and complete OpenSpec verification.
- **Committed Graphify output can become stale** -> Add an explicit refresh
  rule and PR checklist item.
- **Pages and branch rules depend on workflow check names** -> Apply the ruleset
  only after the first workflow run reveals the exact check context.
- **GitHub Projects requires extra CLI scopes** -> Refresh authentication before
  creating or updating the Project.
- **Archiving OpenSpec before merge changes the PR late** -> Verify first,
  archive as the final content commit, and rerun required checks.

## Migration Plan

1. Create the issue, branch, and OpenSpec artifacts.
2. Add repository tooling, documentation, and GitHub metadata.
3. Regenerate Graphify and run all checks locally.
4. Commit, push, open the PR, and make the repository public.
5. Enable remote security, Wiki, Pages, merge, Project, and roadmap settings.
6. Observe CI, configure the required `main` ruleset, verify OpenSpec, archive
   the change, rerun CI, and squash merge.
7. Confirm Pages, Issue, Project, rules, and security status.

Rollback consists of reverting the bootstrap PR and restoring the prior
repository visibility and settings through the GitHub API.

## Open Questions

None.
