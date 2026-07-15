## 1. Frontend Deployment

- [x] 1.1 Pin the frontend deploy job to the supported Terraform version.
- [x] 1.2 Validate the workflow installs Terraform before resolving live outputs.
- [x] 1.3 Build deployable assets with API and Cognito values from the live stack.

## 2. AWS Runtime Journey

- [x] 2.1 Upload the checked-in valid PDF sample through the presigned multipart URL.
- [x] 2.2 Add bounded job polling for ready, failed, complete, and timeout outcomes.
- [x] 2.3 Submit export and verify a non-empty authorized result download.
- [x] 2.4 Report sanitized presigned transfer errors without signed URLs.
- [x] 2.5 Add focused tests for polling and transfer error behavior.

## 3. Documentation And Verification

- [x] 3.1 Document the full opt-in runtime smoke and browser verification boundary.
- [x] 3.2 Run backend, frontend, OpenSpec, documentation, and infrastructure checks.
- [ ] 3.3 Run the full runtime smoke against the deployed AWS stack.
- [ ] 3.4 Verify the deployed CloudFront-to-Cognito entry flow in a real browser.
- [x] 3.5 Refresh Graphify after source and architecture changes.
