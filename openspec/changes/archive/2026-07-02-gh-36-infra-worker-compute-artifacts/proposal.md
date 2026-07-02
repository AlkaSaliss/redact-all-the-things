## Why

The Floci stack now models the app edge, auth, API, and persistence resources,
but it still lacks worker image storage, queueing, and compute infrastructure
for asynchronous analysis and render jobs. Issue #36 adds the worker
infrastructure shape needed by the control plane while keeping emulator
coverage honest.

## What Changes

- Add a worker compute/artifacts Terraform module that composes the app
  edge/auth/API module.
- Model ECR worker image storage, AWS Batch on Fargate Spot, a one-worker job
  queue, analyze/render job definitions, worker IAM, CloudWatch logs, and
  worker network resources.
- Add a minimal worker container stub for infrastructure wiring until the final
  worker image pipeline owns the deployable artifact.
- Update Floci Terragrunt to source the worker compute module.
- Update docs and smoke output to describe static validation versus emulator
  coverage for Batch/Fargate/ECR.

## Capabilities

### New Capabilities

- `infrastructure-worker-compute-artifacts`: Worker image, Batch/Fargate Spot,
  queueing, IAM, logs, and artifact access infrastructure.

### Modified Capabilities

- `infrastructure-app-edge-auth-api`: Expose app resource ARNs needed by worker
  IAM policies.
- `infrastructure-foundation`: Floci smoke guidance now includes worker
  compute coverage boundaries.

## Impact

- Adds `infra/modules/worker-compute-artifacts`.
- Updates the Floci live module source and provider endpoints.
- Adds a minimal worker stub under `infra/stubs`.
- Does not change runtime worker behavior, control-plane application code,
  production deployment workflows, or real AWS remote state.
