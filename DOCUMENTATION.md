# PyPI MCP Server - Comprehensive Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation Instructions](#installation-instructions)
3. [Configuration](#configuration)
4. [API Reference](#api-reference)
5. [Usage Examples](#usage-examples)
6. [Development Setup](#development-setup)
7. [Troubleshooting](#troubleshooting)

## Project Overview

PyPI MCP Server is a comprehensive Model Context Protocol (MCP) server that provides AI models with powerful tools to query PyPI package information and management. Built with FastMCP, it offers async/await support, intelligent caching, and comprehensive package analysis capabilities.

### What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI models to external data sources and tools. This server acts as a bridge between AI models (like Claude) and the Python Package Index (PyPI), enabling AI assistants to:

- Search and analyze Python packages
- Check for security vulnerabilities
- Analyze dependencies and compatibility
- Compare package versions
- Assess package health and maintenance status

### Key Features

- **🔍 Package Discovery**: Search packages by name or keywords with intelligent matching
- **📊 Dependency Analysis**: Comprehensive dependency tree analysis with environment markers
- **🔒 Security Scanning**: Real-time vulnerability checking with CVE integration
- **📈 Statistics & Analytics**: PyPI-wide statistics and package metrics
- **⚡ High Performance**: Async/await architecture with intelligent caching (TTL-based)
- **🛠️ Multiple Transports**: Support for both STDIO and HTTP transports
- **📝 Rich Metadata**: Detailed package information including files, classifiers, and project URLs

### Architecture

The server is built using modern Python technologies:

- **FastMCP**: Modern MCP framework providing the server foundation
- **httpx**: Async HTTP client for PyPI API interactions
- **Pydantic**: Data validation and serialization with type safety
- **packaging**: Python package version handling and requirement parsing
- **cachetools**: Intelligent caching system with TTL support

### Core Components

```
pypi_mcp/
├── server.py      # Main FastMCP server with tool definitions
├── client.py      # PyPI API client with async support
├── models.py      # Pydantic data models for type safety
├── config.py      # Configuration management with environment variables
├── cache.py       # Caching utilities and statistics
├── utils.py       # Helper functions for validation and formatting
└── exceptions.py  # Custom exception classes
```

## Installation Instructions

### Prerequisites

- Python 3.11 or higher
- Internet connection for PyPI API access

### Method 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is the fastest Python package manager and is recommended for this project:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install the project
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
uv sync
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp

# Install in development mode
pip install -e .

# Or install from PyPI (when available)
pip install pypi-mcp
```

### Method 3: From Source

```bash
# Clone and install dependencies manually
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastmcp>=2.12.0 httpx>=0.27.0 packaging>=23.0 cachetools>=5.3.0 pydantic>=2.0.0

# Install the package
pip install -e .
```

### Verification

Verify the installation by running:

```bash
pypi-mcp --help
```

You should see the command-line options for the PyPI MCP server.

## Configuration

The PyPI MCP server can be configured using environment variables, command-line arguments, or a `.env` file.

### Environment Variables

All configuration options use the `PYPI_MCP_` prefix:

#### PyPI API Settings

```bash
# Base URL for PyPI API (default: https://pypi.org)
export PYPI_MCP_PYPI_BASE_URL="https://pypi.org"

# PyPI simple index URL (default: https://pypi.org/simple)
export PYPI_MCP_PYPI_SIMPLE_URL="https://pypi.org/simple"

# User-Agent header for HTTP requests
export PYPI_MCP_USER_AGENT="pypi-mcp/0.1.0 (https://github.com/AstroAir/pypi-mcp)"
```

#### Performance Settings

```bash
# HTTP request timeout in seconds (default: 30.0)
export PYPI_MCP_TIMEOUT=30.0

# Maximum number of retries for failed requests (default: 3)
export PYPI_MCP_MAX_RETRIES=3

# Rate limiting: maximum requests per second (default: 10.0)
export PYPI_MCP_RATE_LIMIT=10.0

# Cache TTL in seconds (default: 300)
export PYPI_MCP_CACHE_TTL=300

# Maximum number of items in cache (default: 1000)
export PYPI_MCP_CACHE_MAX_SIZE=1000
```

#### Logging Configuration

```bash
# Logging level (default: INFO)
export PYPI_MCP_LOG_LEVEL="INFO"

# Log format string
export PYPI_MCP_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

#### Feature Flags

```bash
# Enable vulnerability checking (default: true)
export PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true

# Enable statistics endpoints (default: true)
export PYPI_MCP_ENABLE_STATS=true

# Enable package search functionality (default: true)
export PYPI_MCP_ENABLE_SEARCH=true
```

#### Server Settings

```bash
# Server name for identification (default: "PyPI MCP Server")
export PYPI_MCP_SERVER_NAME="PyPI MCP Server"

# Server version (default: "0.1.0")
export PYPI_MCP_SERVER_VERSION="0.1.0"
```

### Configuration File

Create a `.env` file in the project root:

```env
# .env file example
PYPI_MCP_LOG_LEVEL=DEBUG
PYPI_MCP_CACHE_TTL=600
PYPI_MCP_RATE_LIMIT=5.0
PYPI_MCP_TIMEOUT=60.0
```

### Command-Line Arguments

The server supports several command-line options:

```bash
# Run with STDIO transport (default)
pypi-mcp

# Run with HTTP transport
pypi-mcp --transport http --host 0.0.0.0 --port 8000

# Set log level
pypi-mcp --log-level DEBUG

# Full options
pypi-mcp --transport http --host localhost --port 8080 --log-level INFO
```

Available command-line options:
- `--transport`: Transport protocol (`stdio` or `http`, default: `stdio`)
- `--host`: Host to bind to for HTTP transport (default: `localhost`)
- `--port`: Port to bind to for HTTP transport (default: `8000`)
- `--log-level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, default: `INFO`)

## API Reference

The PyPI MCP server provides 10 tools, 2 resources, and 3 prompts for comprehensive PyPI package management.

### Tools

#### 1. get_package_info

Get detailed information about a PyPI package.

**Parameters:**
- `package_name` (str, required): Name of the package to look up
- `version` (str, optional): Specific version to get info for (latest if not specified)
- `include_files` (bool, optional): Whether to include file information in the response (default: false)

**Returns:**
```json
{
  "name": "requests",
  "version": "2.31.0",
  "summary": "Python HTTP for Humans.",
  "description": "Requests is a simple, yet elegant HTTP library...",
  "author": "Kenneth Reitz",
  "author_email": "me@kennethreitz.org",
  "license": "Apache 2.0",
  "home_page": "https://requests.readthedocs.io",
  "project_urls": {
    "Homepage": "https://requests.readthedocs.io",
    "Repository": "https://github.com/psf/requests"
  },
  "classifiers": ["Development Status :: 5 - Production/Stable", ...],
  "keywords": ["http", "requests", "web"],
  "requires_python": ">=3.7",
  "dependencies": [
    {
      "name": "urllib3",
      "version_spec": ">=1.21.1,<3",
      "extras": [],
      "environment_marker": null
    }
  ],
  "extras": ["security", "socks"],
  "yanked": false,
  "package_url": "https://pypi.org/project/requests/",
  "version_type": "stable",
  "vulnerabilities": []
}
```

**Example Usage:**
```python
# Get latest version info
result = await get_package_info("requests")

# Get specific version with files
result = await get_package_info("django", "4.2.0", include_files=True)
```

#### 2. get_package_versions

Get all available versions of a package.

**Parameters:**
- `package_name` (str, required): Name of the package
- `limit` (int, optional): Maximum number of versions to return (all if not specified)
- `include_prereleases` (bool, optional): Whether to include pre-release versions (default: true)

**Returns:**
```json
{
  "package_name": "django",
  "total_versions": 150,
  "returned_versions": 10,
  "latest_version": "4.2.7",
  "versions": [
    {
      "version": "4.2.7",
      "type": "stable",
      "is_latest": true
    },
    {
      "version": "4.2.6",
      "type": "stable",
      "is_latest": false
    }
  ]
}
```

#### 3. search_packages

Search for packages by name or keywords.

**Parameters:**
- `query` (str, required): Search query (package name or keywords)
- `limit` (int, optional): Maximum number of results to return (default: 10, max: 100)
- `include_description` (bool, optional): Whether to include package descriptions (default: false)

**Returns:**
```json
{
  "query": "web framework",
  "total_results": 1,
  "results": [
    {
      "name": "django",
      "version": "4.2.7",
      "summary": "A high-level Python Web framework",
      "description": "Django is a high-level Python Web framework...",
      "author": "Django Software Foundation",
      "keywords": ["web", "framework", "django"],
      "score": 1.0
    }
  ]
}
```

#### 4. compare_versions

Compare two versions of a package.

**Parameters:**
- `package_name` (str, required): Name of the package
- `version1` (str, required): First version to compare
- `version2` (str, required): Second version to compare

**Returns:**
```json
{
  "package_name": "requests",
  "version1": {
    "version": "2.30.0",
    "type": "stable",
    "upload_time": "2023-05-22T16:49:05",
    "dependencies_count": 5,
    "vulnerabilities_count": 0
  },
  "version2": {
    "version": "2.31.0",
    "type": "stable",
    "upload_time": "2023-07-27T15:06:07",
    "dependencies_count": 5,
    "vulnerabilities_count": 0
  },
  "comparison": {
    "result": -1,
    "newer_version": "2.31.0",
    "is_upgrade": false,
    "is_downgrade": true
  }
}
```

#### 5. check_compatibility

Check Python version compatibility for a package.

**Parameters:**
- `package_name` (str, required): Name of the package
- `version` (str, optional): Package version (latest if not specified)
- `python_version` (str, optional): Python version to check compatibility against (default: "3.11")

**Returns:**
```json
{
  "package_name": "requests",
  "package_version": "2.31.0",
  "python_version": "3.11",
  "is_compatible": true,
  "requires_python": ">=3.7",
  "compatibility_notes": [],
  "classifiers": [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11"
  ]
}
```

#### 6. get_dependencies

Get package dependencies with detailed analysis.

**Parameters:**
- `package_name` (str, required): Name of the package
- `version` (str, optional): Package version (latest if not specified)
- `include_extras` (bool, optional): Whether to include optional dependencies (default: false)

**Returns:**
```json
{
  "package_name": "fastapi",
  "package_version": "0.104.1",
  "total_dependencies": 3,
  "runtime_dependencies": [
    {
      "name": "starlette",
      "version_spec": ">=0.27.0,<0.28.0",
      "extras": [],
      "environment_marker": null
    }
  ],
  "development_dependencies": [],
  "available_extras": ["all", "dev", "doc", "test"],
  "optional_dependencies": {
    "all": [
      {
        "name": "email-validator",
        "version_spec": ">=2.0.0",
        "extras": [],
        "environment_marker": "extra == \"all\""
      }
    ]
  }
}
```

#### 7. check_vulnerabilities

Check for known security vulnerabilities in a package.

**Parameters:**
- `package_name` (str, required): Name of the package
- `version` (str, optional): Package version (latest if not specified)

**Returns:**
```json
{
  "package_name": "django",
  "package_version": "2.0.0",
  "vulnerability_count": 2,
  "has_vulnerabilities": true,
  "vulnerabilities": [
    {
      "id": "GHSA-2hrw-hx67-34x6",
      "source": "GitHub Advisory Database",
      "summary": "Django vulnerable to potential denial of service",
      "details": "An issue was discovered in Django...",
      "aliases": ["CVE-2023-31047"],
      "fixed_in": ["2.2.28", "3.2.19", "4.1.9", "4.2.1"],
      "link": "https://github.com/advisories/GHSA-2hrw-hx67-34x6",
      "withdrawn": null,
      "severity": "high"
    }
  ],
  "security_status": "vulnerable",
  "recommendation": "Update to a patched version"
}
```

#### 8. get_pypi_stats

Get overall PyPI statistics and top packages.

**Parameters:** None

**Returns:**
```json
{
  "total_packages_size": 15728640000,
  "total_size_formatted": "14.6 GB",
  "top_packages_count": 20,
  "top_packages": [
    {
      "name": "tensorflow",
      "size": 524288000,
      "size_formatted": "500.0 MB"
    }
  ],
  "last_updated": "real-time"
}
```

#### 9. get_package_health

Assess package health and maintenance status.

**Parameters:**
- `package_name` (str, required): Name of the package
- `version` (str, optional): Package version (latest if not specified)

**Returns:**
```json
{
  "package_name": "requests",
  "package_version": "2.31.0",
  "health_score": 100,
  "health_status": "excellent",
  "health_notes": [],
  "total_versions": 150,
  "is_latest": true,
  "has_vulnerabilities": false,
  "is_yanked": false,
  "version_type": "stable"
}
```

#### 10. get_cache_info

Get information about the server's cache status.

**Parameters:** None

**Returns:**
```json
{
  "cache_stats": {
    "hits": 150,
    "misses": 25,
    "hit_rate": 0.857,
    "current_size": 45,
    "max_size": 1000
  },
  "cache_enabled": true,
  "cache_ttl_seconds": 300
}
```

### Resources

Resources provide static or dynamic content that can be accessed by MCP clients.

#### 1. pypi://stats/overview

Provides PyPI statistics overview as a text resource.

**URI:** `pypi://stats/overview`

**Returns:** Plain text with PyPI statistics including total package size and top packages count.

#### 2. pypi://package/{package_name}

Provides package metadata as a text resource.

**URI:** `pypi://package/{package_name}` (e.g., `pypi://package/requests`)

**Returns:** Plain text with basic package information including name, version, summary, author, license, homepage, dependencies count, and vulnerabilities count.

### Prompts

Prompts provide structured templates for AI analysis tasks.

#### 1. analyze_package

Generate a comprehensive package analysis prompt.

**Parameters:**
- `package_name` (str, required): Name of the package to analyze
- `version` (str, optional): Specific version to analyze

**Returns:** A structured prompt asking the AI to analyze the package considering purpose, maintenance status, security, dependencies, compatibility, documentation, alternatives, and recommendations.

#### 2. compare_packages

Generate a package comparison prompt.

**Parameters:**
- `package1` (str, required): First package to compare
- `package2` (str, required): Second package to compare

**Returns:** A structured prompt asking the AI to compare packages across functionality, performance, community adoption, maintenance, security, documentation, dependencies, ease of use, licensing, and use case recommendations.

#### 3. security_review

Generate a security review prompt for a package.

**Parameters:**
- `package_name` (str, required): Name of the package to review

**Returns:** A structured prompt asking the AI to conduct a security review focusing on vulnerabilities, dependency security, package integrity, maintenance status, security best practices, trust indicators, potential risks, and secure usage recommendations.

## Usage Examples

### Basic Package Information

```python
# Get information about a popular package
result = await get_package_info("requests")
print(f"Package: {result['name']} v{result['version']}")
print(f"Summary: {result['summary']}")
print(f"Dependencies: {len(result['dependencies'])}")
```

### Security Analysis

```python
# Check for vulnerabilities in a specific version
vuln_check = await check_vulnerabilities("django", "2.0.0")
if vuln_check["has_vulnerabilities"]:
    print(f"⚠️ Found {vuln_check['vulnerability_count']} vulnerabilities")
    for vuln in vuln_check["vulnerabilities"]:
        print(f"- {vuln['id']}: {vuln['summary']}")
        if vuln["fixed_in"]:
            print(f"  Fixed in: {', '.join(vuln['fixed_in'])}")
else:
    print("✅ No known vulnerabilities")
```

### Dependency Analysis

```python
# Analyze dependencies for a package
deps = await get_dependencies("fastapi", include_extras=True)
print(f"Runtime dependencies: {len(deps['runtime_dependencies'])}")
print(f"Available extras: {', '.join(deps['available_extras'])}")

# Check Python compatibility
compat = await check_compatibility("numpy", "1.24.0", "3.11")
print(f"Compatible with Python 3.11: {compat['is_compatible']}")
```

### Package Comparison

```python
# Compare two versions of the same package
comparison = await compare_versions("django", "4.1.0", "4.2.0")
newer = comparison["comparison"]["newer_version"]
print(f"Newer version: {newer}")

# Get package health assessment
health = await get_package_health("requests")
print(f"Health status: {health['health_status']} (score: {health['health_score']})")
```

### Search and Discovery

```python
# Search for packages
search_results = await search_packages("web framework", limit=5)
for result in search_results["results"]:
    print(f"- {result['name']}: {result['summary']}")

# Get PyPI statistics
stats = await get_pypi_stats()
print(f"Total PyPI size: {stats['total_size_formatted']}")
```

### Integration with Claude Desktop

Add the following configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "pypi": {
      "command": "pypi-mcp",
      "args": [],
      "env": {
        "PYPI_MCP_LOG_LEVEL": "INFO",
        "PYPI_MCP_CACHE_TTL": "300",
        "PYPI_MCP_RATE_LIMIT": "10.0"
      }
    }
  }
}
```

Then you can ask Claude questions like:
- "What is the latest version of FastAPI and what are its dependencies?"
- "Check if Django 3.2.0 has any known vulnerabilities"
- "Compare FastAPI vs Flask for building web APIs"
- "Is numpy 1.24.0 compatible with Python 3.11?"

### HTTP Transport Usage

For HTTP transport, start the server:

```bash
pypi-mcp --transport http --host 0.0.0.0 --port 8000
```

Then connect using any MCP client that supports HTTP transport.

## Development Setup

### Prerequisites for Development

- Python 3.11 or higher
- uv (recommended) or pip
- Git

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp

# Install with development dependencies using uv
uv sync --dev

# Or using pip
pip install -e ".[dev]"
```

### Development Dependencies

The project includes comprehensive development tools:

- **Testing**: pytest, pytest-asyncio, pytest-httpx, pytest-mock, pytest-cov, respx
- **Code Quality**: black, isort, mypy, ruff
- **Coverage**: pytest-cov for test coverage reporting

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=pypi_mcp --cov-report=html

# Run specific test categories
uv run pytest -m unit          # Unit tests only
uv run pytest -m integration   # Integration tests only
uv run pytest -m performance   # Performance tests only

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_server.py
```

### Code Quality Tools

```bash
# Format code with black
uv run black pypi_mcp/ tests/

# Sort imports with isort
uv run isort pypi_mcp/ tests/

# Type checking with mypy
uv run mypy pypi_mcp/

# Linting with ruff
uv run ruff check pypi_mcp/ tests/

# Fix linting issues automatically
uv run ruff check --fix pypi_mcp/ tests/
```

### Project Structure

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
│   ├── test_server.py     # Server tests
│   ├── test_config.py     # Configuration tests
│   ├── test_integration.py # Integration tests
│   ├── test_performance.py # Performance tests
│   └── test_*.py          # Other test modules
├── examples/              # Usage examples
│   ├── basic_usage.py     # Basic usage demonstration
│   └── claude_desktop_config.json # Claude Desktop config
├── pyproject.toml         # Project configuration
├── README.md              # Project README
├── DOCUMENTATION.md       # This documentation
└── LICENSE                # MIT License
```

### Adding New Features

1. **Create a new branch**: `git checkout -b feature/your-feature-name`
2. **Write tests first**: Add tests in the appropriate test file
3. **Implement the feature**: Add your code following existing patterns
4. **Update documentation**: Update this documentation if needed
5. **Run quality checks**: Ensure all tests pass and code quality tools are satisfied
6. **Submit a pull request**: Include a clear description of your changes

### Testing Guidelines

- Write unit tests for all new functions and methods
- Use pytest fixtures for common test data
- Mock external API calls in unit tests
- Include integration tests for end-to-end functionality
- Aim for high test coverage (>90%)
- Use descriptive test names that explain what is being tested

### Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable and function names
- Add comments for complex logic

### Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with new features and fixes
3. Run full test suite: `uv run pytest`
4. Run code quality checks: `uv run black . && uv run isort . && uv run mypy . && uv run ruff check .`
5. Create a git tag: `git tag v0.x.x`
6. Push to GitHub: `git push origin main --tags`
7. GitHub Actions will handle the rest

## Troubleshooting

### Common Issues and Solutions

#### 1. Installation Issues

**Problem**: `uv sync` fails with dependency resolution errors

**Solution**:
```bash
# Clear uv cache and try again
uv cache clean
uv sync

# Or use pip as fallback
pip install -e .
```

**Problem**: Python version compatibility issues

**Solution**:
```bash
# Check Python version
python --version

# Ensure you have Python 3.11+
# Install using pyenv if needed
pyenv install 3.11.0
pyenv local 3.11.0
```

#### 2. Runtime Issues

**Problem**: `ModuleNotFoundError: No module named 'pypi_mcp'`

**Solution**:
```bash
# Ensure the package is installed in development mode
pip install -e .

# Or check your Python path
python -c "import sys; print(sys.path)"
```

**Problem**: HTTP timeout errors when querying PyPI

**Solution**:
```bash
# Increase timeout in environment variables
export PYPI_MCP_TIMEOUT=60.0

# Or check your internet connection
curl -I https://pypi.org/pypi/requests/json
```

**Problem**: Rate limiting errors

**Solution**:
```bash
# Reduce rate limit
export PYPI_MCP_RATE_LIMIT=5.0

# Or increase cache TTL to reduce API calls
export PYPI_MCP_CACHE_TTL=600
```

#### 3. Configuration Issues

**Problem**: Environment variables not being loaded

**Solution**:
```bash
# Check if .env file exists and has correct format
cat .env

# Ensure variables have PYPI_MCP_ prefix
export PYPI_MCP_LOG_LEVEL=DEBUG

# Verify configuration is loaded
python -c "from pypi_mcp.config import settings; print(settings.log_level)"
```

**Problem**: Logging not working as expected

**Solution**:
```bash
# Set log level explicitly
export PYPI_MCP_LOG_LEVEL=DEBUG

# Check log format
export PYPI_MCP_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

#### 4. MCP Integration Issues

**Problem**: Claude Desktop not recognizing the server

**Solution**:
1. Verify the server is installed: `pypi-mcp --help`
2. Check Claude Desktop configuration syntax
3. Restart Claude Desktop after configuration changes
4. Check Claude Desktop logs for error messages

**Problem**: STDIO transport not working

**Solution**:
```bash
# Test the server directly
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | pypi-mcp

# Check if the server starts without errors
pypi-mcp --log-level DEBUG
```

**Problem**: HTTP transport connection issues

**Solution**:
```bash
# Check if the server is running
curl http://localhost:8000/health

# Verify port is not in use
netstat -an | grep 8000

# Try a different port
pypi-mcp --transport http --port 8080
```

#### 5. Performance Issues

**Problem**: Slow response times

**Solution**:
```bash
# Enable caching with longer TTL
export PYPI_MCP_CACHE_TTL=600
export PYPI_MCP_CACHE_MAX_SIZE=2000

# Reduce rate limiting if you have good network
export PYPI_MCP_RATE_LIMIT=20.0
```

**Problem**: High memory usage

**Solution**:
```bash
# Reduce cache size
export PYPI_MCP_CACHE_MAX_SIZE=500

# Monitor memory usage
python -c "from pypi_mcp.cache import get_cache_stats; import asyncio; print(asyncio.run(get_cache_stats()))"
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Set `PYPI_MCP_LOG_LEVEL=DEBUG` for detailed logging
2. **Search existing issues**: Check the [GitHub Issues](https://github.com/AstroAir/pypi-mcp/issues)
3. **Create a new issue**: Include:
   - Python version
   - Operating system
   - Full error message
   - Steps to reproduce
   - Configuration (environment variables)
4. **Join discussions**: Participate in [GitHub Discussions](https://github.com/AstroAir/pypi-mcp/discussions)

### Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
# Set debug logging
export PYPI_MCP_LOG_LEVEL=DEBUG

# Run with verbose output
pypi-mcp --log-level DEBUG

# Check cache statistics
python -c "
from pypi_mcp.cache import get_cache_stats
import asyncio
print(asyncio.run(get_cache_stats()))
"
```

### Performance Monitoring

Monitor server performance:

```bash
# Check cache hit rate
curl http://localhost:8000/cache/stats  # If using HTTP transport

# Monitor response times
time pypi-mcp --help

# Check memory usage
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

---

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of conduct
- Development workflow
- Pull request process
- Issue reporting guidelines

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyPI](https://pypi.org/) for providing the package index API
- [FastMCP](https://gofastmcp.com/) for the excellent MCP framework
- The Python packaging community for their tools and standards
- All contributors who help improve this project
