# infrastructure-foundation Specification

## Purpose
TBD - created by archiving change gh-34-infra-floci-foundation. Update Purpose after archive.
## Requirements
### Requirement: Floci infrastructure foundation

The repository SHALL provide a Terragrunt/Terraform foundation for the AWS
infrastructure milestone that targets Floci through an AWS-compatible endpoint.

#### Scenario: Configure the Floci endpoint from the environment

- **GIVEN** a developer has set `FLOCI_ENDPOINT_URL`
- **WHEN** Terragrunt initializes or plans the Floci environment
- **THEN** the AWS provider is configured to use that endpoint with fake local
  AWS credentials and `eu-west-1` as the default region.

#### Scenario: Keep emulator state local

- **WHEN** the Floci environment is initialized
- **THEN** Terraform state is local to the developer workspace rather than an
  S3/DynamoDB remote backend.

#### Scenario: Validate the foundation without real AWS

- **WHEN** a developer runs the repository infrastructure validation target
- **THEN** Terraform and Terragrunt configuration are validated without
  requiring a real AWS account.

### Requirement: Floci developer commands

The repository SHALL provide Make targets for starting/checking Floci and for
running Terragrunt validation, plan, apply, and smoke entrypoints.

#### Scenario: Start Floci through the repository command

- **WHEN** the developer runs the Floci startup target
- **THEN** the local Floci AWS emulator is started with repository-local
  persistent state.

#### Scenario: Require an explicit Floci endpoint

- **GIVEN** `FLOCI_ENDPOINT_URL` is not set
- **WHEN** the developer runs a Floci check, plan, apply, or smoke target
- **THEN** the command fails with setup guidance before invoking Terragrunt.

#### Scenario: Validate app-edge smoke boundary

- **GIVEN** `FLOCI_ENDPOINT_URL` is set
- **WHEN** the developer runs the Floci smoke target
- **THEN** the command checks endpoint reachability and reports that unsupported
  app-edge/auth/API services remain covered by static Terraform validation.

#### Scenario: Validate worker-compute smoke boundary

- **GIVEN** `FLOCI_ENDPOINT_URL` is set
- **WHEN** the developer runs the Floci smoke target
- **THEN** the command reports that Batch, Fargate, ECR, and worker networking
  support depends on the configured emulator and remains covered by static
  Terraform validation when unsupported.

#### Scenario: Select infrastructure deployment target

- **GIVEN** `INFRA_TARGET` is set to `floci` or `aws`
- **WHEN** the developer runs a generic Terragrunt plan or apply target
- **THEN** the command selects the matching live stack and uses that stack's
  deployment mode.

### Requirement: Infrastructure deployment workflow

The repository SHALL provide GitHub Actions automation for infrastructure
validation and manually gated AWS deployment.

#### Scenario: Validate infrastructure changes in CI

- **WHEN** a pull request or push changes infrastructure files
- **THEN** GitHub Actions runs the repository Terragrunt validation target
  without requiring AWS credentials.

#### Scenario: Plan AWS infrastructure manually

- **GIVEN** the AWS OIDC role secret is configured
- **WHEN** an operator dispatches the infrastructure workflow with `plan`
- **THEN** GitHub Actions assumes the configured AWS role and runs Terragrunt
  plan against the AWS live stack.

#### Scenario: Apply AWS infrastructure after approval

- **GIVEN** the AWS OIDC role secret and `aws-production` environment approval
  gate are configured
- **WHEN** an operator dispatches the infrastructure workflow with `apply`
- **THEN** GitHub Actions plans the AWS live stack and applies it only after
  the protected environment allows the apply job to run.
