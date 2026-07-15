# infrastructure-app-edge-auth-api Specification

## Purpose
TBD - created by archiving change gh-35-infra-app-edge-auth-api. Update Purpose after archive.
## Requirements
### Requirement: App-facing infrastructure resources

The Floci infrastructure stack SHALL model the app edge, authentication,
control-plane, and persistence resources required by the technical scope.

#### Scenario: Model frontend and artifact storage

- **WHEN** the Floci Terraform module is validated
- **THEN** it defines a private frontend S3 bucket, a private artifact S3
  bucket, encryption, public access blocks, and 24-hour artifact lifecycle
  expiration.

#### Scenario: Model control-plane persistence

- **WHEN** the Floci Terraform module is validated
- **THEN** it defines a DynamoDB jobs table with owner lookup support and TTL
  enabled for eventual cleanup.

#### Scenario: Model authenticated HTTP API

- **WHEN** the Floci Terraform module is validated
- **THEN** it defines a Cognito user pool, Cognito user pool app client, API
  Gateway HTTP API, Cognito JWT authorizer, Lambda integration, Lambda invoke
  permission, and default route.

#### Scenario: Model edge delivery

- **WHEN** the Floci Terraform module is validated
- **THEN** it defines a CloudFront distribution using origin access control for
  the frontend S3 origin.

#### Scenario: Keep local apply compatible with Floci edge coverage

- **GIVEN** `deployment_mode` is `floci`
- **WHEN** the configured emulator does not provide CloudFront-compatible apply
  responses
- **THEN** the live stack can disable CloudFront creation while retaining the
  CloudFront resources in the reusable module for static validation and later
  real AWS deployment.

#### Scenario: Activate edge delivery in AWS mode

- **GIVEN** `deployment_mode` is `aws`
- **WHEN** the AWS live stack is planned
- **THEN** CloudFront distribution creation is enabled for the production-shaped
  resource graph.

#### Scenario: Model least-privilege Lambda access

- **WHEN** the Floci Terraform module is validated
- **THEN** the Lambda execution role grants only the app resources needed for
  job metadata, file artifacts, logging, and later worker submission wiring.

#### Scenario: Expose worker policy inputs

- **WHEN** worker compute infrastructure composes the app module
- **THEN** the app module exposes artifact bucket and jobs table identifiers
  and ARNs needed by worker IAM policies.

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

### Requirement: Temporary frontend placeholder

The app edge/auth/API slice SHALL include a minimal frontend placeholder only
for infrastructure wiring until product slices provide the real frontend
artifact.

#### Scenario: Publish a frontend placeholder

- **WHEN** Terraform plans the Floci stack
- **THEN** a minimal static frontend placeholder object is available for the
  frontend bucket without implementing product UI behavior.
