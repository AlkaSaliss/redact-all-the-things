## Context

Issue #7 is the first application milestone and establishes contracts consumed
by the later analysis worker and React frontend. The repository currently has
no application package or runtime dependencies. The approved architecture uses
API Gateway HTTP API, Cognito JWT authorization, Python Lambda, DynamoDB for job
metadata, S3 for document artifacts and manifests, and AWS Batch for
asynchronous `analyze` and `render` work.

The API must enforce ownership and exact 24-hour access expiry independently of
DynamoDB TTL and S3 lifecycle cleanup. It must also keep OCR text, detected PII,
and page-manifest content out of DynamoDB and logs. Local development through
this milestone uses mocked AWS boundaries rather than deployed infrastructure.

## Goals / Non-Goals

**Goals:**

- Define validated Python contracts for jobs, statuses, redaction regions,
  page manifests, failures, and worker submissions.
- Implement authenticated job lifecycle and object-authorization operations.
- Enforce ownership, expiry, state transitions, and optimistic concurrency in
  one application service layer.
- Provide DynamoDB, S3, and Batch integration validated against LocalStack.
- Produce stable fixtures and contracts for issues #6 and #8.

**Non-Goals:**

- Implement Cognito provisioning, API Gateway, Lambda, DynamoDB tables, S3
  buckets, Batch queues, or other production infrastructure.
- Validate uploaded file contents, rasterize documents, run OCR or PII models,
  or render exports.
- Build the review editor or frontend client.
- Implement eventual lifecycle deletion; this change only enforces access
  expiry and records cleanup timestamps.

## Decisions

### Separate domain contracts, application services, and AWS integration

The Python package will keep validated domain models and lifecycle rules free
of HTTP and AWS SDK concerns. Application services will orchestrate ownership,
expiry, persistence, presigning, and worker submission through concrete AWS
repositories configured with injected boto3 clients. HTTP handlers translate
at the outer boundary.

This keeps domain tests fast, lets service and API tests use LocalStack, and
allows later worker code to import the same contracts. A separate hierarchy of
port protocols plus in-memory and mocked adapters was rejected as unnecessary
for this single AWS deployment target.

### Validate persistence with LocalStack and use a minimal Batch fake

Service, API, and persistence tests will run against a Docker Compose service
pinned to `localstack/localstack:4.14.0`. Boto3 DynamoDB and S3 clients receive
the LocalStack endpoint and test credentials through application settings.
Pure domain contract tests remain independent of external services.

LocalStack Community does not provide Batch in this pinned release. Local
worker-submission tests will therefore use one minimal fake that records
`WorkerSubmission` contracts and de-duplicates them by idempotency token. It
will not emulate queues, scheduling, or worker execution.

Mocked SDK clients and custom DynamoDB/S3 in-memory adapters were rejected
because LocalStack exercises endpoint-level serialization and conditional
behavior with less test-only implementation.

### Use FastAPI with Pydantic models and a Lambda adapter

FastAPI will define the HTTP boundary, request validation, error mapping, and
OpenAPI contract. Pydantic models will provide strict serialization shared by
the API, persistence adapters, fixtures, and worker submissions. A thin Lambda
adapter will expose the application to API Gateway without coupling domain
logic to Lambda event shapes.

A hand-written router was considered but rejected because it would duplicate
validation and contract generation while providing no useful scope reduction.

### Trust only the API Gateway Cognito subject for ownership

The HTTP boundary will extract the Cognito subject from the validated API
Gateway authorizer context and pass it as the owner identifier. Request bodies
and query parameters will never select an owner. Missing identity fails before
storage access.

Foreign-owned, missing, and expired jobs will use the same not-found response
to avoid revealing job existence.

### Store job metadata in DynamoDB and manifests in S3

Each DynamoDB job item will contain the approved job fields, an integer
optimistic-lock version, and a numeric TTL derived from `expires_at`. An owner
index will support newest-first dashboard listing. Object keys are generated
by the service under an owner-ID and job-ID namespace rather than accepted from
clients.

Full page manifests remain JSON objects in S3 because they contain detected PII
categories and user review state. Conditional object writes using the current
object version implement optimistic saves. DynamoDB will not duplicate
manifest content, OCR text, or detected values.

Storing manifests in DynamoDB was rejected because it conflicts with the
technical scope's privacy boundary and risks item-size growth.

### Enforce lifecycle transitions with compare-and-set updates

The domain defines an explicit transition table:

- `uploading` to `queued`
- `queued` to `analyzing`
- `analyzing` to `ready` or `failed`
- `ready` to `exporting`
- `exporting` to `complete` or `failed`
- an eligible `failed` job to `queued` or `exporting`, based on its safe
  failure code
- any accessible status to the effective terminal state `expired` once the
  access deadline is reached

DynamoDB updates compare the expected version and current status. API
operations use idempotency tokens derived from the job, target transition, and
resulting version so repeated accepted requests do not create a second logical
Batch submission.

### Treat expiry as an authorization rule, not a cleanup result

The application compares an injected UTC clock with `expires_at` for every
operation. Access is denied at equality or later. DynamoDB TTL and S3 lifecycle
rules remain eventual cleanup mechanisms owned by the infrastructure
milestone.

### Keep the initial HTTP surface task-oriented

The initial API will expose operations for job creation, listing, retrieval,
upload completion, manifest retrieval and update, export confirmation,
download authorization, and retry. Responses use domain models and stable
error categories for validation, not found, conflict, and invalid transition.

Worker progress updates use the shared repository and domain contracts rather
than a public user endpoint in this milestone.

## Risks / Trade-offs

- **Batch submission can fail after a status update** -> Persist the transition
  and stable idempotency token, report a safe failure, and allow reconciliation
  or an eligible retry without generating duplicate logical work.
- **S3 conditional-write support can differ between LocalStack and AWS** -> Run
  LocalStack integration tests now and defer deployed AWS smoke tests to the
  infrastructure milestone.
- **LocalStack behavior can differ from AWS** -> Use it for local integration
  confidence while keeping mocked request assertions and deferring deployed
  AWS smoke tests to the infrastructure milestone.
- **The Batch fake cannot validate AWS request compatibility** -> Keep it
  limited to the shared submission contract and validate the real Batch client
  during the infrastructure milestone.
- **FastAPI and the Lambda adapter increase package size** -> Keep dependencies
  minimal and defer deployment-size optimization to the infrastructure
  milestone.
- **Failure codes encode retry mode and retryability** -> Define a closed,
  documented code set and reject unknown codes at contract boundaries.
- **DynamoDB TTL is not exact** -> Enforce expiry in application services and
  test boundary timestamps directly.
- **Job listing through an owner index can be eventually consistent** -> Accept
  eventual dashboard listing while direct job operations use authoritative
  reads and conditional writes.

## Migration Plan

1. Add the application package, dependencies, LocalStack service, and strict
   domain models.
2. Add DynamoDB and S3 integration, provision test resources in LocalStack,
   and add the minimal recording Batch fake.
3. Add application services and FastAPI operations with LocalStack-backed
   tests and an injected authenticated identity.
5. Add documentation and representative fixtures for worker and frontend
   consumers.
6. Run tests, linting, strict documentation, strict OpenSpec validation, and
   Graphify refresh.

Rollback consists of reverting the application package and dependency changes;
no production data or infrastructure migration occurs in this milestone.

## Open Questions

None.
