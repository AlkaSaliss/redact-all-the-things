# Infrastructure

The infrastructure milestone is delivered through issue #4 child slices. The
first slice establishes a Terragrunt and Terraform foundation that targets
Floci as an AWS-compatible emulator. The app edge/auth/API slice adds the
browser edge, authentication boundary, control-plane Lambda, and persistence
resources. The worker compute slice adds image storage, AWS Batch/Fargate Spot,
worker IAM, logs, isolated worker networking, and GitHub Actions validation and
manual AWS deployment entrypoints.

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
`INFRA_TARGET=floci`; set `INFRA_TARGET=aws` or use `make terragrunt-plan-aws`
and `make terragrunt-apply-aws` for the real AWS live stack.

## GitHub Actions deployment

The `Infrastructure` workflow validates Terraform modules and Terragrunt HCL on
pull requests and pushes that touch infrastructure files. Manual dispatch runs
the AWS live stack through GitHub Actions OIDC using the
`AWS_ROLE_TO_ASSUME` secret and `AWS_REGION` repository variable, defaulting to
`eu-west-1` when the variable is unset.

Manual `plan` runs only `terragrunt plan` for `infra/live/aws`. Manual `apply`
runs the same plan job first and then applies the AWS live stack after the
`aws-production` GitHub Environment gate approves the run.

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
- Lambda control-plane stub wiring and least-privilege IAM;
- CloudFront frontend distribution with origin access control;
- seven-day CloudWatch log retention.

The frontend and Lambda artifacts are placeholders. They exist only so the
infrastructure graph has deployable references before the frontend and
control-plane deployment slices provide real artifacts.

The worker compute module composes the app edge/auth/API module and adds:

- an immutable ECR worker image repository with scan-on-push enabled;
- an AWS Batch Fargate Spot compute environment capped at 2 vCPU;
- a worker job queue sized for one active worker globally;
- separate `analyze` and `render` job definitions;
- task execution and worker job roles for image pulls, logs, artifacts, and
  job metadata;
- seven-day worker CloudWatch log retention;
- a small worker VPC, private worker subnets, and a no-ingress security group;
- a temporary infrastructure-only worker stub under `infra/stubs/worker`.

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

## Real AWS migration

Issue #38 owns the later hardening from the local AWS live stack to the final
production account workflow. That work will add remote state and locking,
replace any temporary bootstrap role configuration with the final account
layout, and revalidate the `eu-west-1` cost model.
