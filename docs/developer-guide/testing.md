# Testing Guide

Comprehensive guide to testing the PyPI MCP Server, including test structure, best practices, and testing strategies.

## Testing Philosophy

The PyPI MCP Server follows a comprehensive testing strategy:

- **Fast Feedback**: Unit tests provide immediate feedback
- **Confidence**: Integration tests ensure real-world functionality
- **Performance**: Performance tests validate scalability
- **Quality**: High test coverage ensures code quality

## Test Structure

### Directory Organization

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_server.py           # Server and tool tests
├── test_client.py           # PyPI client tests
├── test_config.py           # Configuration tests
├── test_models.py           # Data model tests
├── test_utils.py            # Utility function tests
├── test_cache.py            # Cache functionality tests
├── test_integration.py      # Integration tests
├── test_performance.py      # Performance tests
├── test_error_handling.py   # Error handling tests
└── fixtures/                # Test data and fixtures
    ├── package_data.json
    ├── vulnerability_data.json
    └── stats_data.json
```

### Test Categories

We use pytest markers to categorize tests:

| Marker        | Description                    | Speed     | Dependencies  |
| ------------- | ------------------------------ | --------- | ------------- |
| `unit`        | Fast, isolated tests           | Very Fast | None          |
| `integration` | Tests with real APIs           | Slow      | Network, PyPI |
| `performance` | Load and performance tests     | Variable  | Network       |
| `network`     | Tests requiring network access | Slow      | Internet      |
| `slow`        | Tests taking >5 seconds        | Slow      | Variable      |

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_server.py

# Run specific test
pytest tests/test_server.py::test_get_package_info

# Run specific test class
pytest tests/test_server.py::TestPackageTools
```

### Test Categories

```bash
# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration

# Run performance tests
pytest -m performance

# Run tests that require network
pytest -m network

# Skip slow tests
pytest -m "not slow"

# Run unit and integration tests
pytest -m "unit or integration"
```

### Coverage Testing

```bash
# Run tests with coverage
pytest --cov=pypi_mcp

# Generate HTML coverage report
pytest --cov=pypi_mcp --cov-report=html

# Generate XML coverage report (for CI)
pytest --cov=pypi_mcp --cov-report=xml

# Fail if coverage below threshold
pytest --cov=pypi_mcp --cov-fail-under=90
```

### Parallel Testing

```bash
# Install pytest-xdist for parallel execution
pip install pytest-xdist

# Run tests in parallel
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

## Writing Tests

### Unit Tests

Unit tests are fast, isolated tests that don't depend on external services:

```python
import pytest
from unittest.mock import AsyncMock, patch
from pypi_mcp.server import create_server
from pypi_mcp.models import PackageInfo

@pytest.mark.unit
async def test_get_package_info_success():
    """Test successful package info retrieval."""
    # Arrange
    server = create_server()
    mock_package_info = PackageInfo(
        name="requests",
        version="2.31.0",
        summary="Python HTTP for Humans.",
        # ... other required fields
    )

    # Act & Assert
    with patch('pypi_mcp.client.client') as mock_client:
        mock_client.get_package_info = AsyncMock(return_value=mock_package_info)

        result = await server.call_tool("get_package_info", {
            "package_name": "requests"
        })

        assert result["name"] == "requests"
        assert result["version"] == "2.31.0"
        mock_client.get_package_info.assert_called_once_with("requests", None)

@pytest.mark.unit
def test_validate_package_name():
    """Test package name validation."""
    from pypi_mcp.utils import validate_package_name

    # Valid names
    assert validate_package_name("requests") is True
    assert validate_package_name("django-rest-framework") is True
    assert validate_package_name("scikit-learn") is True

    # Invalid names
    assert validate_package_name("") is False
    assert validate_package_name("-invalid") is False
    assert validate_package_name("invalid-") is False
```

### Integration Tests

Integration tests verify functionality with real external services:

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
        assert package_info.summary is not None

@pytest.mark.integration
@pytest.mark.network
async def test_package_not_found():
    """Test handling of non-existent packages."""
    from pypi_mcp.exceptions import PackageNotFoundError

    async with client:
        with pytest.raises(PackageNotFoundError):
            await client.get_package_info("this-package-definitely-does-not-exist-12345")
```

### Performance Tests

Performance tests validate system performance under load:

