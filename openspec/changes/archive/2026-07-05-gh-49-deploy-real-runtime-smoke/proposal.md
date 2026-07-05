# Deploy real runtime and smoke path

## Summary

Replace the infrastructure-only control-plane Lambda and worker stubs with the
real Python control-plane package, real worker image entrypoint, and network
runtime wiring needed for the first real AWS upload-to-worker smoke path.

## Motivation

The real AWS stack currently models the target resources but still deploys
placeholder Lambda and worker commands. Upload completion can submit only to
placeholder Batch wiring, and the worker subnets do not have an outbound route
for ECR, CloudWatch Logs, S3, DynamoDB, or Batch runtime calls. This prevents a
real E2E smoke from exercising the production Lambda, multipart upload
completion, and worker runtime.

## Scope

- Package and deploy the checked-in FastAPI/Mangum control-plane Lambda code.
- Wire the Lambda to deterministic real Batch queue and job-definition names.
- Add the IAM permissions required for Lambda Batch submission.
- Add a real worker container entrypoint for `analyze` and `render` Batch jobs.
- Point Batch job definitions at the real worker module entrypoint and image
  tag.
- Add outbound worker networking sufficient for the first AWS smoke.
- Normalize multipart upload completion input for real S3 compatibility.
- Add a smoke entrypoint that can create a job, upload a real part, complete
  the multipart upload, and observe worker submission/execution state.
- Update runtime documentation and verification commands.

## Out of Scope

- Frontend production artifact deployment.
- Budget alerts and account-specific notification targets.
- Reworking the Terraform module decomposition beyond the minimum needed
  runtime wiring.
- Replacing Cognito Hosted UI flows or adding new user-facing authentication
  features.
