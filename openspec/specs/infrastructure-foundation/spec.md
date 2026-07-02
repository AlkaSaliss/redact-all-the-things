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

#### Scenario: Start Floci through a developer-provided command

- **GIVEN** `FLOCI_START_CMD` is set
- **WHEN** the developer runs the Floci startup target
- **THEN** the command is executed without hard-coding a Floci image or CLI in
  the repository.

#### Scenario: Require an explicit Floci endpoint

- **GIVEN** `FLOCI_ENDPOINT_URL` is not set
- **WHEN** the developer runs a Floci check, plan, apply, or smoke target
- **THEN** the command fails with setup guidance before invoking Terragrunt.

#### Scenario: Validate app-edge smoke boundary

- **GIVEN** `FLOCI_ENDPOINT_URL` is set
- **WHEN** the developer runs the Floci smoke target
- **THEN** the command checks endpoint reachability and reports that unsupported
  app-edge/auth/API services remain covered by static Terraform validation.