```python
import pytest
import asyncio
import time
from pypi_mcp.client import client

@pytest.mark.performance
@pytest.mark.network
async def test_concurrent_requests():
    """Test handling of concurrent requests."""
    async with client:
        start_time = time.time()

        # Create 10 concurrent requests
        tasks = []
        for _ in range(10):
            task = client.get_package_info("requests")
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        end_time = time.time()
        duration = end_time - start_time

        # All requests should succeed
        assert len(results) == 10
        assert all(result.name == "requests" for result in results)

        # Should complete within reasonable time (adjust based on expectations)
        assert duration < 10.0  # 10 seconds for 10 requests

@pytest.mark.performance
async def test_cache_performance():
    """Test cache performance."""
    from pypi_mcp.cache import get_cache_stats

    # Warm up cache
    async with client:
        await client.get_package_info("requests")

        # Measure cache hit performance
        start_time = time.time()
        for _ in range(100):
            await client.get_package_info("requests")
        end_time = time.time()

        duration = end_time - start_time

        # Cache hits should be very fast
        assert duration < 1.0  # 100 cache hits in under 1 second

        # Check cache statistics
        stats = await get_cache_stats()
        assert stats['hit_rate'] > 0.9  # >90% hit rate
```

### Error Handling Tests

Test error conditions and edge cases:

```python
import pytest
from pypi_mcp.exceptions import ValidationError, PyPIMCPError

@pytest.mark.unit
async def test_invalid_package_name():
    """Test handling of invalid package names."""
    server = create_server()

    with pytest.raises(ValidationError) as exc_info:
        await server.call_tool("get_package_info", {
            "package_name": ""  # Empty name
        })

    assert "Invalid package name" in str(exc_info.value)

@pytest.mark.unit
async def test_network_timeout():
    """Test handling of network timeouts."""
    import httpx

    with patch('pypi_mcp.client.httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.TimeoutException("Timeout")

        async with client:
            with pytest.raises(PyPIMCPError) as exc_info:
                await client.get_package_info("requests")

            assert "timeout" in str(exc_info.value).lower()
```

## Test Fixtures

### Pytest Fixtures

Common fixtures for test data and setup:

```python
# conftest.py
import pytest
from unittest.mock import AsyncMock
from pypi_mcp.models import PackageInfo, PackageFile, Vulnerability

@pytest.fixture
def mock_package_info():
    """Mock package info for testing."""
    return PackageInfo(
        name="test-package",
        version="1.0.0",
        summary="A test package",
        description="This is a test package for unit testing",
        author="Test Author",
        author_email="test@example.com",
        license="MIT",
        home_page="https://example.com",
        package_url="https://pypi.org/project/test-package/",
        project_url="https://pypi.org/project/test-package/",
        release_url="https://pypi.org/project/test-package/1.0.0/",
        requires_dist=["requests>=2.25.0"],
        provides_extra=["dev"],
        classifiers=["Programming Language :: Python :: 3"],
        keywords="test,package",
        requires_python=">=3.8",
        files=[],
        vulnerabilities=[]
    )

@pytest.fixture
def mock_vulnerability():
    """Mock vulnerability for testing."""
    return Vulnerability(
        id="GHSA-test-1234",
        source="GitHub Advisory Database",
        summary="Test vulnerability",
        details="This is a test vulnerability",
        aliases=["CVE-2023-12345"],
        fixed_in=["1.0.1", "1.1.0"],
        link="https://github.com/advisories/GHSA-test-1234"
    )

@pytest.fixture
async def mock_client():
    """Mock PyPI client for testing."""
    client = AsyncMock()
    client.get_package_info = AsyncMock()
    client.get_package_versions = AsyncMock()
    client.get_pypi_stats = AsyncMock()
    return client
```

### Test Data Files

Store complex test data in JSON files:

```json
// fixtures/package_data.json
{
  "requests": {
    "name": "requests",
    "version": "2.31.0",
    "summary": "Python HTTP for Humans.",
    "description": "Requests is a simple, yet elegant HTTP library.",
    "author": "Kenneth Reitz",
    "license": "Apache 2.0",
    "requires_dist": ["urllib3>=1.21.1,<3", "certifi>=2017.4.17"]
  }
}
```

Load test data in fixtures:

