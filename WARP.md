# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a PyPI MCP (Model Context Protocol) Server built with FastMCP that provides AI models with comprehensive tools to query PyPI package information, analyze dependencies, check vulnerabilities, and manage Python package data. The server supports both STDIO and HTTP transports for integration with various MCP clients.

## Core Commands

### Development Setup
```bash
uv sync --dev          # Install all dependencies including dev tools
make install-dev       # Alternative using Makefile
```

### Testing
```bash
# Using Makefile (recommended)
make test             # All tests
make test-unit        # Fast unit tests only
make test-integration # Integration tests (hits real APIs)
make test-coverage    # Tests with HTML coverage report

# Using uv directly
uv run pytest                           # All tests
uv run pytest -m unit                   # Unit tests only
uv run pytest -m integration            # Integration tests only
uv run pytest tests/test_server.py      # Specific test file
uv run pytest --cov=pypi_mcp --cov-report=html  # Coverage report

# Using custom test runner (advanced options)
python run_tests.py --unit              # Unit tests with detailed output
python run_tests.py --integration       # Integration tests
python run_tests.py --performance       # Performance tests
python run_tests.py --coverage          # All tests with coverage
python run_tests.py --ci                # CI pipeline (unit + lint)
python run_tests.py --test tests/test_server.py::TestSpecificFunction
pypi-mcp-test --unit                    # Using entry point script
```

### Code Quality
```bash
make lint            # Run all linting checks (ruff, black, isort)
make format          # Format code (black, isort, ruff format)
make type-check      # Run MyPy type checking
make check           # Run lint + type-check + test (full check)
```

### Running the Server
```bash
# STDIO transport (default for MCP clients)
pypi-mcp                                 # Using entry point
python -m pypi_mcp.server               # Direct module execution
python main.py                           # Using main.py wrapper

# HTTP transport for testing/debugging
pypi-mcp --transport http --host 0.0.0.0 --port 8000
pypi-mcp --transport http --port 8001 --log-level DEBUG
uv run pypi-mcp --transport http --host localhost --port 8000

# Get help
pypi-mcp --help                          # Show all available options
```

### Building and Packaging
```bash
make build                           # Build package with uv
make package                         # Full build pipeline with validation  
make check-packaging                 # Check packaging configuration
make validate-package                # Validate built packages
make test-install                    # Test installation in clean environment
python scripts/packaging_utils.py   # Package management utilities
python scripts/validate_package.py  # Detailed package validation
```

### Docker
```bash
make docker-build    # Build Docker image
make docker-run      # Run containerized server
```

## Architecture Overview

### Core Components
- **server.py**: FastMCP server with 10 MCP tools, 2 resources, and 3 prompts for PyPI operations
- **client.py**: Async PyPI API client using httpx with rate limiting, retries, and caching
- **models.py**: Pydantic data models (PackageInfo, Vulnerability, PackageFile, PyPIStats, etc.)
- **config.py**: Environment-driven configuration with validation and `PYPI_MCP_*` prefix
- **cache.py**: TTL-based caching system using cachetools with statistics
- **utils.py**: Helper functions for validation, formatting, version comparison, and requirement parsing
- **exceptions.py**: Custom exception hierarchy (PyPIMCPError, PackageNotFoundError, etc.)

### Key Design Patterns
- **Async/await throughout**: All I/O operations are async for performance
- **Context managers**: PyPI client uses async context managers for resource management
- **Caching with TTL**: Intelligent caching (300s default) to respect PyPI rate limits
- **Environment-driven config**: All settings configurable via `PYPI_MCP_*` env vars
- **Type safety**: Pydantic models and MyPy for full type checking
- **Error handling**: Custom exception hierarchy with proper error propagation

### MCP Tools Provided
The server exposes these 10 tools to AI models:
- **get_package_info** - Detailed package metadata with optional file listings
- **get_package_versions** - All available versions with pre-release filtering
- **search_packages** - Package search by name/keywords (exact match implementation)
- **compare_versions** - Side-by-side version comparison with detailed analysis
- **check_compatibility** - Python version compatibility checking
- **get_dependencies** - Dependency analysis with runtime/dev/optional categorization
- **check_vulnerabilities** - Security vulnerability scanning with CVE details
- **get_pypi_stats** - PyPI-wide statistics and top packages by size
- **get_package_health** - Package maintenance and health scoring (0-100)
- **get_cache_info** - Cache statistics and configuration details

### MCP Resources Provided
- **pypi://stats/overview** - PyPI statistics overview resource
- **pypi://package/{package_name}** - Package metadata as formatted resource

### MCP Prompts Provided
- **analyze_package** - Comprehensive package analysis prompt template
- **compare_packages** - Package comparison analysis prompt template  
- **security_review** - Security-focused review prompt template

### Transport Support
- **STDIO**: Default for MCP clients like Claude Desktop
- **HTTP**: For debugging and web-based integrations

## Environment Configuration

All configuration uses `PYPI_MCP_` prefix. Complete configuration options:

