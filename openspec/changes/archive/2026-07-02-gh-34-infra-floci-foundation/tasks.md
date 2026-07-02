## 1. OpenSpec and Governance

- [x] 1.1 Add proposal, design, specs, and tasks for the Floci foundation.
- [x] 1.2 Update roadmap/development/architecture docs with the approved issue
  #4 roadmap override and emulator boundary.

## 2. Infrastructure Foundation

- [x] 2.1 Add a Terragrunt live environment for Floci using local state.
- [x] 2.2 Add a reusable Terraform foundation module with provider endpoint
  configuration driven by `FLOCI_ENDPOINT_URL`.
- [x] 2.3 Add repository scripts that validate required Floci environment
  variables and perform a lightweight endpoint check.

## 3. Developer Commands

- [x] 3.1 Add Make targets for `floci-up`, `floci-check`,
  `terragrunt-validate`, `terragrunt-plan-floci`, `terragrunt-apply-floci`,
  and `infra-smoke-floci`.
- [x] 3.2 Ensure Floci plan/apply/smoke targets fail clearly when
  `FLOCI_ENDPOINT_URL` is missing.

## 4. Verification

- [x] 4.1 Run `openspec validate --all --strict --no-interactive`.
- [x] 4.2 Run `uv run mkdocs build --strict`.
- [x] 4.3 Run available Terragrunt validation or report missing local tooling.
- [x] 4.4 Refresh Graphify after documentation and infrastructure files change.
