# Design

## Assumptions

- The existing `dev/eu-west-1/worker-compute-artifacts` live stack remains the
  real AWS deployment target.
- The worker ECR repository may already exist from previous infrastructure
  applies; if it does not, the first apply can create it before pushing the
  image tag used by Batch.
- The first smoke should prove the production control-plane Lambda, S3
  multipart upload, DynamoDB, Batch submission, and worker runtime wiring. It
  does not need to prove the browser UI.

## Control-plane package

Terraform will reference a generated Lambda ZIP instead of the stub source.
Repository tooling will build that ZIP from the `src/redact_api` package plus
the small Lambda runtime dependencies. The workflow will build the package
before planning so the reviewed plan and apply both use the same artifact path.

## Batch wiring

The app module and worker module already share `module.foundation.name_prefix`.
To avoid a larger module split, the Lambda environment will use deterministic
Batch names derived from that prefix:

- `${name_prefix}-worker`
- `${name_prefix}-analyze`
- `${name_prefix}-render`

`AwsBatchSubmitter` will select the analyze or render job definition based on
the `WorkerSubmission.mode`. This keeps the control-plane service contract
unchanged while allowing separate Batch job definitions to run different modes.

## Worker runtime

Add a small `redact_api.worker_runtime` module for Batch jobs. It will:

- validate Batch parameters as a `WorkerSubmission`;
- load the current job record from DynamoDB;
- load source bytes from S3 for analyze mode;
- run `analyze_source` with the packaged OCR and PII adapters;
- run `render_redacted_output` for render mode;
- print only safe job status metadata.

The Batch job definitions will pass AWS Batch `Ref::` parameters into this
module. The worker image remains built from `Dockerfile.worker`.

## Network path

For the first smoke, worker subnets will be public subnets with an Internet
Gateway route and `assignPublicIp = ENABLED`. This is simpler than adding NAT
or multiple VPC endpoints, keeps the no-ingress security group, and gives
Fargate tasks outbound access to ECR, Logs, DynamoDB, S3, and Batch APIs.

## Multipart normalization

The API already returns presigned upload-part URLs and accepts ETags on
completion. The service will normalize completion parts by sorting them by
part number, rejecting duplicates, and preserving quoted ETags from S3. This
matches real S3 `CompleteMultipartUpload` expectations and tolerates browsers
reporting completed parts in upload-finish order.

## Smoke path

The smoke script will read live Terragrunt outputs, call the real Lambda
function with an API Gateway-compatible Cognito `sub` context, upload a small
sample through the returned presigned URL, complete the multipart upload, and
check that the job reaches `queued` and a Batch job is submitted. It will keep
the existing read-only infrastructure checks and add an opt-in E2E mode for
runtime mutation.
