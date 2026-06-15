## ADDED Requirements

### Requirement: Authenticated control-plane boundary
Every control-plane operation SHALL require an authenticated Cognito subject
and SHALL use that subject as the owner identifier rather than accepting an
owner identifier from request data.

#### Scenario: Authenticated request
- **WHEN** API Gateway supplies a valid Cognito subject
- **THEN** the operation executes in that owner's scope

#### Scenario: Missing identity
- **WHEN** a request has no valid authenticated subject
- **THEN** the API rejects the request without reading or mutating job storage

### Requirement: Create job and authorize upload
The API SHALL create one job for one supported source file and return
short-lived authorization to upload only that job's source object.

#### Scenario: Create a supported job
- **WHEN** an authenticated user requests a job for PDF, JPEG, or PNG input
- **THEN** the API returns the `uploading` job contract and object-specific multipart upload authorization under the owner's job namespace

#### Scenario: Reject unsupported creation data
- **WHEN** a request specifies an unsupported source type, invalid size, or size above 100 MB
- **THEN** the API rejects job creation without issuing upload authorization

### Requirement: List and retrieve jobs
The API SHALL allow an owner to list and retrieve only that owner's unexpired
jobs and SHALL return the fields required by the dashboard and job workflow.

#### Scenario: List recent jobs
- **WHEN** an authenticated user lists jobs
- **THEN** the API returns only that user's unexpired jobs ordered from newest to oldest

#### Scenario: Retrieve an inaccessible job
- **WHEN** a user requests a missing, foreign-owned, or expired job
- **THEN** the API returns a non-disclosing not-found response

### Requirement: Complete upload and submit analysis
The API SHALL confirm that the expected source object exists before atomically
accepting an uploaded job for analysis and submitting the worker request.

#### Scenario: Complete a valid upload
- **WHEN** the owner completes upload for an `uploading` job whose expected object exists
- **THEN** the API transitions the job to `queued` and submits an idempotent `analyze` request

#### Scenario: Complete a missing upload
- **WHEN** the expected source object does not exist
- **THEN** the API rejects completion and leaves the job in `uploading`

#### Scenario: Repeat upload completion
- **WHEN** the owner repeats completion after the analysis submission was accepted
- **THEN** the API does not create a second logical analysis submission

### Requirement: Read and update page manifests
The API SHALL allow the owner of a `ready` or `failed` unexpired job to read
page manifests and SHALL accept valid user-region updates using optimistic
manifest versions.

#### Scenario: Read a page manifest
- **WHEN** the owner requests an existing page manifest for an accessible job
- **THEN** the API returns its immutable suggestions, current regions, version, and last-save timestamp

#### Scenario: Save user changes
- **WHEN** the owner submits valid current regions with the current manifest version
- **THEN** the API persists and returns the next manifest version

#### Scenario: Resolve concurrent edits
- **WHEN** the owner submits a stale manifest version
- **THEN** the API returns a conflict response containing no overwritten data

### Requirement: Confirm export and submit rendering
The API SHALL require explicit acknowledgement that automated detection may
miss PII before accepting export for a `ready` job.

#### Scenario: Confirm export
- **WHEN** the owner acknowledges the warning and requests export for a `ready` job
- **THEN** the API transitions the job to `exporting` and submits an idempotent `render` request

#### Scenario: Omit export acknowledgement
- **WHEN** the owner requests export without the required acknowledgement
- **THEN** the API rejects the request and leaves the job `ready`

### Requirement: Authorize completed download
The API SHALL issue a short-lived, object-specific download URL only for the
owner of an unexpired `complete` job with an existing output object.

#### Scenario: Download completed output
- **WHEN** the owner requests download for an accessible `complete` job
- **THEN** the API returns authorization scoped only to that job's output object

#### Scenario: Download unavailable output
- **WHEN** the job is not `complete` or its output object is absent
- **THEN** the API rejects the request without issuing a URL

### Requirement: Retry eligible processing
The API SHALL permit the owner to retry only failed jobs whose safe failure
code identifies a transient infrastructure or Spot interruption.

#### Scenario: Retry a transient failure
- **WHEN** the owner retries an eligible failed job
- **THEN** the API applies the defined lifecycle transition and submits one idempotent worker request in the recorded failure mode

#### Scenario: Retry an ineligible failure
- **WHEN** the owner retries a job with a permanent failure or a non-failed status
- **THEN** the API rejects the request without submitting work

### Requirement: Presigned URL security
Upload and download authorization SHALL be short-lived, object-specific,
owner-scoped, and excluded from application logs and persisted job records.

#### Scenario: Generate object authorization
- **WHEN** the API creates a presigned upload part or download URL
- **THEN** its operation, bucket, key, and expiry are limited to the requested owner and job object

#### Scenario: Record an API request
- **WHEN** request and response metadata is logged
- **THEN** filenames, file content, manifest content, detected PII, and presigned URLs are absent

### Requirement: Locally testable service boundaries
The control-plane SHALL configure DynamoDB and S3 clients for a pinned
LocalStack environment and SHALL use a minimal recording Batch fake locally so
integrated behavior can be tested without an AWS account or paid emulator
features.

#### Scenario: Validate AWS integration locally
- **WHEN** the opt-in integration suite runs against the pinned LocalStack services
- **THEN** DynamoDB and S3 behavior is validated against LocalStack and Batch submission contracts are validated with the recording fake
