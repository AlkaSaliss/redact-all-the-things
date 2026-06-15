# Job Contracts Specification

## Purpose

Define the persistent job, lifecycle, page-manifest, privacy, and asynchronous
worker-submission contracts shared by the control plane and workers.

## Requirements

### Requirement: Persistent job record
The system SHALL represent each job with an identifier, owner identifier,
source type, namespaced source and output object keys, status, page count,
completed-page count, creation and expiry timestamps, model versions, safe
failure code, and optimistic-lock version.

#### Scenario: Store a new job
- **WHEN** an authenticated user creates a job
- **THEN** the system persists a complete job record with status `uploading`, version `1`, and an expiry exactly 24 hours after creation

#### Scenario: Reject an invalid job record
- **WHEN** a job record has an unsupported source type, status, timestamp ordering, page count, progress count, or object-key namespace
- **THEN** contract validation rejects the record before persistence

### Requirement: Job status lifecycle
The system SHALL support the statuses `uploading`, `queued`, `analyzing`,
`ready`, `exporting`, `complete`, `failed`, and `expired`, and SHALL reject
transitions outside the defined lifecycle.

#### Scenario: Complete the normal lifecycle
- **WHEN** a job progresses through upload, analysis, review readiness, export, and completion
- **THEN** its transitions are `uploading` to `queued` to `analyzing` to `ready` to `exporting` to `complete`

#### Scenario: Reject an invalid transition
- **WHEN** a caller attempts to move an `uploading` job directly to `ready`
- **THEN** the system rejects the transition without changing the persisted job

#### Scenario: Record processing failure
- **WHEN** analysis or rendering reports a classified failure
- **THEN** the system moves the job to `failed` and stores only a safe failure code

### Requirement: Optimistic job updates
Persistent job updates SHALL compare the expected job version and increment
the version exactly once when the update succeeds.

#### Scenario: Update the current version
- **WHEN** a caller updates a job using its current version
- **THEN** the system persists the change with the version incremented by one

#### Scenario: Detect a stale job update
- **WHEN** a caller updates a job using a version older than the persisted version
- **THEN** the system reports a version conflict and preserves the newer record

### Requirement: Ownership and access expiry
Every job operation SHALL authorize against the authenticated owner and SHALL
deny access at or after the job expiry timestamp independently of physical
storage cleanup.

#### Scenario: Owner accesses an active job
- **WHEN** the authenticated owner requests a job before its expiry timestamp
- **THEN** the operation may proceed

#### Scenario: Another user accesses a job
- **WHEN** an authenticated user requests a job owned by another user
- **THEN** the system denies access without exposing the job data

#### Scenario: Owner accesses an expired job
- **WHEN** the authenticated owner requests a job at or after its expiry timestamp
- **THEN** the system denies access and treats the job as expired even if its storage has not been deleted

### Requirement: Page manifest contract
The system SHALL represent each page manifest with a job identifier, page
number, immutable model suggestions, current user-selected regions, integer
manifest version, and last-save timestamp.

#### Scenario: Validate a redaction region
- **WHEN** a page manifest contains a redaction region
- **THEN** the region has an identifier, page number, normalized `x`, `y`, `width`, and `height`, source `automatic` or `manual`, category, optional confidence, and selected state

#### Scenario: Preserve immutable suggestions
- **WHEN** a user saves changes to the current selected regions
- **THEN** the immutable model suggestions remain unchanged

#### Scenario: Reject out-of-bounds geometry
- **WHEN** a region has non-finite coordinates, non-positive dimensions, or extends beyond normalized page bounds
- **THEN** contract validation rejects the manifest

### Requirement: Optimistic page-manifest persistence
Page manifest writes SHALL require the expected manifest version and SHALL
atomically replace the S3 manifest only when that version is current.

#### Scenario: Save the current manifest
- **WHEN** the owner saves a valid page manifest using its current version
- **THEN** the system stores the updated manifest with its version incremented by one and a new last-save timestamp

#### Scenario: Save a stale manifest
- **WHEN** the owner saves a page manifest using a stale version
- **THEN** the system reports a version conflict and preserves the current manifest

### Requirement: Privacy-preserving persistence
DynamoDB SHALL store job metadata, ownership, lifecycle, progress, model
versions, and safe failure information, while S3 SHALL store source files,
previews, analysis artifacts, page manifests, and exported files.

#### Scenario: Persist sensitive analysis output
- **WHEN** OCR text, detected PII values, or page-manifest content is persisted
- **THEN** the content is stored only in the job's namespaced S3 objects and not in DynamoDB

#### Scenario: Serialize a safe job record
- **WHEN** a job record is written to DynamoDB or emitted to logs
- **THEN** it excludes filenames, OCR text, detected PII, manifest content, file content, and presigned URLs

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
- **THEN** the system permits an idempotent retry in the mode identified by that failure code

#### Scenario: Reject a permanent failure retry
- **WHEN** a job has a permanent validation, content, or processing failure code
- **THEN** the system rejects automatic retry