```bash
# PyPI API Settings
PYPI_MCP_PYPI_BASE_URL=https://pypi.org              # Base PyPI API URL
PYPI_MCP_PYPI_SIMPLE_URL=https://pypi.org/simple     # PyPI simple index URL
PYPI_MCP_USER_AGENT=pypi-mcp/0.1.0                   # Custom User-Agent string

# HTTP Client Settings  
PYPI_MCP_TIMEOUT=30.0                                # Request timeout in seconds
PYPI_MCP_MAX_RETRIES=3                               # Max retry attempts

# Performance Settings
PYPI_MCP_RATE_LIMIT=10.0                             # Max requests per second
PYPI_MCP_CACHE_TTL=300                               # Cache TTL in seconds
PYPI_MCP_CACHE_MAX_SIZE=1000                         # Max cache entries

# Logging Configuration
PYPI_MCP_LOG_LEVEL=INFO                              # DEBUG, INFO, WARNING, ERROR
PYPI_MCP_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Server Settings
PYPI_MCP_SERVER_NAME="PyPI MCP Server"               # Server identification
PYPI_MCP_SERVER_VERSION="0.1.0"                     # Server version

# Feature Flags
PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true             # Enable security scanning
PYPI_MCP_ENABLE_STATS=true                           # Enable PyPI statistics
PYPI_MCP_ENABLE_SEARCH=true                          # Enable package search
```

Use `.env` file (copy from `.env.example`) or export environment variables directly.

## Testing Strategy

### Test Organization
- **Unit tests**: Fast, mocked dependencies, no network calls
- **Integration tests**: Real PyPI API calls, marked with `@pytest.mark.integration`
- **Performance tests**: Caching, concurrency, rate limiting validation
- **Markers**: `unit`, `integration`, `performance`, `network`, `slow`

### Running Tests
```bash
# Fast development cycle
uv run pytest -m unit

# Full validation before PR
make check

# Debug failing tests
uv run pytest --pdb tests/test_server.py::test_specific_function
```

### Mocking Patterns
Unit tests mock `httpx.AsyncClient` or use `respx` for HTTP mocking. Avoid real network calls in unit tests to keep them fast and reliable.

## Code Style Requirements

- **Python 3.11+** with full type hints
- **Black** formatting (4-space indent)
- **isort** for import organization
- **Ruff** for linting and additional formatting
- **MyPy** for type checking with strict settings
- **Docstrings** required for all public APIs
- **Async/await** for all I/O operations

### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: prefix with `_`

## Development Workflow

### Adding New Features
1. Add tool/resource to `server.py` with proper async patterns
2. Update models in `models.py` if needed for new data structures
3. Add client methods in `client.py` with caching decorators
4. Write comprehensive tests with both unit and integration coverage
5. Update documentation and examples
6. Run full validation: `make check`

### Common Patterns
- Use `@cached(ttl=300)` decorator for cacheable API calls
- Implement proper rate limiting with `self._rate_limiter` semaphore
- Validate inputs using utility functions from `utils.py`
- Handle PyPI API errors with custom exception classes
- Use Pydantic models for all API responses for type safety

### Performance Considerations
- Respect PyPI rate limits (default 10 requests/second)
- Use caching aggressively for repeated queries
- Implement proper async patterns to avoid blocking
- Monitor cache hit rates using cache statistics tools

## Special Files and Directories

- **run_tests.py**: Custom test runner with multiple modes (unit/integration/performance/coverage)
- **scripts/**: Packaging utilities and validation scripts
  - `packaging_utils.py`: Version validation, build automation, metadata checking
  - `validate_package.py`: Built package validation and installation testing
- **examples/**: Usage examples and integration configurations
  - `basic_usage.py`: Programmatic usage examples
  - `claude_desktop_config.json`: Claude Desktop MCP configuration
- **docs/**: MkDocs documentation (run `make docs-serve` to preview)
- **.github/**: GitHub Actions CI/CD workflows and templates
- **Dockerfile**: Multi-stage build for containerized deployment
- **.env.example**: Complete configuration template
- **AGENTS.md**: Repository guidelines and development conventions
- **CONTRIBUTING.md**: Detailed contribution guidelines and setup
- **DOCUMENTATION.md**: Comprehensive project documentation

## Integration Notes

### Claude Desktop Integration
Add to Claude Desktop config (`~/Library/Application\ Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "pypi": {
      "command": "pypi-mcp",
      "args": [],
      "env": {
        "PYPI_MCP_LOG_LEVEL": "INFO",
        "PYPI_MCP_CACHE_TTL": "300"
      }
    }
  }
}
```

Example config is available in `examples/claude_desktop_config.json`.

### Common Use Cases
- Package analysis and comparison for AI assistants
- Security vulnerability assessment in development workflows
- Dependency management and compatibility checking
- PyPI ecosystem exploration and statistics

The codebase is designed for high reliability and performance when serving AI models with PyPI data, with comprehensive error handling, caching, and async patterns throughout.

<citations>
  <document>
      <document_type>WARP_DOCUMENTATION</document_type>
      <document_id>getting-started/quickstart-guide/coding-in-warp</document_id>
  </document>
</citations>
