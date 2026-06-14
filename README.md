# Redact All The Things

Redact All The Things is an assisted redaction application for PDFs and images.
It will use PaddleOCR and GLiNER2 to suggest textual PII regions, require human
review, and export permanently rasterized redacted files.

The repository currently contains the approved technical scope and project
tooling. Application and AWS runtime implementation is tracked separately on
the GitHub roadmap.

## Documentation

The project documentation is built with MkDocs and Material for MkDocs:

- [Published documentation](https://alkasaliss.github.io/redact-all-the-things/)
- [Technical scope](docs/architecture/technical-scope.md)
- [Development workflow](docs/development.md)
- [Architecture decisions](docs/adr/index.md)

## Local setup

Install the locked repository tooling:

```bash
uv sync --locked
```

Run the validation suite:

```bash
uv run pre-commit run --all-files
uv run mkdocs build --strict
openspec validate --all --strict --no-interactive
```

Preview documentation locally:

```bash
uv run mkdocs serve
```

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) before
starting work. Non-trivial changes use the GitHub Issue → OpenSpec → pull
request lifecycle.

## Security

Do not open public issues for vulnerabilities. Follow
[SECURITY.md](SECURITY.md) for private reporting.

## License

Licensed under the [Apache License 2.0](LICENSE).
