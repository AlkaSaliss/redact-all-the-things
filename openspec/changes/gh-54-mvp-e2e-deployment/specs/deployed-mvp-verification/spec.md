## ADDED Requirements

### Requirement: Verify deployed document lifecycle

The AWS runtime smoke SHALL prove a valid supported document can complete the
deployed analysis and export lifecycle through production-shaped interfaces.

#### Scenario: Complete analysis and export

- **WHEN** the opt-in AWS runtime smoke runs after an approved deployment
- **THEN** it uploads a valid supported sample through a control-plane
  presigned multipart URL
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
