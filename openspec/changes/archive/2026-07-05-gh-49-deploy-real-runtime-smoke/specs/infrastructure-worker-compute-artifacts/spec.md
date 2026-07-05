## MODIFIED Requirements

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
