## Why

The worker and frontend milestones need one tested source of truth for job
lifecycle, ownership, expiry, manifests, persistence, and asynchronous worker
submission. Establishing these contracts first prevents later components from
inventing incompatible API and storage behavior.

## What Changes

- Add persistent job, status, redaction-region, and page-manifest contracts.
- Add authenticated control-plane operations for creating, listing, retrieving,
  and advancing jobs.
- Add short-lived, object-specific S3 upload and download authorization.
- Add optimistic page-manifest updates and explicit version-conflict behavior.
- Add ownership and exact 24-hour access-expiry enforcement to every job
  operation.
- Add LocalStack-backed DynamoDB and S3 integration plus a minimal recording
  Batch fake so lifecycle, retry, and worker-submission behavior can be tested
  locally.
- Exclude OCR processing, review-editor UI, export rendering, and production
  AWS deployment.

## Capabilities

### New Capabilities

- `job-contracts`: Persistent job, status, redaction-region, page-manifest,
  ownership, expiry, versioning, and safe-failure requirements.
- `control-plane-api`: Authenticated job lifecycle, presigned object access,
  manifest persistence, export confirmation, download authorization, and
  worker-submission requirements.

### Modified Capabilities

None.

## Impact

- Introduces the Python application package and its HTTP/API boundary.
- Adds DynamoDB and S3 integration configured for LocalStack validation during
  local development and CI, with a minimal recording fake for Batch submission.
- Adds API and contract tests consumed by the later worker and frontend
  milestones.
- Adds Python runtime dependencies and project documentation for the new
  control-plane behavior.
