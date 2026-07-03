## Why

Issue #38 moves the infrastructure milestone from emulator-only validation to a
real AWS account deployment path. The repository already models the AWS graph
and GitHub Actions OIDC entrypoints, but the AWS live stack still lacks remote
state, locking, reviewed plan artifacts, and production-only smoke guidance.

## What Changes

- Configure the `infra/live/aws` Terragrunt stack to use S3 remote state and a
  DynamoDB lock table from environment-provided account configuration.
- Keep production AWS provider configuration free of Floci endpoint overrides
  and emulator-only credentials.
- Harden the manual infrastructure workflow so AWS plan and apply use GitHub
  OIDC, expose plan output as a CI artifact, and apply only after the
  `aws-production` environment gate approves the run.
- Add an AWS-only smoke entrypoint for services that Floci cannot fully
  emulate.
- Document required GitHub configuration, remote-state bootstrap
  prerequisites, and the deferred budget-alert follow-up.

## Capabilities

### New Capabilities

### Modified Capabilities

- `infrastructure-foundation`: Add the real AWS remote-state, deployment, and
  production smoke contract that replaces the emulator-only deployment boundary.

## Impact

- Updates Terragrunt configuration under `infra/live/aws`.
- Updates the infrastructure GitHub Actions workflow and Makefile entrypoints.
- Adds a production smoke script under repository tooling.
- Updates infrastructure and development documentation.
- Does not change runtime application APIs, worker behavior, or the Floci local
  validation path.
