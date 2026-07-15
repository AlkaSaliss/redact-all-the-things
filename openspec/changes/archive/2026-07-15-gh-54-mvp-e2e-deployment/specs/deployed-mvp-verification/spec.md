## ADDED Requirements

### Requirement: The deployed worker includes its runtime validation policy

The worker container SHALL include the configured validation limits at the
path selected by `WORKER_VALIDATION_CONFIG`.

#### Scenario: AWS Batch starts analysis

- **WHEN** an analysis job starts in the deployed worker container
- **THEN** the worker can load its validation policy before processing the source

### Requirement: Verify deployed document lifecycle

The AWS runtime smoke SHALL prove a valid supported document can complete the
deployed analysis and export lifecycle through production-shaped interfaces.

#### Scenario: Complete analysis and export

- **WHEN** the opt-in AWS runtime smoke runs after an approved deployment
- **THEN** it uploads a valid supported sample through a control-plane
  Signature V4 presigned multipart URL
- **AND** it waits for the job to become ready
- **AND** it confirms export and waits for the job to complete
- **AND** it downloads a non-empty redacted result through the authorized URL.

#### Scenario: Report terminal worker failure

- **WHEN** analysis or render reaches a failed state or exceeds its deadline
- **THEN** the smoke fails with the safe job status and failure code
- **AND** it does not print source content, OCR content, or signed URLs.

#### Scenario: Report presigned transfer failure

- **WHEN** a presigned upload or download returns an HTTP error
- **THEN** the smoke reports the operation, HTTP status, and sanitized response
  body
- **AND** it does not print the signed URL.

### Requirement: Verify deployed browser entry

The deployed MVP verification SHALL exercise the public application entry and
authentication redirect in a real browser.

#### Scenario: Open application and start sign-in

- **WHEN** a browser opens the deployed CloudFront application
- **THEN** the React application renders its signed-out state
- **AND** starting sign-in navigates to the configured Cognito hosted UI.

### Requirement: CloudFront can serve the private frontend

The frontend bucket SHALL allow object reads from only the configured
CloudFront distribution, and CloudFront SHALL route missing SPA paths to the
application entry document.

#### Scenario: Open an application route

- **WHEN** a browser requests the root, OAuth callback, or client-side route
- **THEN** CloudFront serves the React application from the private S3 bucket
- **AND** a later infrastructure apply does not replace the published entry document with the bootstrap placeholder
