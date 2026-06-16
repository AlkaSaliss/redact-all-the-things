## 1. Application Setup

- [x] 1.1 Create the issue branch `feat/7-control-plane-api` and move GitHub issue #7 to `In Progress`
- [x] 1.2 Add pinned runtime and test dependencies for FastAPI, Pydantic, the Lambda adapter, AWS SDK access, and pytest to `pyproject.toml` and refresh `uv.lock`
- [x] 1.3 Create the Python package structure for domain contracts, application services, HTTP handlers, and AWS integration
- [x] 1.4 Add a pinned LocalStack Docker Compose service and pytest integration-test marker

## 2. Domain Contracts

- [x] 2.1 Write failing tests for job fields, source types, statuses, timestamp ordering, progress limits, object-key namespaces, and serialization
- [x] 2.2 Implement strict job, status, failure-code, and worker-submission models that satisfy the contract tests
- [x] 2.3 Write failing tests for valid, invalid, failed, retry, and expired lifecycle transitions
- [x] 2.4 Implement the transition table, retry classification, optimistic job versions, and stable submission idempotency tokens
- [x] 2.5 Write failing tests for normalized redaction regions, immutable suggestions, page-manifest validation, and serialization
- [x] 2.6 Implement redaction-region and page-manifest models that satisfy the contract tests

## 3. Application Services

- [x] 3.1 Add LocalStack resource fixtures, concrete DynamoDB/S3 repositories, and the minimal recording Batch fake
- [x] 3.2 Write failing LocalStack-backed service tests for job creation, owner-scoped listing and retrieval, exact expiry, and non-disclosing access denial
- [x] 3.3 Implement job creation, listing, retrieval, ownership enforcement, and exact 24-hour expiry
- [x] 3.4 Write failing LocalStack-backed service tests for upload completion, export confirmation, eligible retry, invalid transitions, and idempotent submissions
- [x] 3.5 Implement upload completion, export confirmation, retry, compare-and-set transitions, and worker orchestration
- [x] 3.6 Write failing LocalStack-backed service tests for manifest reads, valid saves, immutable suggestions, and stale-version conflicts
- [x] 3.7 Implement owner-authorized manifest retrieval and optimistic S3-backed manifest updates
- [x] 3.8 Write failing LocalStack-backed service tests for completed-download authorization and unavailable output rejection
- [x] 3.9 Implement short-lived, object-specific upload and download authorization rules

## 4. HTTP API

- [x] 4.1 Write failing API tests for Cognito-subject extraction, missing identity, validation errors, and non-disclosing not-found responses
- [x] 4.2 Implement the FastAPI application, dependency wiring, stable error mapping, and Lambda entry point
- [x] 4.3 Write failing API tests for create, list, retrieve, upload-complete, manifest read/update, export, download, and retry operations
- [x] 4.4 Implement the authenticated control-plane routes and response contracts
- [x] 4.5 Add an OpenAPI snapshot or schema assertions covering the public request and response contracts

## 5. AWS Persistence Integration

- [x] 5.1 Add LocalStack tests for DynamoDB serialization, owner-index listing, TTL fields, authoritative reads, and conditional version updates
- [x] 5.2 Implement the DynamoDB job repository without persisting filenames, OCR text, PII values, manifests, file contents, or presigned URLs
- [x] 5.3 Add LocalStack tests for namespaced S3 keys, multipart upload authorization, object existence, manifest reads, conditional writes, and downloads
- [x] 5.4 Implement the S3 object and page-manifest repository with short-lived presigning and optimistic write conflicts
- [x] 5.5 Add tests for the minimal Batch fake covering `analyze` and `render` submissions, stable idempotency tokens, and retry modes
- [x] 5.6 Implement the recording Batch fake and run the complete LocalStack-backed integration suite

## 6. Documentation and Verification

- [x] 6.1 Add representative, non-sensitive job, manifest, failure, and worker-request fixtures for issues #6 and #8
- [x] 6.2 Document local API development, authentication assumptions, endpoint contracts, persistence boundaries, and test commands in MkDocs
- [x] 6.3 Add ADR 0002 for the control-plane package boundaries, FastAPI/Lambda choice, and DynamoDB/S3 persistence split
- [x] 6.4 Run the complete pytest suite and resolve failures
- [x] 6.5 Run pre-commit, strict MkDocs, and strict OpenSpec validation
- [x] 6.6 Refresh Graphify with `graphify update .` and review the diff for unrelated or sensitive generated content
- [x] 6.7 Run OpenSpec verification, resolve critical findings, and update all completed task checkboxes
