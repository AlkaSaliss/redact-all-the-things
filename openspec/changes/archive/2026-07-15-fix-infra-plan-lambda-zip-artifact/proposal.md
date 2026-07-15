## Why

Real AWS plans report a Lambda update when the only difference is the local or
CI filesystem path used for the generated control-plane ZIP. That makes plan
review noisy and obscures real package-content changes.

## What Changes

- Stage the Lambda ZIP in a private S3 deployment bucket.
- Build deterministic Lambda ZIP files for unchanged package inputs.
- Keep the Lambda package content hash as the deployment trigger while removing
  local filesystem paths from Lambda function state.
- Default local AWS plans to the current git commit worker image tag instead
  of `local`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `infrastructure-app-edge-auth-api`: Lambda deployment uses a stable package
  artifact instead of caller-specific ZIP paths.

## Impact

- Affects the app edge/auth/API Terraform module and adds a private Lambda
  package bucket/object.
- Affects Makefile plan/apply defaults for the worker image tag.
- No runtime API, data model, or dependency changes.
