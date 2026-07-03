## Why

Issue #38 moves the infrastructure milestone from emulator-only validation to a
real AWS account deployment path. The repository already models the AWS graph
and GitHub Actions OIDC entrypoints, but the live stack still needs the
standard Terragrunt env/region/component hierarchy, remote state, locking,
reviewed plan artifacts, and AWS-only smoke guidance.

## What Changes

- Configure the `infra/live/dev/eu-west-1/worker-compute-artifacts`
  Terragrunt stack to use S3 remote state and a DynamoDB lock table from
  environment-provided account configuration.
- Keep real AWS provider configuration free of Floci endpoint overrides and
  emulator-only credentials.
- Migrate the Floci live stack into the same env/region/component hierarchy
  while preserving local state and emulator provider settings.
- Harden the infrastructure workflow so AWS plans run on branch and pull
  request updates, manual plan/apply runs use GitHub OIDC, plan output is
  exposed as a CI artifact, and apply runs only after the `aws-production`
  environment gate approves the run.
- Add an AWS-only smoke entrypoint for services that Floci cannot fully
  emulate.
- Document required GitHub configuration, existing remote-state prerequisites,
  and the deferred budget-alert follow-up.

## Capabilities

### New Capabilities

### Modified Capabilities

- `infrastructure-foundation`: Add the real AWS remote-state, deployment, and
  AWS smoke contract that extends the emulator-only deployment boundary.

## Impact

- Updates Terragrunt configuration under `infra/root.hcl` and `infra/live`.
- Updates the infrastructure GitHub Actions workflow and Makefile entrypoints.
- Adds an AWS smoke script under repository tooling.
- Updates infrastructure and development documentation.
- Does not change runtime application APIs, worker behavior, or the Floci local
  validation path.
