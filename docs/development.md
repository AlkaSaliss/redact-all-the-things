# Development workflow

This repository uses GitHub for collaboration, OpenSpec for change definition
and implementation tracking, and MkDocs for versioned documentation.

## Prerequisites

- Git
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Node.js with OpenSpec `1.4.1`
- Graphify when changing indexed source or architecture content

## Install tooling

```bash
uv sync --locked
uv run pre-commit install
```

## Change lifecycle

1. Create or link a GitHub Issue.
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
uv run mkdocs build --strict
openspec validate --all --strict --no-interactive
```

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
