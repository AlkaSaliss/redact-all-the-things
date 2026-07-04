## 1. OpenSpec

- [x] 1.1 Document the combined-scope governance exception.
- [x] 1.2 Add requirements for preview APIs, frontend auth/upload/review, and render export.

## 2. Backend and Worker

- [x] 2.1 Verify existing #21 worker manifest integration remains in place.
- [x] 2.2 Add owner-checked page summary and preview URL APIs.
- [x] 2.3 Add render-mode worker output generation from page artifacts and manifests.
- [x] 2.4 Add focused API and worker tests.

## 3. Frontend

- [x] 3.1 Add React/Vite/TypeScript npm frontend scaffold.
- [x] 3.2 Add Cognito Hosted UI auth boundary and live API client.
- [x] 3.3 Add contract fixtures and API mapping tests.
- [x] 3.4 Add upload, dashboard, review editor, autosave, and export confirmation UI.

## 4. Infrastructure and CI

- [x] 4.1 Add Cognito Hosted UI Terraform configuration and outputs.
- [x] 4.2 Add API and S3 CORS for CloudFront and localhost frontend origins.
- [x] 4.3 Add frontend CI build/test and main/manual deployment sync.

## 5. Verification

- [x] 5.1 Run focused backend tests.
- [x] 5.2 Run frontend tests and build.
- [x] 5.3 Run strict MkDocs and OpenSpec validation.
- [x] 5.4 Run Terraform validation.
- [x] 5.5 Run Graphify update.
