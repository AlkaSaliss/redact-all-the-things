## MODIFIED Requirements

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
