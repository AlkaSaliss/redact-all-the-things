.DEFAULT_GOAL := help

.PHONY: help localstack-up localstack-down test test-worker docs openspec-validate worker-image worker-ocr-smoke

help: ## Show available make targets.
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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

worker-image: ## Build the local OCR worker image.
	docker build --platform linux/amd64 -f Dockerfile.worker -t redact-worker-ocr:test .

worker-ocr-smoke: worker-image ## Run OCR worker smoke test against tests/samples.
	docker run --rm --platform linux/amd64 -v "$(CURDIR)":/workspace -w /workspace redact-worker-ocr:test python tools/worker_ocr_smoke.py tests/samples/dlptest-name-dob-email.pdf tests/samples/Passport_of_Austria_\(2024\)_data_page.jpg
