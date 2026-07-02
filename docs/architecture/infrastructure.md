# Infrastructure

The infrastructure milestone is delivered through issue #4 child slices. The
first slice establishes a Terragrunt and Terraform foundation that targets
Floci as an AWS-compatible emulator. The app edge/auth/API slice adds the
browser edge, authentication boundary, control-plane Lambda, and persistence
resources. The worker compute slice adds image storage, AWS Batch/Fargate Spot,
worker IAM, logs, and isolated worker networking. Deployment automation is
added by a later slice.

## Floci phase

The Floci phase uses:

- `eu-west-1` as the modeled AWS region.
- Local Terraform state.
- Fake local AWS credentials.
- `FLOCI_ENDPOINT_URL` as the AWS-compatible endpoint.
- `FLOCI_START_CMD` as an optional developer-provided startup command.

Run the foundation checks with:

```bash
export FLOCI_ENDPOINT_URL=http://127.0.0.1:4566
export AWS_REGION=eu-west-1
export AWS_ACCESS_KEY_ID=floci
export AWS_SECRET_ACCESS_KEY=floci

make floci-check
make terragrunt-validate
make terragrunt-plan-floci
```

`make floci-up` runs the command in `FLOCI_START_CMD` when developers want the
repository to invoke their local Floci startup command. The repository does not
pin a Floci image or CLI because that runtime is environment-specific.

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

## Real AWS migration

Issue #38 owns the later swap from Floci-only validation to a real AWS account.
That work will add remote state and locking, remove production endpoint
overrides, enable GitHub Actions OIDC apply after approval, and revalidate the
`eu-west-1` cost model.
