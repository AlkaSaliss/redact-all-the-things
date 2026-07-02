## Why

The Floci foundation exists, but the infrastructure stack still does not model
the application edge, authentication boundary, control-plane API, or persistence
resources required by the technical scope. Issue #35 adds those resources and
minimal deployable stubs so later slices can wire worker compute and deployment
automation without inventing the app-facing infrastructure shape.

## What Changes

- Add an app edge/auth/API Terraform module that composes the existing
  infrastructure foundation module.
- Model frontend S3 hosting, artifact S3 storage, DynamoDB job metadata,
  Cognito, API Gateway HTTP API, Lambda, CloudWatch logs, CloudFront origin
  access control, and least-privilege IAM.
- Add minimal frontend and Lambda stub artifacts used only for infrastructure
  wiring during the Floci phase.
- Update Floci Terragrunt live configuration to target the app edge/auth/API
  module.
- Extend infrastructure docs and smoke checks with emulator coverage boundaries
  for this slice.

## Capabilities

### New Capabilities

- `infrastructure-app-edge-auth-api`: App edge, authentication, control-plane,
  and persistence infrastructure modeled for the Floci phase.

### Modified Capabilities

- `infrastructure-foundation`: Floci developer validation now includes
  app-edge/auth/API smoke coverage for supported emulator resources.

## Impact

- Adds a new Terraform module and minimal stub assets under `infra/`.
- Updates Terragrunt live source for the Floci environment.
- Updates infrastructure smoke scripts and documentation.
- Does not change Python runtime behavior, public API contracts, worker
  processing, frontend product implementation, production AWS remote state, or
  CI deployment workflows.
