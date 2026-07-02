## 1. OpenSpec

- [x] 1.1 Add proposal, design, specs, and tasks for the worker compute slice.

## 2. Terraform and Terragrunt

- [x] 2.1 Add a worker compute Terraform module that composes the app module.
- [x] 2.2 Model ECR, Batch/Fargate Spot compute environment, job queue,
  analyze/render job definitions, IAM, logs, and worker networking.
- [x] 2.3 Add minimal worker stubs for infrastructure wiring only.
- [x] 2.4 Point the Floci Terragrunt live config at the worker compute module.
- [x] 2.5 Extend infrastructure validation targets to cover the worker module.

## 3. Documentation and Smoke

- [x] 3.1 Update infrastructure docs with worker compute resources and emulator
  coverage boundaries.
- [x] 3.2 Update smoke output to distinguish worker compute static validation
  from emulator service coverage.

## 4. Verification

- [x] 4.1 Run `uv run pre-commit run --all-files`.
- [x] 4.2 Run `openspec validate --all --strict --no-interactive`.
- [x] 4.3 Run `uv run mkdocs build --strict`.
- [x] 4.4 Run `make terragrunt-validate`.
- [x] 4.5 Run `FLOCI_ENDPOINT_URL=http://127.0.0.1:4566 make terragrunt-plan-floci`.
- [ ] 4.6 Run `FLOCI_ENDPOINT_URL=http://127.0.0.1:4566 make infra-smoke-floci`.
- [x] 4.7 Run `uv run pytest`.
- [ ] 4.8 Refresh Graphify after infrastructure and architecture changes.
