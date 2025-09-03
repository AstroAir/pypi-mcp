# Development Setup

Complete guide for setting up a development environment for the PyPI MCP Server.

## Prerequisites

Before starting development, ensure you have:

- **Python 3.11+**: Required for the project
- **Git**: For version control
- **uv** (recommended) or **pip**: For package management
- **Code Editor**: VS Code, PyCharm, or your preferred editor

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
```

### 2. Set Up Python Environment

=== "Using uv (Recommended)"

    ```bash
    # Install uv if not already installed
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Create and activate virtual environment with dependencies
    uv sync --dev

    # Activate the environment
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

=== "Using pip"

    ```bash
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install development dependencies
    pip install -e ".[dev]"
    ```

### 3. Verify Installation

```bash
# Check that the package is installed
pypi-mcp --help

# Run tests to verify everything works
pytest

# Check code quality tools
black --check pypi_mcp/
isort --check-only pypi_mcp/
mypy pypi_mcp/
ruff check pypi_mcp/
```

## Development Dependencies

The development environment includes:

### Core Dependencies

- **fastmcp** (>=2.12.0) - MCP framework
- **httpx** (>=0.27.0) - Async HTTP client
- **packaging** (>=23.0) - Python package version handling
- **cachetools** (>=5.3.0) - Caching utilities
- **pydantic** (>=2.0.0) - Data validation and serialization

### Development Tools

- **pytest** (>=7.0.0) - Testing framework
- **pytest-asyncio** (>=0.21.0) - Async testing support
- **pytest-httpx** (>=0.21.0) - HTTP testing utilities
- **pytest-mock** (>=3.10.0) - Mocking utilities
- **pytest-cov** (>=4.0.0) - Coverage reporting
- **respx** (>=0.20.0) - HTTP request mocking

### Code Quality Tools

- **black** (>=23.0.0) - Code formatting
- **isort** (>=5.12.0) - Import sorting
- **mypy** (>=1.0.0) - Type checking
- **ruff** (>=0.1.0) - Fast Python linter

## Project Structure

```
pypi-mcp/
├── pypi_mcp/              # Main package
│   ├── __init__.py        # Package initialization
│   ├── server.py          # FastMCP server with tools
│   ├── client.py          # PyPI API client
│   ├── models.py          # Pydantic data models
│   ├── config.py          # Configuration management
│   ├── cache.py           # Caching utilities
│   ├── utils.py           # Helper functions
│   └── exceptions.py      # Custom exceptions
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_server.py     # Server tests
│   ├── test_client.py     # Client tests
│   ├── test_config.py     # Configuration tests
│   ├── test_integration.py # Integration tests
│   ├── test_performance.py # Performance tests
│   └── conftest.py        # Pytest configuration
├── examples/              # Usage examples
│   ├── basic_usage.py     # Basic usage demonstration
│   └── claude_desktop_config.json # Claude Desktop config
├── docs/                  # Documentation (MkDocs)
├── pyproject.toml         # Project configuration
├── README.md              # Project README
├── LICENSE                # MIT License
└── .gitignore            # Git ignore rules
```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 2. Make Changes

Edit the code following the project conventions:

- **Code Style**: Follow PEP 8 and use black for formatting
- **Type Hints**: Add type hints to all functions and methods
- **Docstrings**: Write docstrings for all public functions and classes
- **Tests**: Write tests for new functionality

### 3. Run Quality Checks

```bash
# Format code
black pypi_mcp/ tests/
isort pypi_mcp/ tests/

# Type checking
mypy pypi_mcp/

# Linting
ruff check pypi_mcp/ tests/

# Run tests
pytest

# Run tests with coverage
pytest --cov=pypi_mcp --cov-report=html
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new package health assessment tool"

# Or for bug fixes
git commit -m "fix: handle rate limiting in PyPI client"
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_server.py

# Run specific test
pytest tests/test_server.py::test_get_package_info

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=pypi_mcp --cov-report=html
```

### Test Categories

The project uses pytest markers to categorize tests:

```bash
# Run only unit tests (fast, no external dependencies)
pytest -m unit

# Run only integration tests (may hit real APIs)
pytest -m integration

# Run only performance tests
pytest -m performance

# Run tests that require network access
pytest -m network

# Skip slow tests
pytest -m "not slow"
```

### Writing Tests

#### Unit Test Example

