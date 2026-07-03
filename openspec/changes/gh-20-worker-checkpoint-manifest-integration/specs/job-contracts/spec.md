## MODIFIED Requirements

### Requirement: Worker submission contract
The system SHALL submit asynchronous worker requests containing a job
identifier, owner-scoped object keys, and mode `analyze` or `render`, and SHALL
use a stable idempotency token for each accepted lifecycle transition.

#### Scenario: Submit analysis
- **WHEN** an uploaded job is accepted for processing
- **THEN** the system submits one `analyze` request associated with the transition to `queued`

#### Scenario: Submit rendering
- **WHEN** a ready job is accepted for export
- **THEN** the system submits one `render` request associated with the transition to `exporting`

#### Scenario: Retry an eligible failure
- **WHEN** a job has a failure code classified as transient infrastructure or Spot interruption
- **THEN** the system permits an idempotent retry in the mode identified by that failure code while preserving existing page count, completed page count, and model version checkpoint fields

#### Scenario: Reject a permanent failure retry
- **WHEN** a job has a permanent validation, content, or processing failure code
- **THEN** the system rejects automatic retry
