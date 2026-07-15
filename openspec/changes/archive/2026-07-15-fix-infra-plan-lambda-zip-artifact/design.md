## Context

`aws_lambda_function.filename` is an upload input, but the AWS provider stores
the configured path in state. The real dev stack was last applied from a CI path
and local plans use a different `.build/control-plane-lambda.zip` path, so
Terraform planned an in-place Lambda update when the package path changed. A
targeted local apply also failed because the provider tried to read the stale CI
path from state while applying a real package hash update.

## Decision

Upload the generated ZIP to a private encrypted S3 package bucket and configure
the Lambda function with `s3_bucket` and `s3_key` instead of `filename`. Keep
`source_code_hash = filebase64sha256(local.lambda_package_path)` as the
deployment signal so real package-content changes remain visible. The S3 object
uses the same package hash as `source_hash` instead of ETag because larger ZIPs
can receive multipart S3 ETags that are not equal to the local file MD5.

The package builder writes ZIP entries with sorted paths, fixed timestamps,
fixed file permissions, and no `__pycache__`/`.pyc` files so unchanged inputs
produce the same package hash.

Local AWS plan/apply defaults use the current git commit as the worker image
tag. CI deploys the worker image with that tag, so local plans do not propose a
Batch job-definition revision back to `local` unless the operator explicitly
overrides `WORKER_IMAGE_TAG`.

## Risks

- A package rebuild with changed contents still updates the S3 object and
  Lambda `source_code_hash`.
- The package bucket must not share the 24-hour artifact lifecycle policy used
  for user files.
- Planning from an unpushed local commit still requires a pushed worker image
  tag before apply.
