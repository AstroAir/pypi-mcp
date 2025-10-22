# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Model Context Protocol (MCP) server for PyPI package information and management. It provides AI models with tools to query PyPI package data, analyze dependencies, check for vulnerabilities, and manage Python package information.

## Development Commands

### Environment Setup
```bash
# Using uv (recommended)
uv sync --dev

# Using pip
pip install -e .
```

### Running the Server
```bash
# STDIO transport (for local MCP clients)
pypi-mcp
# or
python -m pypi_mcp.server

# HTTP transport
pypi-mcp --transport http --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run unit tests (default)
python run_tests.py

# Run specific test types
python run_tests.py --unit           # Unit tests only
python run_tests.py --integration    # Integration tests (real APIs)
python run_tests.py --performance    # Performance tests
python run_tests.py --all           # All tests
python run_tests.py --coverage      # All tests with coverage

# Run specific test file/function
python run_tests.py --test tests/test_server.py::test_get_package_info

# Run tests with pytest directly
uv run pytest tests/ -v
uv run pytest tests/test_server.py -v
```

### Code Quality
```bash
# Linting and formatting
uv run black pypi_mcp/
uv run isort pypi_mcp/
uv run ruff check pypi_mcp/
uv run mypy pypi_mcp/

# Run all linting checks
python run_tests.py --lint
```

### Building and Packaging
```bash
# Validate packaging configuration
python scripts/packaging_utils.py

# Build packages
uv build

# Validate built packages
python scripts/validate_package.py
```

## Architecture

### Core Components

- **`server.py`** - Main FastMCP server with all tool definitions (get_package_info, search_packages, check_vulnerabilities, etc.)
- **`client.py`** - Async PyPI API client with rate limiting and error handling
- **`models.py`** - Pydantic data models for package information
- **`config.py`** - Configuration management using pydantic-settings
- **`cache.py`** - Intelligent caching system with TTL support
- **`utils.py`** - Helper functions for validation, comparison, version parsing
- **`exceptions.py`** - Custom exceptions for different error types

### Key Patterns

1. **Async/Await**: All API operations are async for high performance
2. **Caching**: Intelligent caching with TTL to reduce API calls
3. **Rate Limiting**: Built-in rate limiting to respect PyPI API limits
4. **Error Handling**: Comprehensive error handling with custom exception types
5. **Validation**: Input validation for all API parameters
6. **Modular Design**: Clear separation of concerns between components

### Configuration

The server uses environment variables with `PYPI_MCP_` prefix:
- `PYPI_MCP_TIMEOUT` - HTTP request timeout (default: 30.0)
- `PYPI_MCP_RATE_LIMIT` - Max requests per second (default: 10.0)
- `PYPI_MCP_CACHE_TTL` - Cache TTL in seconds (default: 300)
- `PYPI_MCP_LOG_LEVEL` - Logging level (default: "INFO")
- `PYPI_MCP_ENABLE_VULNERABILITY_CHECK` - Enable vulnerability checking (default: true)

### Testing Strategy

- **Unit tests**: Fast tests with mocked dependencies
- **Integration tests**: Tests that may hit real PyPI APIs
- **Performance tests**: Tests for caching and concurrency
- **Test markers**: Use `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.performance`

### Package Structure

```
pypi_mcp/
├── __init__.py          # Package initialization and version
├── server.py            # FastMCP server with all tools/resources/prompts
├── client.py            # Async PyPI API client
├── models.py            # Pydantic data models
├── config.py            # Configuration management
├── cache.py             # Caching utilities
├── utils.py             # Helper functions
└── exceptions.py        # Custom exceptions

tests/
├── test_server.py       # Server tool tests
├── test_integration.py  # Integration tests
├── test_error_handling.py  # Error handling tests
├── test_config.py       # Configuration tests
└── test_performance.py  # Performance tests

scripts/
├── packaging_utils.py   # Packaging validation utilities
└── validate_package.py  # Built package validation
```

## Development Guidelines

1. **Always use async/await** for API operations
2. **Validate inputs** using the validation utilities in `utils.py`
3. **Handle exceptions** appropriately using the custom exception types
4. **Add tests** for new functionality following the existing test patterns
5. **Use caching** for expensive operations
6. **Follow the existing code style** (Black, isort, mypy-compliant)
7. **Update documentation** when adding new tools or changing functionality

## Common Tasks

### Adding a New Tool
1. Add the tool function in `server.py` with the `@mcp.tool` decorator
2. Follow the existing pattern for parameter validation and error handling
3. Add tests in `test_server.py`
4. Update the README.md if the tool should be listed there

### Adding New Configuration Options
1. Add the field to the `Settings` class in `config.py`
2. Update the environment variable documentation in README.md
3. Add tests for the new configuration option in `test_config.py`

### Debugging API Issues
- Use `PYPI_MCP_LOG_LEVEL=DEBUG` for detailed logging
- Check the cache status with the `get_cache_info` tool
- Monitor rate limiting with the log output
- Use integration tests to test real API calls