```python
import json
from pathlib import Path

@pytest.fixture
def package_test_data():
    """Load package test data from JSON file."""
    test_data_path = Path(__file__).parent / "fixtures" / "package_data.json"
    with open(test_data_path) as f:
        return json.load(f)
```

## Mocking Strategies

### HTTP Request Mocking

Use `respx` for HTTP request mocking:

```python
import respx
import httpx

@pytest.mark.unit
@respx.mock
async def test_pypi_api_call():
    """Test PyPI API call with mocked response."""
    # Mock the PyPI API response
    respx.get("https://pypi.org/pypi/requests/json").mock(
        return_value=httpx.Response(200, json={
            "info": {
                "name": "requests",
                "version": "2.31.0",
                "summary": "Python HTTP for Humans."
            }
        })
    )

    async with client:
        package_info = await client.get_package_info("requests")
        assert package_info.name == "requests"
```

### Async Function Mocking

Use `AsyncMock` for async function mocking:

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.unit
async def test_cached_response():
    """Test cached response handling."""
    with patch('pypi_mcp.cache.cache.get') as mock_get:
        mock_get.return_value = {"name": "requests", "version": "2.31.0"}

        result = await get_cached_package_info("requests")
        assert result["name"] == "requests"
        mock_get.assert_called_once()
```

## Test Configuration

### Pytest Configuration

Configure pytest in `pyproject.toml`:

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
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::PendingDeprecationWarning"
]
```

### Environment Variables for Testing

Set test-specific environment variables:

```python
import os
import pytest

@pytest.fixture(autouse=True)
def test_environment():
    """Set up test environment variables."""
    os.environ["PYPI_MCP_CACHE_TTL"] = "60"
    os.environ["PYPI_MCP_LOG_LEVEL"] = "DEBUG"
    os.environ["PYPI_MCP_RATE_LIMIT"] = "100.0"  # Higher limit for tests
    yield
    # Cleanup if needed
```

## Continuous Integration

### GitHub Actions Configuration

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run unit tests
        run: pytest -m unit --cov=pypi_mcp

      - name: Run integration tests
        run: pytest -m integration
        env:
          PYPI_MCP_TIMEOUT: 60.0

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Test Reporting

Generate test reports for CI:

```bash
# JUnit XML for CI systems
pytest --junitxml=test-results.xml

# Coverage XML for coverage services
pytest --cov=pypi_mcp --cov-report=xml

# HTML reports for local viewing
pytest --cov=pypi_mcp --cov-report=html
```

## Best Practices

### 1. Test Naming

Use descriptive test names:

```python
# Good
def test_get_package_info_returns_correct_data_for_valid_package():
    """Test that get_package_info returns correct data for valid package."""

# Bad
def test_package_info():
    """Test package info."""
```

### 2. Test Structure

Follow the Arrange-Act-Assert pattern:

```python
async def test_package_validation():
    # Arrange
    package_name = "invalid-package-name-"

    # Act
    result = validate_package_name(package_name)

    # Assert
    assert result is False
```

### 3. Test Independence

Ensure tests are independent and can run in any order:

```python
# Good - each test sets up its own data
@pytest.fixture
def clean_cache():
    """Provide a clean cache for each test."""
    cache = TTLCache(maxsize=100, ttl=300)
    yield cache
    cache.clear()

# Bad - tests depend on shared state
global_cache = {}

def test_cache_set():
    global_cache["key"] = "value"

def test_cache_get():
    assert global_cache["key"] == "value"  # Depends on previous test
```

### 4. Error Testing

Test both success and failure cases:

```python
async def test_get_package_info_success():
    """Test successful package retrieval."""
    # Test success case

async def test_get_package_info_not_found():
    """Test package not found error."""
    # Test error case

async def test_get_package_info_network_error():
    """Test network error handling."""
    # Test network failure
```

## Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with pdb debugger
pytest --pdb

# Run with pdb on failures only
pytest --pdb-trace

# Run single test with debugging
pytest -s tests/test_server.py::test_specific_function
```

### Test Debugging Tips

1. **Use print statements** for quick debugging
2. **Use pytest fixtures** to set up debug data
3. **Run tests in isolation** to identify issues
4. **Check test logs** for detailed information
5. **Use IDE debugging** for complex issues

## Next Steps

- [Development Setup](development-setup.md) - Set up your development environment
- [Contributing Guidelines](contributing.md) - Learn how to contribute
- [Architecture Guide](architecture.md) - Understand the system architecture
