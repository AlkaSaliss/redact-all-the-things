# infrastructure-worker-compute-artifacts Specification

## Purpose
TBD - created by archiving change gh-36-infra-worker-compute-artifacts. Update Purpose after archive.
## Requirements
### Requirement: Worker image and compute resources

The Floci infrastructure stack SHALL model image storage and AWS Batch/Fargate
Spot compute resources for analysis and render workers.

#### Scenario: Model worker image repository

- **WHEN** the worker compute Terraform module is validated
- **THEN** it defines an ECR repository for the worker image with tag
  immutability and scan-on-push enabled.

#### Scenario: Model one-worker Batch capacity

- **WHEN** the worker compute Terraform module is validated
- **THEN** it defines an AWS Batch Fargate Spot compute environment capped at 2
  vCPU and job definitions that each request 2 vCPU and 8192 MiB.

#### Scenario: Model analyze and render jobs

- **WHEN** the worker compute Terraform module is validated
- **THEN** it defines separate `analyze` and `render` Batch job definitions
  that share the worker image repository and use explicit job modes.

#### Scenario: Model worker logs and IAM

- **WHEN** the worker compute Terraform module is validated
- **THEN** it defines seven-day worker log retention and IAM roles that allow
  only required artifact, job metadata, ECR pull, and log operations.

#### Scenario: Avoid emulator dependency on AWS-managed IAM policies

- **GIVEN** `deployment_mode` is `floci`
- **WHEN** the worker compute Terraform module is applied
- **THEN** the Batch service role uses a module-defined policy instead of
  requiring the emulator to preload AWS-managed service-role policies.

#### Scenario: Use production Batch service policy in AWS mode

- **GIVEN** `deployment_mode` is `aws`
- **WHEN** the worker compute Terraform module is planned
- **THEN** the Batch service role uses the AWS-managed
  `AWSBatchServiceRole` policy attachment.

#### Scenario: Model worker network isolation

- **WHEN** the worker compute Terraform module is validated
- **THEN** it defines worker network resources with no inbound security group
  rules.

### Requirement: Run real worker image commands

The worker compute infrastructure SHALL run the real worker image entrypoint
for analyze and render jobs instead of the infrastructure-only worker stub.

#### Scenario: Analyze job uses real runtime

- **WHEN** the analyze Batch job definition is registered
- **THEN** it uses the configured worker image tag and invokes
  `python -m redact_api.worker_runtime analyze` with Batch-substituted job
  parameters.

#### Scenario: Render job uses real runtime

- **WHEN** the render Batch job definition is registered
- **THEN** it uses the configured worker image tag and invokes
  `python -m redact_api.worker_runtime render` with Batch-substituted job
  parameters.

#### Scenario: Worker tasks have outbound runtime access

- **WHEN** AWS Batch starts a Fargate worker task
- **THEN** the task can reach required AWS service APIs and ECR through an
  outbound-only network path while retaining no inbound security-group access.
