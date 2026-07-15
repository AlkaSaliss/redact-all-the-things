# Infrastructure

The infrastructure milestone is delivered through issue #4 child slices. The
first slice establishes a Terragrunt and Terraform foundation that targets
Floci as an AWS-compatible emulator. The app edge/auth/API slice adds the
browser edge, authentication boundary, control-plane Lambda, and persistence
resources. The worker compute slice adds image storage, AWS Batch/Fargate Spot,
worker IAM, logs, isolated worker networking, and GitHub Actions validation and
manual AWS deployment entrypoints. Issue #38 moves the live stack into the
Terragrunt env/region/component hierarchy and uses reviewed real-account
deployment for the `dev` environment.

## Floci phase

The Floci phase uses:

- `eu-west-1` as the modeled AWS region.
- Local Terraform state.
- Fake local AWS credentials.
- `FLOCI_ENDPOINT_URL` as the AWS-compatible endpoint.
- `FLOCI_START_CMD` as an optional developer-provided startup command.

Run the Floci checks with:

```bash
make floci-check
make terragrunt-validate
make terragrunt-plan-local
make terragrunt-apply-local
```

`make floci-up` starts the local Floci AWS emulator with persistent local state.
`make terragrunt-plan` and `make terragrunt-apply` default to
`INFRA_TARGET=floci`; set `INFRA_TARGET=dev` or use `make terragrunt-plan-aws`
and `make terragrunt-apply-aws` for the real AWS live stack.

## GitHub Actions deployment

The `Infrastructure` workflow validates Terraform modules and Terragrunt HCL on
pushes to `main` or `feat/**` branches and on pull requests targeting `main`.
Those runs also plan the dev AWS live stack through GitHub Actions OIDC using
the `AWS_ROLE_TO_ASSUME` secret and `AWS_REGION` repository variable,
defaulting to `eu-west-1` when the variable is unset.

Automatic and manual `plan` runs execute `terragrunt plan` for
`infra/live/dev/eu-west-1/worker-compute-artifacts` and uploads the reviewed
plan artifact. Manual `apply` runs the same plan job first, then downloads and
applies that saved plan after the `aws-production` GitHub Environment gate
approves the run.

The real AWS workflow requires these repository or environment settings:

- `AWS_ROLE_TO_ASSUME` secret for the GitHub OIDC deployment role.
- `TG_STATE_BUCKET` variable or secret for the pre-created S3 state bucket.
- `TG_LOCK_TABLE` variable or secret for the pre-created DynamoDB lock table.
- Optional `AWS_REGION` and `TG_STATE_REGION` variables, both defaulting to
  `eu-west-1`.

## Validation boundary

Static Terraform and Terragrunt validation must not require a real AWS account.
Floci smoke checks verify only the services that the local emulator supports.
Later slices keep unsupported services in Terraform so the intended AWS graph is
reviewable, but their emulator coverage is documented separately from static
validation.

The app edge/auth/API module models:

- private S3 frontend and artifact buckets;
- 24-hour artifact lifecycle cleanup;
- DynamoDB job metadata with TTL;
- Cognito invited-user authentication resources;
- API Gateway HTTP API with a Cognito JWT authorizer;
- Lambda control-plane package wiring and runtime IAM;
- CloudFront frontend distribution with origin access control and an
  OAC-scoped S3 read policy;
- seven-day CloudWatch log retention.

Terraform creates a placeholder frontend object only to bootstrap the stack and
ignores its ETag after deployment so frontend publishing owns the live assets.
CloudFront maps S3 403/404 responses to `index.html` for OAuth callbacks and
client-side routes. The Lambda artifact is built from the checked-in
control-plane package before AWS planning/apply so the deployed function runs
`redact_api.lambda_handler.handler`.

The worker compute module composes the app edge/auth/API module and adds:

- an immutable ECR worker image repository with scan-on-push enabled;
- an AWS Batch Fargate Spot compute environment capped at 2 vCPU;
- a worker job queue sized for one active worker globally;
- separate `analyze` and `render` job definitions;
- task execution and worker job roles for image pulls, logs, artifacts, and
  job metadata;
- seven-day worker CloudWatch log retention;
- a small worker VPC, public worker subnets with outbound Internet Gateway
  routing, and a no-ingress security group;
- real worker image commands for `redact_api.worker_runtime` analyze and render
  modes.

Batch, Fargate, ECR, and worker networking coverage depends on the configured
Floci-compatible emulator. When those services are unsupported, static
Terraform validation and plan review are the authoritative checks for this
slice.

The modules use `deployment_mode` to select emulator compatibility. In
`floci` mode, the live stack disables CloudFront distribution creation and uses
a module-defined Batch service-role policy because Floci does not currently
provide a CloudFront response compatible with AWS provider readback or preload
the AWS-managed Batch service policy. In `aws` mode, the AWS live stack omits
endpoint overrides, enables CloudFront, and uses the AWS-managed
`AWSBatchServiceRole` attachment.

## Remote state

The S3 state bucket and DynamoDB lock table already exist outside this
repository. The real AWS live stack consumes those resources through
`TG_STATE_BUCKET`, `TG_LOCK_TABLE`, and optional `TG_STATE_REGION`; this
repository does not provision or bootstrap them.

## Real AWS deployment

The Floci live stack keeps local state, fake credentials, and AWS-compatible
endpoint overrides. The AWS live stack uses S3 remote state, DynamoDB locking,
the default AWS provider, and no emulator endpoint overrides. Both stacks use
the same env/region/component hierarchy:

- `infra/live/floci/eu-west-1/worker-compute-artifacts`
- `infra/live/dev/eu-west-1/worker-compute-artifacts`

Use the AWS smoke check after an approved apply:

```bash
make infra-smoke-aws
```

The smoke check reads Terragrunt outputs from the real AWS live stack and
verifies deployed DynamoDB, S3, Batch, ECR, and Lambda resources that Floci
cannot fully cover. It is read-only by default and expects credentials for the
approved account.

To run the mutating runtime smoke that invokes the real Lambda and exercises a
valid sample through multipart upload, Batch analysis, export rendering, and
authorized result download:

```bash
AWS_E2E_SMOKE=1 make infra-smoke-aws
```

The smoke polls the owner-scoped control-plane job contract with a 30-minute
deadline and fails on safe terminal failure codes. Presigned transfer errors
include the S3 response body for diagnosis but never log signed URLs. Browser
verification separately checks that the CloudFront React entry page starts the
Cognito hosted sign-in flow; invited-user credentials remain outside the
repository.

Issue #38 revalidates the `eu-west-1` cost model before apply. Terraform-managed
AWS budget alerts are deferred to follow-up issue #42 because alert notification
targets are account-specific and are not committed to this repository.
