.DEFAULT_GOAL := help

.PHONY: help localstack-up localstack-down test test-worker docs openspec-validate worker-image worker-ocr-smoke floci-up floci-check terragrunt-validate terragrunt-plan-floci terragrunt-apply-floci infra-smoke-floci

help: ## Show available make targets.
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

AWS_REGION ?= eu-west-1
AWS_ACCESS_KEY_ID ?= floci
AWS_SECRET_ACCESS_KEY ?= floci
FLOCI_ENV_DIR ?= infra/live/floci
TERRAGRUNT ?= terragrunt
TERRAFORM ?= terraform

localstack-up: ## Start the pinned LocalStack service for local AWS tests.
	docker compose up -d localstack

localstack-down: ## Stop local Docker Compose services.
	docker compose down

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
	@[ -n "$$FLOCI_START_CMD" ] || { echo "FLOCI_START_CMD is required"; exit 2; }
	$(SHELL) -lc "$$FLOCI_START_CMD"

floci-check: ## Verify FLOCI_ENDPOINT_URL points at a reachable endpoint.
	./tools/check_floci.sh

terragrunt-validate: ## Validate Terraform modules and Terragrunt HCL.
	$(TERRAFORM) -chdir=infra/modules/foundation fmt -check
	$(TERRAFORM) -chdir=infra/modules/foundation validate
	$(TERRAGRUNT) hcl format --check $(FLOCI_ENV_DIR)/terragrunt.hcl

terragrunt-plan-floci: floci-check ## Generate a Terragrunt plan against Floci.
	cd $(FLOCI_ENV_DIR) && AWS_REGION=$(AWS_REGION) AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) $(TERRAGRUNT) plan

terragrunt-apply-floci: floci-check ## Apply the Floci Terragrunt environment.
	cd $(FLOCI_ENV_DIR) && AWS_REGION=$(AWS_REGION) AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) $(TERRAGRUNT) apply

infra-smoke-floci: ## Run Floci foundation smoke checks.
	./tools/infra_smoke_floci.sh

pre-commit:
	@echo "Pre-Commit Checks"
	@uv run pre-commit run --all-files
