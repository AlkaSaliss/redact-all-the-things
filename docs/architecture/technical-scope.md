# Technical Scope: Assisted File Redaction Application

## 1. Objective

Build a private web application that enables invited users to:

1. Upload a PDF, JPEG, or PNG.
2. Automatically identify textual PII.
3. Review and modify proposed redactions.
4. Export a permanently redacted file.
5. Access the job for up to 24 hours.

The system will run entirely within AWS and target an operating cost below
EUR 25 per month for approximately 1,500 pages processed monthly.

## 2. Scope

### In Scope

- Cognito-managed invited users.
- One file per processing job.
- PDF files up to 200 pages.
- Files up to 100 MB.
- JPEG and PNG images.
- PaddleOCR processing of every page.
- GLiNER2 PII detection.
- Review and manual redaction editor.
- Rasterized PDF output.
- Metadata-stripped image output.
- Resumable jobs and review sessions.
- Automatic expiration after 24 hours.
- Terraform and Terragrunt infrastructure.
- GitHub Actions deployment using AWS OIDC.

### Out of Scope

- Public registration.
- Anonymous access.
- Mobile and tablet editing.
- Batch uploads.
- Permanent document storage.
- Native PDF text extraction.
- Searchable PDF output.
- Automatic face or signature detection.
- External OCR or AI APIs.
- In-app user administration.
- Formal multilingual accuracy guarantees.
- Multiple production environments.

## 3. Functional Requirements

### Authentication

- Only Cognito users created by an AWS administrator may sign in.
- Users may access only their own jobs and files.
- The application will not provide registration or account-management screens.

### Upload

- Accept PDF, JPEG, and PNG files.
- Enforce a 100 MB maximum file size.
- Enforce a 200-page PDF limit.
- Reject encrypted, corrupt, or unsupported files.
- Upload directly to S3 using short-lived presigned multipart URLs.
- Display upload progress and cancellation controls.

### Analysis

- Rasterize every PDF page using PDFium through `pypdfium2`.
- Run PaddleOCR on every rasterized page and uploaded image.
- Construct an ordered text stream while preserving mappings to OCR polygons.
- Run a pinned GLiNER2 model against the extracted text.
- Favor recall when configuring detection confidence thresholds.
- Convert detected spans into normalized redaction rectangles.
- Select every detected PII region by default.
- Checkpoint completed pages to support interruption recovery.

### Review

- Present a desktop document editor containing:
  - Page thumbnails.
  - Per-page suggestion counts.
  - Zoomable page canvas.
  - Editable redaction rectangles.
  - PII category and confidence details.
  - Next and previous suggestion navigation.
  - Manual rectangle creation.
  - Region resize and deletion.
  - Session undo and redo.
- Autosave changes independently for each page.
- Display saving, saved, and failed states.
- Allow users to leave and resume from the recent-jobs dashboard.
- Require explicit acknowledgement that automated detection may miss PII before
  export.

### Export

- Submit export as a separate asynchronous job.
- Burn opaque rectangles into output pixels.
- Rebuild PDFs exclusively from rasterized pages.
- Remove PDF text layers, metadata, annotations, attachments, and forms.
- Remove metadata from JPEG and PNG outputs.
- Preserve the source image format for image inputs.
- Provide a short-lived download URL after export completes.

### Retention

- Deny access exactly 24 hours after job creation.
- Use S3 and DynamoDB lifecycle policies for eventual physical cleanup.
- Display job expiry times in the UI.

## 4. System Architecture

### Frontend

- React and TypeScript single-page application.
- Hosted in a private S3 bucket.
- Distributed through CloudFront using Origin Access Control.
- Initially use the generated CloudFront domain.

### Control Plane

- API Gateway HTTP API.
- Cognito JWT authorization.
- Python Lambda API.
- Responsibilities:
  - Job creation.
  - Ownership enforcement.
  - Presigned URL generation.
  - Job listing and retrieval.
  - Page manifest updates.
  - Batch submission and retry.
  - Export confirmation.
  - Download authorization.

### Persistence

#### Amazon S3

Store:

- Original uploads.
- Page previews.
- OCR and detection manifests.
- User redaction manifests.
- Exported files.

Object keys will be namespaced by Cognito user ID and job ID.

#### Amazon DynamoDB

Store:

- Job ownership.
- Job status.
- Creation and expiry timestamps.
- Page count.
- Processing progress.
- Model versions.
- Safe failure information.

Extracted text and PII values must not be stored in DynamoDB.

### Processing

- AWS Batch using Fargate Spot.
- One active worker globally.
- CPU-only container, initially sized at 2 vCPU and 8 GB RAM.
- Two job modes:
  - `analyze`
  - `render`
- Process pages sequentially to bound memory usage.
- Resume interrupted analysis from page checkpoints.
- Retry only transient infrastructure and Spot failures.

### Region

Deploy initially to `eu-west-1`.

This selection is based on the official AWS regional price index available
during scoping and must be revalidated before the initial deployment.

## 5. Core Data Model

### Job

```text
id
owner_id
source_type
source_key
output_key
status
page_count
completed_pages
created_at
expires_at
model_versions
failure_code
version
```

### Job Status

```text
uploading
queued
analyzing
ready
exporting
complete
failed
expired
```

### Redaction Region

```text
id
page_number
x
y
width
height
source        # automatic | manual
category
confidence
selected
```

Coordinates will be normalized relative to page dimensions so rendering
remains stable across preview and export resolutions.

### Page Manifest

