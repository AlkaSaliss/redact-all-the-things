## ADDED Requirements

### Requirement: Permanent worker validation failures
The shared job contract SHALL classify worker input-validation and unsupported
content failures as permanent failures that are safe to persist and not
eligible for automatic retry.

#### Scenario: Persist validation failure safely
- **WHEN** worker input validation rejects a source object for size, page-count, image pixel-count, encryption, or malformed supported content
- **THEN** the job may transition to `failed` with safe failure code `validation_failed`

#### Scenario: Persist unsupported content safely
- **WHEN** worker input validation rejects a source object because its signature or decoded content does not match the supported job source type
- **THEN** the job may transition to `failed` with safe failure code `unsupported_content`

#### Scenario: Reject retry for permanent validation failures
- **WHEN** a failed job has safe failure code `validation_failed` or `unsupported_content`
- **THEN** automatic retry is not permitted
