## ADDED Requirements

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

#### Scenario: Model worker network isolation

- **WHEN** the worker compute Terraform module is validated
- **THEN** it defines worker network resources with no inbound security group
  rules.

### Requirement: Temporary worker stub

The Floci worker compute slice SHALL include a minimal worker stub only for
infrastructure wiring until the worker image pipeline provides the real image.

#### Scenario: Keep worker stub separate

- **WHEN** contributors inspect infrastructure stubs
- **THEN** the worker stub is located under infrastructure paths and does not
  replace runtime worker implementation code.
