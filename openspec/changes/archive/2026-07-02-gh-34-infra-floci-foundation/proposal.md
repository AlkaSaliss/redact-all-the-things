## Why

Issue #4 now needs an early infrastructure foundation so the AWS target can be
validated against the Floci AWS-compatible emulator before the remaining
application slices are complete. The repository currently has no Terraform or
Terragrunt structure, no Floci endpoint contract, and no local commands for
infrastructure validation.

## What Changes

- Add a Terragrunt/Terraform foundation for the `eu-west-1` Floci phase.
- Configure the AWS provider through `FLOCI_ENDPOINT_URL` and fake local AWS
  credentials while keeping Terraform state local.
- Add Make targets for starting/checking Floci and running Terragrunt
  validation, plan, apply, and smoke entrypoints.
- Add documentation for the approved roadmap override, emulator-only boundary,
  local state, and later real-AWS migration.
- Keep service-specific AWS resources, deployable application stubs, CI
  workflows, and production remote state for later issue #4 child slices.

## Capabilities

### New Capabilities

- `infrastructure-foundation`: Terragrunt/Terraform foundation and local Floci
  validation contract for AWS infrastructure work.

### Modified Capabilities

- `repository-governance`: Document the approved exception that issue #4 child
  infrastructure slices may start before the prior roadmap prerequisites are
  complete, while preserving per-issue OpenSpec and PR workflow.

## Impact

- Adds `infra/` Terragrunt/Terraform scaffold and validation scripts.
- Extends the Makefile with infrastructure targets.
- Updates architecture, roadmap, and development documentation.
- Does not change runtime application APIs, worker behavior, production AWS
  deployment, or existing LocalStack-backed tests.
