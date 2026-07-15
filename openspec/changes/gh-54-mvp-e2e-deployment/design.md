## Context

The live stack contains CloudFront, Cognito, API Gateway/Lambda, S3,
DynamoDB, ECR, and AWS Batch. The frontend build succeeds but its deployment
job resolves Terragrunt outputs with an unpinned Terraform version. The current
AWS runtime smoke invokes Lambda and uses a presigned upload URL, but uploads
invalid placeholder bytes and exits immediately after analysis submission.

## Goals / Non-Goals

**Goals:**

- Publish the real frontend using the repository-supported Terraform version.
- Prove valid analysis and render workers reach terminal success in AWS.
- Keep the smoke bounded, actionable, and safe for approved CI applies.
- Exercise the public CloudFront-to-Cognito entry transition in a browser.

**Non-Goals:**

- Complete all production-readiness checks in parent epic #3.
- Add test-only API routes, worker modes, or persistent fixtures.
- Automate invited-user credentials in repository or browser artifacts.
- Add AWS budget alerts tracked by issue #42.

## Decisions

### Use the existing valid PDF sample

The runtime smoke uploads `tests/samples/dlptest-name-dob-email.pdf`. This
exercises PDF validation, rasterization, OCR, PII mapping, manifest persistence,
rendering, and result storage without introducing a generated or synthetic
runtime-only format. A custom minimal PDF was rejected because it would not
exercise meaningful OCR and previously produced a validation failure.

### Poll the control-plane job contract

After upload completion, the smoke polls `GET /jobs/{id}` until `ready` or a
terminal failure, confirms export, then polls until `complete`. Polling has a
fixed interval and deadline and includes the final safe job status/failure code
in errors. Direct Batch polling was rejected because the user-visible contract
is the job lifecycle persisted by the worker.

### Keep presigned transfers in the proof

Uploads and downloads use the URLs returned by the control plane. This covers
the same S3 authorization boundary used by the browser. HTTP errors include the
status and sanitized response body but never print the signed URL.

### Pin Terraform in every workflow job that invokes Terragrunt

The frontend deploy job uses the same `TERRAFORM_VERSION` and
`hashicorp/setup-terraform` input as infrastructure jobs. Relaxing module
version constraints was rejected because it would make an unrelated deployment
job choose an unverified Terraform release.

### Build deployable assets after resolving live outputs

The deploy job reads the API and Cognito Terragrunt outputs, then runs the Vite
build with those values before S3 synchronization. Reusing the generic build
job artifact was rejected because Vite embeds environment variables at build
time and that artifact has no live configuration. Runtime configuration
loading was rejected for this slice because it would add a new application
bootstrapping contract when a deployment-only rebuild is sufficient.

## Risks / Trade-offs

- **Worker model cold starts can be slow** -> use an explicit configurable
  deadline with a conservative CI default and concise progress output.
- **The smoke incurs AWS compute cost** -> keep it opt-in behind
  `AWS_E2E_SMOKE=1` and use a one-page sample.
- **Cognito credentials are operator-owned** -> browser verification proves the
  public redirect boundary; authenticated data-path proof uses Lambda claims in
  the existing approved smoke harness.
- **A failed smoke can leave 24-hour artifacts** -> rely on the existing bucket
  lifecycle and DynamoDB TTL; use a dedicated owner namespace.

## Migration Plan

1. Merge the workflow and smoke changes.
2. Dispatch the infrastructure apply workflow to publish the current worker
   image and execute the full runtime smoke.
3. Dispatch or merge the frontend workflow to publish the built application.
4. Verify CloudFront and Cognito in a browser.
5. Roll back by reverting the workflow/smoke changes; deployed application
   resources and API contracts are unchanged.

## Open Questions

None for this slice.
