# Repository Guidelines

This repository provides an MCP server for rich PyPI package information and tooling. Use the commands and conventions below to develop, test, and contribute effectively.

## Project Structure & Module Organization
- `pypi_mcp/`: core code
  - `server.py` (FastMCP server and tools), `client.py` (httpx async client), `models.py` (pydantic types), `cache.py`, `config.py` (env‑driven settings), `utils.py`.
- `tests/`: pytest suites (`test_*.py`) with asyncio and markers.
- `examples/`, `docs/` (MkDocs), `scripts/` (packaging helpers), `dist/` (builds).
- Configuration: `.env` (see `.env.example`), env prefix `PYPI_MCP_`.

## Build, Test, and Development Commands
- `make install-dev` — set up dev environment via `uv`.
- `make test` / `make test-unit` / `make test-integration` / `make test-coverage` — run tests; coverage HTML in `htmlcov/`.
- `make lint` / `make format` / `make type-check` — ruff, black, isort, mypy.
- `make build` — build package with `uv`; `make docs-serve` — serve docs locally.
- Run server: `uv run pypi-mcp --transport http --host 0.0.0.0 --port 8000` (or `--transport stdio`). Docker: `make docker-build && make docker-run`.

## Coding Style & Naming Conventions
- Python 3.11+, 4‑space indent, type hints required. Keep functions small and side‑effect light.
- Names: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- Format with Black; sort imports with isort; keep Ruff clean; run MyPy before pushing. Add docstrings for public APIs.

## Testing Guidelines
- Place tests in `tests/test_*.py`; use `@pytest.mark.asyncio` for async tests.
- Avoid real network in unit tests; mock `httpx.AsyncClient` or use `respx`.
- Use markers: `-m unit` or `-m integration`; avoid `-m network` on CI. Add tests for new features and bug fixes; aim for meaningful coverage.

## Commit & Pull Request Guidelines
- Commits: imperative, concise subject (e.g., "Add cache stats API"); include rationale in body if needed.
- Before PR: run `make check`. PRs should include a clear description, linked issues, test evidence (logs/screenshots for CLI), and docs updates for user‑facing changes. Keep changes focused.

## Security & Configuration Tips
- Do not commit secrets. Configure via `PYPI_MCP_*` or `.env`.
- Respect rate limits and caching; prefer unit tests without network access.

