# ADR 0001: Adopt documentation-as-code and GitHub governance

- **Status:** Accepted
- **Date:** 2026-06-14
- **Decision owners:** `@AlkaSaliss`

## Context

The repository has an approved technical scope but no reproducible
documentation toolchain, contribution metadata, continuous validation,
published documentation, or enforced GitHub workflow. Establishing these
controls before application code avoids retrofitting governance after
interfaces and infrastructure begin to change.

The repository is currently maintained by one collaborator. Independent review
cannot be required without blocking all merges.

## Decision

- Use GitHub Issues, Projects, pull requests, Wiki, Actions, and Dependabot for
  project collaboration.
- Use OpenSpec's spec-driven workflow for every non-trivial change.
- Use MkDocs with Material for MkDocs for authoritative versioned
  documentation, published through GitHub Pages.
- Use numbered MADR files under `docs/adr/` for durable architecture decisions.
- Require pull requests and current green quality checks for `main`, with zero
  required approvals while the project has one maintainer.
- Use squash-only merges and delete merged branches.
- Keep `.codex/` and `graphify-out/` as intentional versioned assets.
- License the public repository under Apache-2.0.

## Consequences

- Repository changes gain a consistent issue-to-spec-to-PR audit trail.
- Documentation and OpenSpec consistency become automated merge conditions.
- Solo development remains possible without bypassing CI.
- Committed Graphify output must be refreshed when its source corpus changes.
- Making the repository public exposes its current and future source history.

## Considered alternatives

- **Require one approval:** Rejected because the repository has only one
  collaborator and would become unmergeable.
- **Keep the repository private:** Rejected because free branch rules and Pages
  were required for the chosen workflow.
- **Use GitHub Wiki as canonical documentation:** Rejected because Wiki changes
  are not reviewed and versioned with implementation pull requests.
- **Do not commit Graphify output:** Rejected because the project explicitly
  treats the generated knowledge graph as a shared repository asset.

## References

- [GitHub Issue #1](https://github.com/AlkaSaliss/redact-all-the-things/issues/1)
- OpenSpec change: `gh-1-bootstrap-governance`
- [Technical scope](../architecture/technical-scope.md)
