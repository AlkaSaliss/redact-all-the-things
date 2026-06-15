# Control-plane API

The Python control plane owns authenticated job lifecycle, object
authorization, page-manifest persistence, and asynchronous worker submission.
Its shared contracts are consumed by the analysis worker and React frontend.

## Local development

Install the locked environment and start LocalStack:

```bash
uv sync --locked
docker compose up -d localstack
uv run pytest
```

The Compose service pins `localstack/localstack:4.14.0` and exposes only
`127.0.0.1:4566`. Tests create isolated DynamoDB and S3 resources. LocalStack
Community does not include AWS Batch, so local tests use a minimal recording
fake that validates worker requests and idempotency without emulating
scheduling or execution.

Stop the emulator with:

```bash
docker compose down
```

## Authentication

Production requests obtain the owner identifier exclusively from the Cognito
JWT `sub` claim supplied in the API Gateway HTTP API authorizer context.
Request bodies cannot select an owner.

Tests may enable the explicitly test-only `x-test-cognito-sub` header. The
production Lambda application does not enable this header.

Missing authentication returns `401`. Missing, expired, and foreign-owned jobs
all return the same non-disclosing `404` response.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/jobs` | Create an uploading job and authorize multipart upload |
| `GET` | `/jobs` | List the owner's unexpired jobs |
| `GET` | `/jobs/{job_id}` | Retrieve an accessible job |
| `POST` | `/jobs/{job_id}/upload-complete` | Complete multipart upload and submit analysis |
| `GET` | `/jobs/{job_id}/pages/{page}/manifest` | Read a page manifest |
| `PUT` | `/jobs/{job_id}/pages/{page}/manifest` | Save regions with optimistic versioning |
| `POST` | `/jobs/{job_id}/export` | Confirm review and submit rendering |
| `GET` | `/jobs/{job_id}/download` | Authorize completed output download |
| `POST` | `/jobs/{job_id}/retry` | Retry an eligible transient failure |

FastAPI publishes the full request and response schema at `/openapi.json`.
Job creation returns one presigned upload URL per 5 MB part. Upload completion
accepts the upload ID plus each uploaded part number and ETag.

## Persistence

DynamoDB stores only job ownership, lifecycle, timestamps, progress, model
versions, safe failure codes, and optimistic versions. It also stores a numeric
TTL for eventual cleanup. It does not store filenames, OCR text, detected PII,
page manifests, file contents, or presigned URLs.

S3 stores source objects, output objects, and owner/job-namespaced page
manifests. Manifest updates compare both the integer manifest version and the
current S3 ETag before replacing the object.

Application services deny access at or after `expires_at`; DynamoDB TTL and S3
lifecycle processing are not used as authorization controls.

## Runtime configuration

The Lambda entry point requires:

- `JOBS_TABLE`
- `FILES_BUCKET`
- `BATCH_JOB_QUEUE`
- `BATCH_JOB_DEFINITION`

`AWS_REGION` defaults to `eu-west-1`. `AWS_ENDPOINT_URL` may point boto3 at a
local endpoint, but production omits it. The Lambda runtime uses the real AWS
Batch client; only local tests use the recording fake.
