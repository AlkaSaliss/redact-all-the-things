# ADR 0002: Define control-plane boundaries and persistence

- **Status:** Accepted
- **Date:** 2026-06-15
- **Decision owners:** `@AlkaSaliss`

## Context

The analysis worker and frontend require one stable contract for job lifecycle,
ownership, expiry, page manifests, object access, and worker submission. The
technical scope requires a Python Lambda API, DynamoDB job metadata, S3
document and manifest storage, and AWS Batch processing while prohibiting OCR
text and PII values in DynamoDB.

Local validation must not require an AWS account. LocalStack Community supports
the required DynamoDB and S3 behavior but does not include AWS Batch.

## Decision

- Keep strict Pydantic domain contracts and lifecycle rules independent of
  FastAPI and boto3 request shapes.
- Use FastAPI for HTTP validation and OpenAPI, exposed to Lambda through
  Mangum.
- Read ownership only from the API Gateway Cognito JWT subject.
- Store job metadata, optimistic versions, and TTL values in DynamoDB.
- Store page manifests and file artifacts under owner/job-namespaced S3 keys.
- Enforce job versions through DynamoDB conditions and manifest versions
  through S3 ETag conditions.
- Validate DynamoDB and S3 integration against pinned LocalStack `4.14.0`.
- Use a minimal recording Batch fake only in local tests; use the real boto3
  Batch client in the Lambda runtime.

## Consequences

- Worker and frontend milestones receive versioned, validated shared fixtures.
- Exact 24-hour access expiry is enforced by application logic rather than
  eventual cleanup.
- Sensitive manifest content remains outside DynamoDB.
- Local persistence tests exercise AWS-compatible endpoints rather than custom
  in-memory repositories.
- Batch request compatibility remains unverified locally and must be covered by
  the infrastructure milestone's deployed AWS tests.

## Considered alternatives

- **Store page manifests in DynamoDB:** Rejected because manifests may contain
  detected PII categories and can grow beyond suitable item sizes.
- **Implement in-memory and mocked AWS adapters:** Rejected because they add
  test-only implementations and miss endpoint-level behavior covered by
  LocalStack.
- **Require paid LocalStack Batch support:** Rejected because local validation
  should not require a commercial emulator license.
- **Place lifecycle rules in Lambda handlers:** Rejected because the worker and
  API would risk implementing incompatible transitions.

## References

- [GitHub Issue #7](https://github.com/AlkaSaliss/redact-all-the-things/issues/7)
- OpenSpec change: `gh-7-control-plane-api`
- Pull request: pending
- [Control-plane API](../architecture/control-plane-api.md)
- [Technical scope](../architecture/technical-scope.md)
