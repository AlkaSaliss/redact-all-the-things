## MODIFIED Requirements

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
