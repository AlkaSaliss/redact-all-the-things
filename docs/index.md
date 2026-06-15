# Redact All The Things

Redact All The Things is an assisted file-redaction application for PDFs,
JPEGs, and PNGs. It combines OCR and PII detection with a mandatory human
review step before producing a permanently rasterized redacted output.

The project is implementing the roadmap incrementally through separate GitHub
Issues and OpenSpec changes. The Python control-plane contracts are the first
application milestone.

## Project principles

- Process sensitive files only inside the project's AWS account.
- Prefer scale-to-zero infrastructure and bounded concurrency.
- Treat automatic detection as assistance, not a substitute for review.
- Keep requirements, architecture, code, tests, and documentation aligned.
- Deliver every non-trivial change through GitHub Issues, OpenSpec, and pull
  requests.

## Start here

- Follow the [implementation roadmap](roadmap.md).
- Read the [technical scope](architecture/technical-scope.md).
- Review the [control-plane API](architecture/control-plane-api.md).
- Follow the [development workflow](development.md).
- Review the [architecture decisions](adr/index.md).
- Use the [GitHub repository](https://github.com/AlkaSaliss/redact-all-the-things)
  for issues, roadmap, and pull requests.
