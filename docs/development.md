# Development workflow

This repository uses GitHub for collaboration, OpenSpec for change definition
and implementation tracking, and MkDocs for versioned documentation.

## Prerequisites

- Git
- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Docker with Compose
- Node.js with OpenSpec `1.4.1`
- Terraform `1.13.3` and Terragrunt `0.87.6` for infrastructure work
- Graphify when changing indexed source or architecture content

## Install tooling

```bash
uv sync --locked
uv run pre-commit install
docker compose up -d floci
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

The test suite uses pinned Floci services for DynamoDB and S3. See the
[control-plane API documentation](architecture/control-plane-api.md) for the
local AWS boundary and the rationale for using a recording Batch fake.

Infrastructure work uses Floci as an AWS-compatible emulator during issue #4
child slices. Set `FLOCI_ENDPOINT_URL` before running Floci plan, apply, or
smoke targets:

```bash
export FLOCI_ENDPOINT_URL=http://127.0.0.1:4566
make floci-check
make terragrunt-validate
make terragrunt-plan-local
```

`make floci-up` starts the local Floci AWS emulator with persistent state.
Terraform state remains local for the Floci environment.

The `Infrastructure` GitHub Actions workflow runs `make terragrunt-validate`
for infrastructure pull requests. Manual workflow dispatch can run an AWS plan
or apply against `infra/live/aws` after configuring:

- `AWS_ROLE_TO_ASSUME` as a repository or environment secret;
- `TG_STATE_BUCKET` as a repository variable or secret;
- `TG_LOCK_TABLE` as a repository variable or secret;
- optional `AWS_REGION` and `TG_STATE_REGION` variables, defaulting to
  `eu-west-1`;
- the `aws-production` environment approval gate.

The S3 state bucket and DynamoDB lock table are provisioned by the
`infra/modules/remote-state` module. Deploy them first using the
`Remote State Bootstrap` GitHub Actions workflow (same OIDC role and
`aws-production` gate), or locally:

```bash
make terragrunt-plan-remote-state
make terragrunt-apply-remote-state
make infra-smoke-remote-state
```

After the bootstrap, set `TG_STATE_BUCKET` and `TG_LOCK_TABLE` to the values
output by the remote-state stack. Manual plan runs upload the reviewed
Terraform plan artifact. Manual apply runs download that artifact and apply it
only after the protected environment approves the apply job.

After an approved apply, run the read-only production smoke check from a shell
that has AWS credentials for the approved account:

```bash
export TG_STATE_BUCKET=<state-bucket>
export TG_LOCK_TABLE=<lock-table>
export AWS_REGION=eu-west-1
make infra-smoke-aws
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
