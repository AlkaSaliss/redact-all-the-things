.DEFAULT_GOAL := help

.PHONY: help test test-worker docs openspec-validate worker-image worker-ocr-smoke floci-up floci-down floci-check terragrunt-validate terragrunt-plan terragrunt-apply terragrunt-plan-local terragrunt-apply-local terragrunt-plan-aws terragrunt-apply-aws infra-smoke-floci infra-smoke-aws terragrunt-plan-remote-state terragrunt-apply-remote-state infra-smoke-remote-state

help: ## Show available make targets.
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

INFRA_TARGET ?= floci
INFRA_ENV_DIR ?= infra/live/$(INFRA_TARGET)
FLOCI_ENV_DIR ?= infra/live/floci
FLOCI_ENV := AWS_ENDPOINT_URL=http://localhost.floci.io:4566 \
             AWS_ACCESS_KEY_ID=test \
             AWS_SECRET_ACCESS_KEY=test \
             AWS_DEFAULT_REGION=eu-west-1 \
             FLOCI_ENDPOINT_URL=http://localhost.floci.io:4566
TERRAGRUNT ?= terragrunt
TERRAFORM ?= terraform


test: ## Run the full test suite.
	uv run pytest

test-worker: ## Run focused worker and shared failure-code tests.
	uv run pytest tests/worker/test_validation.py tests/domain/test_lifecycle.py

docs: ## Build project documentation in strict mode.
	uv run mkdocs build --strict

openspec-validate: ## Validate all OpenSpec artifacts in strict mode.
	openspec validate --all --strict --no-interactive

worker-image: ## Build the local analysis worker image.
	docker build --platform linux/amd64 -f Dockerfile.worker -t redact-worker-ocr:test .

worker-ocr-smoke: worker-image ## Run OCR and PII worker smoke test against tests/samples.
	docker run --rm --platform linux/amd64 -v "$(CURDIR)":/workspace -w /workspace redact-worker-ocr:test python tools/worker_ocr_smoke.py tests/samples/dlptest-name-dob-email.pdf tests/samples/Passport_of_Austria_\(2024\)_data_page.jpg

floci-up: ## Start the local Floci AWS emulator.
	@export $(FLOCI_ENV) && \
	mkdir -p "$(CURDIR)/local-data" && \
	floci aws start --persist "$(CURDIR)/local-data/floci-state"

floci-down: ## Stop the local Floci AWS emulator.
	@floci aws stop

floci-check: ## Verify FLOCI_ENV's AWS_ENDPOINT_URL points at a reachable endpoint.
	@export $(FLOCI_ENV); \
	code=$$(curl --connect-timeout 2 --max-time 5 --silent --show-error \
		--output /dev/null --write-out "%{http_code}" "$$AWS_ENDPOINT_URL"); \
	if [ "$$code" -ge 200 ] && [ "$$code" -lt 500 ]; then \
		echo "✅ FLOCI is up at $$AWS_ENDPOINT_URL (HTTP $$code)"; \
	else \
		echo "❌ FLOCI unreachable at $$AWS_ENDPOINT_URL (HTTP $$code)"; \
		exit 1; \
	fi

terragrunt-validate: ## Validate Terraform modules and Terragrunt HCL.
	$(TERRAFORM) -chdir=infra/modules/foundation fmt -check
	$(TERRAFORM) -chdir=infra/modules/app-edge-auth-api fmt -check
	$(TERRAFORM) -chdir=infra/modules/worker-compute-artifacts fmt -check
	$(TERRAFORM) -chdir=infra/modules/foundation init -backend=false
	$(TERRAFORM) -chdir=infra/modules/foundation validate
	$(TERRAFORM) -chdir=infra/modules/app-edge-auth-api init -backend=false
	$(TERRAFORM) -chdir=infra/modules/app-edge-auth-api validate
	$(TERRAFORM) -chdir=infra/modules/worker-compute-artifacts init -backend=false
	$(TERRAFORM) -chdir=infra/modules/worker-compute-artifacts validate
	$(TERRAGRUNT) hcl format --check $(FLOCI_ENV_DIR)/terragrunt.hcl
	$(TERRAGRUNT) hcl format --check infra/live/aws/terragrunt.hcl
	$(TERRAFORM) -chdir=infra/modules/remote-state fmt -check
	$(TERRAFORM) -chdir=infra/modules/remote-state init -backend=false
	$(TERRAFORM) -chdir=infra/modules/remote-state validate
	$(TERRAGRUNT) hcl format --check infra/live/remote-state/terragrunt.hcl

terragrunt-plan: ## Generate a Terragrunt plan for INFRA_TARGET=floci or aws.
	@if [ "$(INFRA_TARGET)" = "floci" ]; then \
		$(MAKE) terragrunt-plan-local; \
	else \
		cd $(INFRA_ENV_DIR) && $(TERRAGRUNT) plan; \
	fi

terragrunt-apply: ## Apply INFRA_TARGET=floci or aws.
	@if [ "$(INFRA_TARGET)" = "floci" ]; then \
		$(MAKE) terragrunt-apply-local; \
	else \
		cd $(INFRA_ENV_DIR) && $(TERRAGRUNT) apply; \
	fi

terragrunt-plan-local: floci-check ## Generate a Terragrunt plan against Floci.
	@export $(FLOCI_ENV) && cd $(FLOCI_ENV_DIR) && $(TERRAGRUNT) plan

terragrunt-apply-local: floci-check ## Apply the Floci Terragrunt environment.
	@export $(FLOCI_ENV) && cd $(FLOCI_ENV_DIR) && $(TERRAGRUNT) apply

terragrunt-plan-aws: ## Generate a Terragrunt plan against the configured AWS account.
	@$(MAKE) terragrunt-plan INFRA_TARGET=aws

terragrunt-apply-aws: ## Apply against the configured AWS account.
	@$(MAKE) terragrunt-apply INFRA_TARGET=aws

infra-smoke-floci: ## Run Floci foundation smoke checks.
	@export $(FLOCI_ENV) && ./tools/infra_smoke_floci.sh

infra-smoke-aws: ## Run read-only smoke checks against the configured AWS live stack.
	@./tools/infra_smoke_aws.sh

terragrunt-plan-remote-state: ## Plan the remote-state bootstrap resources (S3 bucket + DynamoDB lock table).
	cd infra/live/remote-state && $(TERRAGRUNT) plan

terragrunt-apply-remote-state: ## Apply the remote-state bootstrap resources.
	cd infra/live/remote-state && $(TERRAGRUNT) apply

infra-smoke-remote-state: ## Run read-only smoke checks against deployed remote-state resources.
	@./tools/infra_smoke_remote_state.sh

pre-commit:
	@echo "Pre-Commit Checks"
	@uv run pre-commit run --all-files