```python
import pytest
from unittest.mock import AsyncMock, patch
from pypi_mcp.server import create_server

@pytest.mark.unit
async def test_get_package_info():
    """Test get_package_info tool."""
    server = create_server()

    with patch('pypi_mcp.client.client') as mock_client:
        mock_client.get_package_info = AsyncMock(return_value=mock_package_info)

        result = await server.call_tool("get_package_info", {
            "package_name": "requests"
        })

        assert result["name"] == "requests"
        mock_client.get_package_info.assert_called_once_with("requests", None)
```

#### Integration Test Example

```python
import pytest
from pypi_mcp.client import client

@pytest.mark.integration
@pytest.mark.network
async def test_real_package_info():
    """Test getting real package info from PyPI."""
    async with client:
        package_info = await client.get_package_info("requests")

        assert package_info.name == "requests"
        assert package_info.version is not None
        assert len(package_info.requires_dist) > 0
```

### Test Configuration

The project uses `pytest.ini` configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "--verbose",
    "--tb=short",
    "--strict-markers",
    "--strict-config",
    "--disable-warnings",
    "--color=yes",
    "--durations=10"
]
markers = [
    "unit: Unit tests (fast, no external dependencies)",
    "integration: Integration tests (may hit real APIs)",
    "performance: Performance and load tests",
    "slow: Slow tests that take more than a few seconds",
    "network: Tests that require network access"
]
```

## Code Quality

### Formatting with Black

```bash
# Format all code
black pypi_mcp/ tests/

# Check formatting without making changes
black --check pypi_mcp/ tests/

# Format specific file
black pypi_mcp/server.py
```

### Import Sorting with isort

```bash
# Sort imports
isort pypi_mcp/ tests/

# Check import sorting
isort --check-only pypi_mcp/ tests/

# Show diff without making changes
isort --diff pypi_mcp/ tests/
```

### Type Checking with mypy

```bash
# Type check all code
mypy pypi_mcp/

# Type check specific file
mypy pypi_mcp/server.py

# Type check with verbose output
mypy --verbose pypi_mcp/
```

### Linting with Ruff

```bash
# Lint all code
ruff check pypi_mcp/ tests/

# Fix auto-fixable issues
ruff check --fix pypi_mcp/ tests/

# Show all issues including fixed ones
ruff check --show-fixes pypi_mcp/ tests/
```

## Debugging

### Local Development Server

```bash
# Run server with debug logging
pypi-mcp --log-level DEBUG

# Run HTTP server for testing
pypi-mcp --transport http --log-level DEBUG

# Test with specific configuration
PYPI_MCP_CACHE_TTL=60 pypi-mcp --log-level DEBUG
```

### Debug Configuration

Create a `.env` file for development:

```env
# Development configuration
PYPI_MCP_LOG_LEVEL=DEBUG
PYPI_MCP_CACHE_TTL=60
PYPI_MCP_RATE_LIMIT=5.0
PYPI_MCP_TIMEOUT=30.0
```

### VS Code Configuration

Create `.vscode/launch.json` for debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug PyPI MCP Server",
      "type": "python",
      "request": "launch",
      "module": "pypi_mcp.server",
      "args": ["--log-level", "DEBUG"],
      "console": "integratedTerminal",
      "env": {
        "PYPI_MCP_LOG_LEVEL": "DEBUG"
      }
    },
    {
      "name": "Debug Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v", "tests/"],
      "console": "integratedTerminal"
    }
  ]
}
```

## Performance Profiling

### Basic Profiling

```python
import asyncio
import cProfile
from pypi_mcp.client import client

async def profile_package_info():
    """Profile package info retrieval."""
    async with client:
        await client.get_package_info("requests")

# Run with profiling
cProfile.run('asyncio.run(profile_package_info())')
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler examples/basic_usage.py
```

### Load Testing

```python
import asyncio
import time
from pypi_mcp.client import client

async def load_test():
    """Simple load test."""
    start_time = time.time()

    async with client:
        tasks = []
        for i in range(100):
            task = client.get_package_info("requests")
            tasks.append(task)

        await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Completed 100 requests in {end_time - start_time:.2f} seconds")

asyncio.run(load_test())
```

## Documentation

### Building Documentation

```bash
# Install MkDocs and dependencies
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Writing Documentation

- Use Markdown format
- Follow MkDocs conventions
- Include code examples
- Add cross-references
- Update navigation in `mkdocs.yml`

## Next Steps

- [Architecture Guide](architecture.md) - Understand the system architecture
- [Contributing Guidelines](contributing.md) - Learn how to contribute
- [Testing Guide](testing.md) - Comprehensive testing information
- [Release Process](release-process.md) - How releases are made
