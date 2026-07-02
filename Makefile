.DEFAULT_GOAL := help

.PHONY: help test test-worker docs openspec-validate worker-image worker-ocr-smoke floci-up floci-down floci-check terragrunt-validate terragrunt-plan-local terragrunt-apply-local infra-smoke-floci

help: ## Show available make targets.
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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

floci-up: ## Start Floci using FLOCI_START_CMD.
	@export $(FLOCI_ENV) && \
	mkdir -p "$(CURDIR)/local-data" && \
	floci aws start --persist "$(CURDIR)/local-data/floci-state"

floci-down: ## Stop Floci using FLOCI_START_CMD.
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

terragrunt-plan-local: floci-check ## Generate a Terragrunt plan against Floci.
	@export $(FLOCI_ENV) && cd $(FLOCI_ENV_DIR) && $(TERRAGRUNT) plan

terragrunt-apply-local: floci-check ## Apply the Floci Terragrunt environment.
	@export $(FLOCI_ENV) && cd $(FLOCI_ENV_DIR) && $(TERRAGRUNT) apply

infra-smoke-floci: ## Run Floci foundation smoke checks.
	./tools/infra_smoke_floci.sh

pre-commit:
	@echo "Pre-Commit Checks"
	@uv run pre-commit run --all-files
