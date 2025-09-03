.PHONY: help install install-dev test test-unit test-integration test-coverage lint format type-check clean build docs docs-serve docker-build docker-run

# Default target
help:
	@echo "Available targets:"
	@echo "  install          Install the package"
	@echo "  install-dev      Install development dependencies"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-coverage    Run tests with coverage report"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code"
	@echo "  type-check       Run type checking"
	@echo "  clean            Clean build artifacts"
	@echo "  build            Build the package"
	@echo "  docs             Build documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run Docker container"

# Installation
install:
	uv sync

install-dev:
	uv sync --dev

# Testing
test:
	uv run pytest

test-unit:
	uv run pytest -m unit

test-integration:
	uv run pytest -m integration

test-coverage:
	uv run pytest --cov=pypi_mcp --cov-report=html --cov-report=term

# Code quality
lint:
	uv run ruff check pypi_mcp/
	uv run ruff format --check pypi_mcp/
	uv run black --check pypi_mcp/
	uv run isort --check-only pypi_mcp/

format:
	uv run black pypi_mcp/
	uv run isort pypi_mcp/
	uv run ruff format pypi_mcp/

type-check:
	uv run mypy pypi_mcp/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -f .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	uv build

# Packaging utilities
validate-package: build
	python scripts/validate_package.py

check-packaging:
	python scripts/packaging_utils.py

# Build and validate package
package: check-packaging build validate-package
	@echo "Package build and validation complete!"

# Test package installation in clean environment
test-install: build
	python scripts/validate_package.py

# Documentation
docs:
	uv run mkdocs build

docs-serve:
	uv run mkdocs serve

# Docker
docker-build:
	docker build -t pypi-mcp .

docker-run:
	docker run -p 8000:8000 pypi-mcp

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify everything works."

check: lint type-check test
	@echo "All checks passed!"
