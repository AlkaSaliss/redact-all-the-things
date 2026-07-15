## MODIFIED Requirements

### Requirement: Deploy real control-plane Lambda package

The app edge/auth/API infrastructure SHALL deploy the checked-in
`redact_api.lambda_handler` application package instead of an
infrastructure-only Lambda stub.

#### Scenario: Package real Lambda runtime

- **WHEN** the AWS live stack is planned or applied
- **THEN** Terraform stages a generated control-plane ZIP built from the real
  Python package and Lambda runtime dependencies in private S3 storage
- **AND** the Lambda function references that staged package artifact
- **AND** the Lambda handler is `redact_api.lambda_handler.handler`.

#### Scenario: Wire Lambda to real Batch jobs

- **WHEN** the Lambda runtime starts in the AWS live stack
- **THEN** its environment includes the artifact bucket, jobs table, worker job
  queue, analyze job definition, render job definition, and allowed frontend
  origins
- **AND** its execution role can submit jobs to AWS Batch.

#### Scenario: Avoid Lambda package path-only drift

- **GIVEN** the generated Lambda ZIP content hash has not changed
- **WHEN** Terraform plans from a different local or CI filesystem path
- **THEN** the plan does not update the Lambda function only because the ZIP
  filename path differs.

#### Scenario: Keep unchanged package builds stable

- **GIVEN** the Lambda source files and runtime dependency versions have not
  changed
- **WHEN** the Lambda package is rebuilt
- **THEN** the generated ZIP content hash remains stable.
