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

- **GIVEN** `INFRA_TARGET` is set to `floci` or `dev`
- **WHEN** the developer runs a generic Terragrunt plan or apply target
- **THEN** the command selects the matching live stack and uses that stack's
  deployment mode.

### Requirement: Real AWS remote state

The repository SHALL configure the dev AWS live Terragrunt stack to use remote
Terraform state and locking in the approved AWS account without committing
account-specific identifiers.

#### Scenario: Configure remote state from environment

- **GIVEN** `TG_STATE_BUCKET` and `TG_LOCK_TABLE` are set
- **WHEN** Terragrunt initializes the dev AWS live stack
- **THEN** Terraform state uses the configured S3 bucket and DynamoDB lock
  table.

#### Scenario: Fail when remote state configuration is missing

- **GIVEN** `TG_STATE_BUCKET` or `TG_LOCK_TABLE` is unset
- **WHEN** a developer or CI job initializes the dev AWS live stack
- **THEN** the command fails before planning with setup guidance for the
  missing remote-state configuration.

#### Scenario: Keep real AWS provider free of emulator endpoints

- **WHEN** Terragrunt generates the AWS provider for the dev AWS live stack
- **THEN** the provider omits Floci endpoint overrides, fake credentials, and
  emulator-only validation skips.

#### Scenario: Preserve local Floci state in the shared hierarchy

- **WHEN** Terragrunt initializes the Floci live stack
- **THEN** the stack uses local Terraform state and the generated provider uses
  the configured Floci endpoint with emulator credentials.

### Requirement: Infrastructure deployment workflow

The repository SHALL provide GitHub Actions automation for infrastructure
validation and manually gated AWS deployment.

#### Scenario: Validate infrastructure changes in CI

- **WHEN** a pull request or push changes infrastructure files
- **THEN** GitHub Actions runs the repository Terragrunt validation target
  without requiring AWS credentials.

#### Scenario: Plan AWS infrastructure on branch and pull request updates

- **WHEN** a push targets `main` or a `feat/**` branch, or a pull request
  targets `main`
- **THEN** GitHub Actions runs Terragrunt plan for the dev AWS live stack and
  uploads the plan output as a workflow artifact.

#### Scenario: Plan AWS infrastructure manually

- **GIVEN** the AWS OIDC role secret is configured
- **WHEN** an operator dispatches the infrastructure workflow with `plan`
- **THEN** GitHub Actions assumes the configured AWS role and runs Terragrunt
  plan against the dev AWS live stack.

#### Scenario: Apply AWS infrastructure after approval

- **GIVEN** the AWS OIDC role secret and `aws-production` environment approval
  gate are configured
- **WHEN** an operator dispatches the infrastructure workflow with `apply`
- **THEN** GitHub Actions plans the dev AWS live stack and applies it only
  after the protected environment allows the apply job to run.

### Requirement: Reviewed AWS deployment workflow

The repository SHALL run real AWS infrastructure deployment through GitHub
Actions OIDC, reviewed plan artifacts, and the protected environment gate.

#### Scenario: Produce a reviewed AWS plan artifact

- **GIVEN** the AWS OIDC role and remote-state configuration are available
- **WHEN** the infrastructure workflow runs automatically or an operator
  dispatches it with `plan` or `apply`
- **THEN** GitHub Actions assumes the configured AWS role, runs Terragrunt plan
  for the dev AWS live stack, and uploads the plan output as a workflow
  artifact.

#### Scenario: Apply only after protected approval

- **GIVEN** the operator dispatches the infrastructure workflow with `apply`
- **WHEN** the `aws-production` environment gate approves the apply job
- **THEN** GitHub Actions applies the reviewed dev AWS live stack using OIDC and
  the configured remote state.

### Requirement: Real AWS smoke boundary

The repository SHALL provide an AWS-only smoke entrypoint and documentation for
validating services that the Floci emulator cannot fully cover.

#### Scenario: Run AWS smoke after approved apply

- **GIVEN** the AWS live stack has been applied
- **WHEN** an operator runs the AWS smoke entrypoint
- **THEN** the command checks deployed AWS outputs and AWS-only service
  coverage without relying on Floci endpoint overrides.

#### Scenario: Track deferred budget alerts

- **WHEN** contributors review the real AWS deployment documentation
- **THEN** the documentation identifies cost-model revalidation for this slice
  and links the follow-up issue that owns AWS budget alerts.
