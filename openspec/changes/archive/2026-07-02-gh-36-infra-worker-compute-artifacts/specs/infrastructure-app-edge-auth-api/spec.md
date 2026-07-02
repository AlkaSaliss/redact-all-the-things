## MODIFIED Requirements

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
