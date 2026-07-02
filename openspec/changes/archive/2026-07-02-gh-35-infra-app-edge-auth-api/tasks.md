## 1. OpenSpec

- [x] 1.1 Add proposal, design, specs, and tasks for the app edge/auth/API
  infrastructure slice.

## 2. Terraform and Terragrunt

- [x] 2.1 Add an app edge/auth/API Terraform module that composes the foundation
  module.
- [x] 2.2 Model frontend S3 hosting, artifact S3 storage, DynamoDB jobs table,
  Cognito, API Gateway HTTP API, Lambda, CloudWatch logs, CloudFront origin
  access control, and IAM.
- [x] 2.3 Add minimal frontend and Lambda stubs for infrastructure wiring only.
- [x] 2.4 Point the Floci Terragrunt live config at the new module.

## 3. Commands and Documentation

- [x] 3.1 Extend infrastructure validation targets to cover all modules.
- [x] 3.2 Update smoke checks and docs with app edge/auth/API emulator coverage
  boundaries.

## 4. Verification

- [x] 4.1 Run `uv run pre-commit run --all-files`.
- [x] 4.2 Run `openspec validate --all --strict --no-interactive`.
- [x] 4.3 Run `uv run mkdocs build --strict`.
- [x] 4.4 Run `make terragrunt-validate`.
- [x] 4.5 Run `uv run pytest`.
- [x] 4.6 Refresh Graphify after infrastructure and architecture changes.
