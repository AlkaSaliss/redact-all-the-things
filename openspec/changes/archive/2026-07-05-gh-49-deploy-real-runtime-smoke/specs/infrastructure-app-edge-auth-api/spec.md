## MODIFIED Requirements

### Requirement: Deploy real control-plane Lambda package
The app edge/auth/API infrastructure SHALL deploy the checked-in
`redact_api.lambda_handler` application package instead of an
infrastructure-only Lambda stub.

#### Scenario: Package real Lambda runtime
- **WHEN** the AWS live stack is planned or applied
- **THEN** the Lambda function references a generated control-plane ZIP built
  from the real Python package and Lambda runtime dependencies
- **AND** the Lambda handler is `redact_api.lambda_handler.handler`.

#### Scenario: Wire Lambda to real Batch jobs
- **WHEN** the Lambda runtime starts in the AWS live stack
- **THEN** its environment includes the artifact bucket, jobs table, worker job
  queue, analyze job definition, render job definition, and allowed frontend
  origins
- **AND** its execution role can submit jobs to AWS Batch.
