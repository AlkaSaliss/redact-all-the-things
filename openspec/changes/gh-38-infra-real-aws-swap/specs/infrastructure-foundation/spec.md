## ADDED Requirements

### Requirement: Real AWS remote state

The repository SHALL configure the AWS live Terragrunt stack to use remote
Terraform state and locking in the approved AWS account without committing
account-specific identifiers.

#### Scenario: Configure remote state from environment

- **GIVEN** `TG_STATE_BUCKET` and `TG_LOCK_TABLE` are set
- **WHEN** Terragrunt initializes the AWS live stack
- **THEN** Terraform state uses the configured S3 bucket and DynamoDB lock
  table.

#### Scenario: Fail when remote state configuration is missing

- **GIVEN** `TG_STATE_BUCKET` or `TG_LOCK_TABLE` is unset
- **WHEN** a developer or CI job initializes the AWS live stack
- **THEN** the command fails before planning with setup guidance for the
  missing remote-state configuration.

#### Scenario: Keep production provider free of emulator endpoints

- **WHEN** Terragrunt generates the AWS provider for the AWS live stack
- **THEN** the provider omits Floci endpoint overrides, fake credentials, and
  emulator-only validation skips.

### Requirement: Reviewed AWS deployment workflow

The repository SHALL run real AWS infrastructure deployment through GitHub
Actions OIDC, reviewed plan artifacts, and the protected production
environment gate.

#### Scenario: Produce a reviewed production plan artifact

- **GIVEN** the AWS OIDC role and remote-state configuration are available
- **WHEN** an operator dispatches the infrastructure workflow with `plan` or
  `apply`
- **THEN** GitHub Actions assumes the configured AWS role, runs Terragrunt plan
  for the AWS live stack, and uploads the plan output as a workflow artifact.

#### Scenario: Apply only after production approval

- **GIVEN** the operator dispatches the infrastructure workflow with `apply`
- **WHEN** the `aws-production` environment gate approves the apply job
- **THEN** GitHub Actions applies the reviewed AWS live stack using OIDC and
  the configured remote state.

### Requirement: Real AWS smoke boundary

The repository SHALL provide an AWS-only smoke entrypoint and documentation for
validating services that the Floci emulator cannot fully cover.

#### Scenario: Run AWS smoke after approved apply

- **GIVEN** the AWS live stack has been applied
- **WHEN** an operator runs the AWS smoke entrypoint
- **THEN** the command checks deployed AWS outputs and production-only service
  coverage without relying on Floci endpoint overrides.

#### Scenario: Track deferred budget alerts

- **WHEN** contributors review the real AWS deployment documentation
- **THEN** the documentation identifies cost-model revalidation for this slice
  and links the follow-up issue that owns AWS budget alerts.
