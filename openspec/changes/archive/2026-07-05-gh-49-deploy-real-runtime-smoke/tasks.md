# Tasks

- [x] 1. Package and deploy the real control-plane Lambda instead of the stub.
- [x] 2. Wire Lambda Batch environment and submit permissions to real analyze
  and render job definitions.
- [x] 3. Add the real worker runtime entrypoint and update Batch job definitions
  to invoke it with the configured worker image tag.
- [x] 4. Add worker outbound network wiring for real AWS Batch/Fargate tasks.
- [x] 5. Normalize multipart upload completion and add focused tests.
- [x] 6. Add real runtime smoke tooling and update documentation/workflow
  references.
- [x] 7. Run focused tests, Terraform/OpenSpec validation, docs build, Graphify
  update, and the first real E2E smoke when credentials and account access are
  available.
  - Completed local verification: full pytest suite, MkDocs strict build,
    OpenSpec validation, Terraform formatting, workflow YAML lint, and Python
    compile checks.
  - Deferred environment-backed verification: Lambda package dependency
    download, Terraform validate/plan/apply with Terraform 1.13, Graphify
    refresh, and AWS E2E smoke. These require network access, the approved AWS
    account, or local toolchain updates outside this sandbox.
