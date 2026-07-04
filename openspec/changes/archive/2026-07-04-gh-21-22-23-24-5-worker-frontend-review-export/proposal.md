## Why

Issues #21, #22, #23, #24, and #5 close the gap between worker analysis
outputs and a usable review/export workflow. The normal repository workflow
would split these into separate one-to-two-day changes, but this change is an
explicit governance exception to deliver the final worker integration,
API-backed frontend foundation, Cognito auth shell, upload/dashboard flow,
review editor, autosave, and raster export in one coordinated workstream.

## What Changes

- Verify and close the existing #21 worker manifest integration instead of
  reworking completed checkpoint code.
- Add owner-checked page preview APIs for review thumbnails and canvas images.
- Add a React/Vite/TypeScript frontend that defaults to the real AWS dev API
  and Cognito Hosted UI.
- Add contract fixtures and OpenAPI export tooling for frontend/backend drift
  checks.
- Add review editor behavior for thumbnails, zoom, manual regions, autosave,
  and explicit export acknowledgement.
- Add render-mode worker behavior that burns selected redaction regions into
  raster pixels and writes metadata-stripped PDF/image outputs.
- Add Terraform support for Cognito Hosted UI, frontend/API/S3 CORS, and
  frontend deployment outputs.

## Impact

- Broadens the normal slice size intentionally; the PR must explain the
  exception and list the linked issues.
- Adds npm-based frontend tooling under `frontend/`.
- Adds new public API routes for page summaries and preview authorization.
- Extends infrastructure outputs consumed by frontend local development and
  deployment.