Each page manifest will distinguish:

- Immutable model suggestions.
- Current user-selected regions.
- Manifest version.
- Last-save timestamp.

Updates will use optimistic version checks to prevent accidental overwrites.

## 6. Security Requirements

- Block all public S3 access.
- Enable encryption at rest.
- Use TLS for all network communication.
- Use short-lived, object-specific presigned URLs.
- Verify job ownership on every API operation.
- Never trust user-provided MIME types or file extensions.
- Validate file signatures and decoded content.
- Constrain page dimensions and image decompression.
- Run containers as a non-root user.
- Use a read-only container root filesystem.
- Give workers no inbound network access.
- Apply least-privilege IAM policies.
- Do not send document content to third-party APIs.
- Do not log:
  - Filenames.
  - OCR text.
  - Detected PII.
  - Page manifests.
  - File contents.
  - Presigned URLs.

Pinned model artifacts must be included in the worker image so production jobs
do not download models dynamically.

## 7. Cost Controls

- No NAT Gateway.
- No continuously running application servers.
- No GPU infrastructure.
- One active Batch worker globally.
- Fargate Spot for processing.
- Static frontend hosting.
- Serverless control plane.
- Lifecycle cleanup after 24 hours.
- Seven-day CloudWatch log retention.
- AWS Budget alerts before and at the EUR 25 threshold.
- Image and dependency versions pinned to prevent unexpected runtime changes.

The EUR 25 target assumes approximately five 10-page files per day. The 100 MB
and 200-page limits are safety ceilings, not expected average usage.

## 8. Infrastructure and Delivery

Infrastructure will be defined using Terraform modules composed through
Terragrunt.

GitHub Actions will:

1. Run frontend and backend tests.
2. Run linting and type checks.
3. Scan dependencies and container images.
4. Build the worker image.
5. Publish versioned images to ECR.
6. Validate Terraform.
7. Generate a Terragrunt plan.
8. Require approval before applying production changes.
9. Authenticate to AWS using OIDC rather than stored access keys.

Local development will use containers and mocked AWS clients. A separate AWS
development environment is excluded from the initial scope.

## 9. Testing Strategy

### Unit Tests

Cover:

- File signature validation.
- File and page limits.
- Encrypted and corrupt PDFs.
- OCR fragment ordering.
- GLiNER span-to-polygon mapping.
- Multiline entities.
- Coordinate normalization.
- Checkpoint recovery.
- Failure classification.
- Manifest version conflicts.

### Quality Regression Tests

Use generated, non-sensitive fixtures containing:

- Known PII categories.
- Multiple layouts and font sizes.
- Rotated text.
- Several representative scripts.
- PDF, JPEG, and PNG inputs.

CI must detect regressions when model or threshold versions change. These
fixtures do not establish a general multilingual accuracy guarantee.

### Redaction Security Tests

Verify that:

- Selected regions are fully opaque.
- Exported PDFs contain raster pages only.
- Original text cannot be extracted.
- Canary strings are absent.
- Metadata is removed.
- PDF annotations, forms, attachments, and embedded content are absent.
- Re-running OCR cannot recover visibly selected text.

### Integration Tests

Cover:

- Cognito authorization.
- Cross-user isolation.
- Presigned URL scope and expiry.
- Job state transitions.
- Page manifest persistence.
- Retry behavior.
- 24-hour access expiration.
- Batch job submission and completion.

### UI Tests

Cover:

- Upload validation and progress.
- Dashboard status states.
- Job resume.
- Rectangle creation, resizing, and deletion.
- Autosave recovery.
- Zoom coordinate stability.
- Keyboard interactions.
- Export confirmation.
- Expired jobs.

Test current desktop releases of Chrome, Firefox, Safari, and Edge.

### Performance Acceptance

- Memory remains below 8 GB.
- Processing streams one page at a time.
- Forced worker termination resumes from checkpoints.
- No more than one worker runs concurrently.
- A 200-page synthetic PDF completes without memory exhaustion.
- The expected workload projects below EUR 25 per month.

## 10. Acceptance Criteria

The scope is complete when:

1. An invited user can authenticate.
2. The user can upload each supported file type.
3. Invalid and encrypted files are rejected safely.
4. Processing continues after the browser is closed.
5. PaddleOCR and GLiNER2 produce reviewable regions.
6. The user can add, remove, and resize redactions.
7. Review state persists across sessions.
8. Export produces a permanently rasterized result.
9. Another user cannot discover or access the job.
10. Access is denied after 24 hours.
11. Spot interruption recovery works from checkpoints.
12. The expected workload meets the documented cost target.

## 11. Principal Risks

- PaddleOCR on every page may make the EUR 25 budget sensitive to unusually
  large jobs.
- CPU inference may produce long queues for 200-page files.
- GLiNER2 may miss PII or produce false positives, especially across languages
  and unusual layouts.
- OCR polygon-to-entity mapping may be ambiguous for fragmented or multiline
  text.
- Fargate Spot tasks may be interrupted and require robust checkpoint
  recovery.
- Rasterized output may be larger and less accessible than the original
  document.

The mandatory review step, cost controls, synthetic regression corpus, and
checkpointed processing mitigate these risks without expanding the initial
scope.

## 12. References

- [AWS Batch pricing](https://aws.amazon.com/batch/pricing/)
- [AWS Fargate pricing](https://aws.amazon.com/fargate/pricing/)
- [AWS Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- [Official AWS ECS regional price index](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECS/current/region_index.json)
