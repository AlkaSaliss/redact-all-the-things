## Context

The technical scope requires Terraform modules composed through Terragrunt, but
the repository currently has no infrastructure tree. The original roadmap
ordered AWS infrastructure after worker, frontend, and review/export completion;
the approved implementation plan intentionally starts the issue #4
infrastructure slices now, using Floci as an AWS-compatible emulator.

This slice must create only the reusable foundation. It should not model the
full AWS graph yet because app edge/auth/API, worker compute, CI/deploy, and
real-AWS migration each have separate child issues.

## Decisions

### Use local Terraform state for the Floci phase

The Floci phase stores state under the local Terragrunt working directory. This
avoids introducing a remote backend that would be replaced by the real-AWS
follow-up and keeps local validation independent of emulator support for S3
backend locking semantics.

### Drive emulator configuration from environment variables

The AWS provider receives its endpoint from `FLOCI_ENDPOINT_URL`. Local runs use
fake AWS credentials and `AWS_REGION=eu-west-1`. The repository does not commit
developer-specific Floci commands or endpoints.

### Add a minimal foundation module before service modules

This slice adds a root module with validation-friendly inputs and outputs, plus
an example foundation resource that can be planned against the Floci endpoint.
Later slices will add S3, DynamoDB, Cognito, API Gateway, Lambda, ECR, Batch,
CloudFront, budgets, OIDC, and IAM resources.

### Keep Floci startup as a command hook

`make floci-up` invokes `FLOCI_START_CMD` when provided. `make floci-check`
verifies `FLOCI_ENDPOINT_URL` is set and performs a lightweight HTTP check. This
keeps the repo independent of an unknown Floci image or CLI.

## Risks

- Floci may not emulate every AWS service used by the final architecture.
  Later slices must distinguish static IaC validation from emulator smoke
  coverage.
- Terragrunt or Terraform may not be installed on a developer machine. Make
  targets should fail with direct command errors rather than silently skipping
  validation.
- The roadmap override could confuse future contributors. Docs must state that
  it is limited to the issue #4 child infrastructure slices.

## Rollout

1. Add foundation IaC files and local validation scripts.
2. Add Make targets for Floci/Terragrunt operations.
3. Document local setup, roadmap override, and real-AWS migration boundary.
4. Validate OpenSpec, docs, and any available Terragrunt checks.
