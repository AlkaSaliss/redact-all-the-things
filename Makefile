.DEFAULT_GOAL := help

.PHONY: help test test-worker docs openspec-validate frontend-test frontend-build frontend-env-local frontend-dev lambda-package worker-image worker-ocr-smoke floci-up floci-down floci-check terragrunt-validate terragrunt-plan terragrunt-apply terragrunt-plan-local terragrunt-apply-local terragrunt-plan-aws terragrunt-apply-aws infra-smoke-floci infra-smoke-aws

help: ## Show available make targets.
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

INFRA_TARGET ?= floci
INFRA_REGION ?= eu-west-1
INFRA_COMPONENT ?= worker-compute-artifacts
INFRA_ROOT_FOLDER ?= infra
INFRA_ENV_DIR ?= infra/live/$(INFRA_TARGET)/$(INFRA_REGION)/$(INFRA_COMPONENT)
AWS_ENV_DIR ?= infra/live/dev/$(INFRA_REGION)/$(INFRA_COMPONENT)
FRONTEND_ENV_FILE ?= frontend/.env.local
LAMBDA_PACKAGE_PATH ?= $(CURDIR)/.build/control-plane-lambda.zip
WORKER_IMAGE_TAG ?= $(shell git rev-parse HEAD)
FLOCI_ENV_DIR ?= infra/live/floci/$(INFRA_REGION)/$(INFRA_COMPONENT)
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

frontend-test: ## Run frontend unit tests.
	cd frontend && npm test

frontend-build: ## Build the frontend application.
	cd frontend && npm run build

frontend-env-local: ## Generate frontend/.env.local from the real dev stack outputs.
	@set -eu; \
	if { [ -z "$${TG_STATE_BUCKET:-}" ] || [ -z "$${TG_LOCK_TABLE:-}" ]; } && [ -f tools/set_local_env_vars.sh ]; then \
		. tools/set_local_env_vars.sh; \
	fi; \
	if [ -z "$${AWS_ACCESS_KEY_ID:-}" ] && [ -f tools/set_local_aws_credentials.sh ]; then \
		. tools/set_local_aws_credentials.sh; \
	fi; \
	if [ -z "$${TG_STATE_BUCKET:-}" ] || [ -z "$${TG_LOCK_TABLE:-}" ]; then \
		echo "Missing TG_STATE_BUCKET or TG_LOCK_TABLE. Run: . tools/set_local_env_vars.sh"; \
		exit 1; \
	fi; \
	if [ ! -d "$(AWS_ENV_DIR)" ]; then \
		echo "Missing AWS stack directory: $(AWS_ENV_DIR)"; \
		exit 1; \
	fi; \
	api_endpoint=$$(cd "$(AWS_ENV_DIR)" && $(TERRAGRUNT) output -raw api_endpoint); \
	user_pool_id=$$(cd "$(AWS_ENV_DIR)" && $(TERRAGRUNT) output -raw user_pool_id); \
	web_client_id=$$(cd "$(AWS_ENV_DIR)" && $(TERRAGRUNT) output -raw web_client_id); \
	hosted_ui_url=$$(cd "$(AWS_ENV_DIR)" && $(TERRAGRUNT) output -raw hosted_ui_url); \
	cp frontend/.env.example "$(FRONTEND_ENV_FILE)"; \
	{ \
		printf '%s\n' "VITE_API_ENDPOINT=$$api_endpoint"; \
		printf '%s\n' "VITE_AWS_REGION=$(INFRA_REGION)"; \
		printf '%s\n' "VITE_COGNITO_USER_POOL_ID=$$user_pool_id"; \
		printf '%s\n' "VITE_COGNITO_CLIENT_ID=$$web_client_id"; \
		printf '%s\n' "VITE_COGNITO_HOSTED_UI_URL=$$hosted_ui_url"; \
	} > "$(FRONTEND_ENV_FILE)"; \
	echo "Wrote $(FRONTEND_ENV_FILE) from $(AWS_ENV_DIR) outputs."

frontend-dev: ## Start the frontend dev server using frontend/.env.local.
	@if [ ! -f "$(FRONTEND_ENV_FILE)" ]; then \
		echo "Missing $(FRONTEND_ENV_FILE). Run: make frontend-env-local"; \
		exit 1; \
	fi
	cd frontend && npm run dev -- --host localhost --port 5173 --strictPort

