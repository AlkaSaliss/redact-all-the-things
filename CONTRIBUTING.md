# Contributing

Thank you for contributing to Redact All The Things.

## Before starting

Read:

- [AGENTS.md](AGENTS.md) for the complete working agreement;
- [development workflow](docs/development.md);
- [technical scope](docs/architecture/technical-scope.md).

## Workflow

1. Create or select a GitHub Issue.
2. Create a branch named `<type>/<issue-number>-<slug>`.
3. For non-trivial work, create OpenSpec change
   `gh-<issue-number>-<slug>` and complete its artifacts.
4. Implement the smallest change satisfying the Issue and OpenSpec artifacts.
5. Add or update tests, documentation, and ADRs as required.
6. Refresh Graphify when indexed source or architecture content changes.
7. Run local validation.
8. Open a pull request containing `Closes #<issue-number>`.
9. Verify and archive the OpenSpec change before merge.
10. Squash merge only after required checks pass.

## Local checks

```bash
uv sync --locked
uv run pre-commit run --all-files
uv run mkdocs build --strict
openspec validate --all --strict --no-interactive
```

## Pull requests

Keep pull requests focused. Explain:

- what changed and why;
- the linked Issue and OpenSpec change;
- tests and checks run;
- documentation and ADR impact;
- Graphify impact.

The project currently permits solo merges after required checks pass. Reviewer
approval may be introduced when additional maintainers join.
