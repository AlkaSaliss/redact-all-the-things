## Why

The AWS stack has real API and worker resources, but the deployment evidence
does not prove an MVP journey: frontend publication fails on an unpinned
Terraform version, and the runtime smoke stops after queueing an invalid PDF.

## What Changes

- Pin the frontend deployment job to the Terraform version supported by the
  live stack, resolve live API/Cognito outputs, and build the published assets
  with that configuration.
- Exercise a valid supported document through multipart upload, analysis,
  export, and result download in the real AWS runtime smoke.
- Report actionable presigned-upload errors without logging signed URLs.
- Verify the deployed CloudFront entry page and Cognito sign-in transition in
  a real browser.

## Capabilities

### New Capabilities

- `deployed-mvp-verification`: Defines the live AWS and browser proof required
  for the upload, analysis, export, and download MVP path.

### Modified Capabilities

- `infrastructure-app-edge-auth-api`: Requires the frontend deployment workflow
  to use the supported Terraform toolchain and publish the real React build.

## Impact

- Affects the frontend GitHub Actions workflow, AWS runtime smoke tooling,
  deployment documentation, and live verification procedure.
- Does not change public API contracts or persistent data models.
