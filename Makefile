.DEFAULT_GOAL := help

.PHONY: help localstack-up localstack-down test test-worker docs openspec-validate

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
