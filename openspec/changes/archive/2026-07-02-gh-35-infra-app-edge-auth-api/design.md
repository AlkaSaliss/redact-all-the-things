## Context

Issue #34 added a foundation-only Floci Terragrunt environment. Issue #35 must
model the app-facing infrastructure from the technical scope while keeping
deployment behavior emulator-only. The product frontend, auth shell, and final
control-plane packaging are not complete yet, so this slice uses minimal stubs
only to exercise infrastructure wiring.

## Decisions

### Compose the existing foundation module

Create `infra/modules/app-edge-auth-api` and invoke the existing foundation
module from it. The Floci Terragrunt live config will source this module, so
later slices can extend the same live environment without deleting the
foundation contract.

### Model full app-facing AWS resources

Define resources for S3 frontend hosting and artifact storage, DynamoDB job
metadata with TTL, Cognito user pool and app client, API Gateway HTTP API with a
Cognito JWT authorizer, Lambda integration and permission, CloudWatch logs,
CloudFront distribution with origin access control, and IAM roles/policies for
Lambda.

### Keep stubs visibly temporary

Add a static HTML placeholder and a minimal Lambda ZIP generated from checked-in
stub source. These are infrastructure fixtures only. Product UI and API
behavior remain owned by their application slices.

### Keep emulator smoke honest

`infra-smoke-floci` will continue to require `FLOCI_ENDPOINT_URL` and will
validate static configuration plus supported endpoint reachability. It will not
claim that CloudFront, Cognito, API Gateway, or Lambda are fully emulated unless
Floci supports them in the developer environment.

## Risks

- Some AWS resources in this module may not be creatable in Floci. Static
  Terraform validation remains the reliable check; Floci apply/smoke is
  best-effort for supported services.
- API Gateway and Cognito wiring depends on final frontend/auth behavior. This
  slice models the boundary but does not implement product flows.
- Lambda packaging is intentionally minimal and should be replaced by the
  control-plane deployment workflow in later slices.

## Rollout

1. Add app edge/auth/API module and stub assets.
2. Point the Floci live config at the new module.
3. Update Make validation to cover every infrastructure module.
4. Update docs and smoke guidance.
5. Validate OpenSpec, docs, Terraform/Terragrunt, and tests.
