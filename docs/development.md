# Development workflow

This repository uses GitHub for collaboration, OpenSpec for change definition
and implementation tracking, and MkDocs for versioned documentation.

## Prerequisites

- Git
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Docker with Compose
- Node.js with OpenSpec `1.4.1`
- Graphify when changing indexed source or architecture content

## Install tooling

```bash
uv sync --locked
uv run pre-commit install
docker compose up -d localstack
```

## Work item model

Roadmap milestone issues are parent epics. They hold context, dependency gates,
and child issue checklists. They are not the normal unit for implementation
OpenSpec changes.

Implementation-slice child issues are the delivery unit. A slice should fit in
one to two days of focused work and produce one reviewable pull request.
Non-trivial implementation slices require OpenSpec artifacts.

For solo development, keep only one dependency-satisfied child issue in
`Ready` or `In Progress`. Keep later child issues in `Backlog`.

## Change lifecycle

1. Create or link a GitHub Issue. For roadmap work, use an implementation-slice
   child issue linked to its parent epic.
2. Create a branch named `<type>/<issue-number>-<slug>`.
3. Create an OpenSpec change named `gh-<issue-number>-<slug>`.
4. Complete proposal, specs, design, and tasks before implementation.
5. Implement tasks with tests and documentation.
6. Refresh Graphify when indexed source or architecture changes.
7. Run OpenSpec verification.
8. Archive the OpenSpec change as the final content update.
9. Open or update the pull request and merge only after required checks pass.

## Local validation

Run the same checks used by CI:

```bash
uv sync --locked
uv run pre-commit run --all-files
uv run pytest
uv run mkdocs build --strict
openspec validate --all --strict --no-interactive
```

The test suite uses pinned LocalStack services for DynamoDB and S3. See the
[control-plane API documentation](architecture/control-plane-api.md) for the
local AWS boundary and Batch testing limitation.

Preview the documentation:

```bash
uv run mkdocs serve
```

## Documentation requirements

Repository documentation is authoritative for shipped behavior and
architecture. The GitHub Wiki is supplementary.

A feature pull request is incomplete unless it updates:

- implementation and tests;
- relevant MkDocs pages;
- OpenSpec artifacts;
- an ADR when architecture changes;
- Graphify output when indexed content changes.

## Architecture decisions

Create numbered MADR files under `docs/adr/`. Copy
[`template.md`](adr/template.md), choose the next four-digit number, and link
the related Issue, OpenSpec change, and pull request.