lambda-package: ## Build the control-plane Lambda ZIP package.
	./tools/build_lambda_package.sh "$(LAMBDA_PACKAGE_PATH)"

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
	$(TERRAGRUNT) hcl format --check infra/root.hcl
	$(TERRAGRUNT) hcl format --check infra/live/dev/env.hcl
	$(TERRAGRUNT) hcl format --check infra/live/dev/$(INFRA_REGION)/region.hcl
	$(TERRAGRUNT) hcl format --check infra/live/dev/$(INFRA_REGION)/$(INFRA_COMPONENT)/terragrunt.hcl
	$(TERRAGRUNT) hcl format --check infra/live/floci/env.hcl
	$(TERRAGRUNT) hcl format --check infra/live/floci/$(INFRA_REGION)/region.hcl
	$(TERRAGRUNT) hcl format --check infra/live/floci/$(INFRA_REGION)/$(INFRA_COMPONENT)/terragrunt.hcl

terragrunt-plan: ## Generate a Terragrunt plan for INFRA_TARGET=floci or dev.
	@if [ "$(INFRA_TARGET)" = "floci" ]; then \
		$(MAKE) terragrunt-plan-local; \
	else \
		cd $(INFRA_ENV_DIR) && $(TERRAGRUNT) plan; \
	fi

terragrunt-apply: ## Apply INFRA_TARGET=floci or dev.
	@if [ "$(INFRA_TARGET)" = "floci" ]; then \
		$(MAKE) terragrunt-apply-local; \
	else \
		cd $(INFRA_ENV_DIR) && $(TERRAGRUNT) apply; \
	fi

terragrunt-plan-local: floci-check ## Generate a Terragrunt plan against Floci.
	@export $(FLOCI_ENV) && cd $(FLOCI_ENV_DIR) && $(TERRAGRUNT) plan

terragrunt-apply-local: floci-check ## Apply the Floci Terragrunt environment.
	@export $(FLOCI_ENV) && cd $(FLOCI_ENV_DIR) && $(TERRAGRUNT) apply

terragrunt-plan-aws: lambda-package ## Generate a Terragrunt plan against the configured AWS account.
	@TF_VAR_lambda_package_path="$(LAMBDA_PACKAGE_PATH)" TF_VAR_worker_image_tag="$(WORKER_IMAGE_TAG)" $(MAKE) terragrunt-plan INFRA_TARGET=dev

terragrunt-apply-aws: lambda-package ## Apply against the configured AWS account.
	@TF_VAR_lambda_package_path="$(LAMBDA_PACKAGE_PATH)" TF_VAR_worker_image_tag="$(WORKER_IMAGE_TAG)" $(MAKE) terragrunt-apply INFRA_TARGET=dev

infra-smoke-floci: ## Run Floci foundation smoke checks.
	@export $(FLOCI_ENV) && ./tools/infra_smoke_floci.sh

infra-smoke-aws: ## Run read-only smoke checks against the configured AWS live stack.
	@./tools/infra_smoke_aws.sh

pre-commit:  ## Run pre-commit checks.
	@echo "Pre-Commit Checks"
	@uv run pre-commit run --all-files

tf-clean:  ## Recursively clean Terraform/Terragrunt caches under INFRA_ROOT_FOLDER.
	@echo "Recursively cleaning Terraform/Terragrunt caches under: $(INFRA_ROOT_FOLDER)"
	@find "$(INFRA_ROOT_FOLDER)" -type d \( -name ".terragrunt-cache" -o -name ".terraform" \) -exec rm -rf {} + 2>/dev/null
	@find "$(INFRA_ROOT_FOLDER)" -type f -name ".terraform.lock.hcl" -delete 2>/dev/null
	@find "$(INFRA_ROOT_FOLDER)" -type f -name "terraform.tfstate.backup" -delete 2>/dev/null
	@find "$(INFRA_ROOT_FOLDER)" -type f -name "*.tfplan" -delete 2>/dev/null
	@find "$(INFRA_ROOT_FOLDER)" -type f -name "crash.log" -delete 2>/dev/null
	@echo "Done."
