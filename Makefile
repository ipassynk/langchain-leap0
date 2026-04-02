.PHONY: help build format lint type typecheck test tests integration_test integration_tests

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_. -]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)


test tests: TEST_FILE ?= tests/unit_tests/
integration_test integration_tests: TEST_FILE=tests/integration_tests/

test: ## Run unit tests
test tests:
	uv run --group test pytest -vvv $(PYTEST_EXTRA) --disable-socket --allow-unix-socket $(TEST_FILE)

integration_test: ## Run integration tests
integration_test integration_tests:
	uv run --group test pytest -vvv --timeout 30 $(TEST_FILE)

build: ## Build sdist and wheel into dist/
	uv build

lint: ## Ruff (package + examples) and ty
	uv run --group test ruff check langchain_leap0 examples
	uv run --group test ruff format langchain_leap0 examples --check
	uv run --group test ty check langchain_leap0

format: ## Ruff format and fixes (package + examples)
	uv run --group test ruff format langchain_leap0 examples
	uv run --group test ruff check --fix langchain_leap0 examples

type: ## Run ty type checker
	uv run --group test ty check langchain_leap0

typecheck: type
