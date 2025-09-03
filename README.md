# PyPI MCP Server

A comprehensive Model Context Protocol (MCP) server for PyPI package information and management. This server provides AI models with powerful tools to query PyPI package data, analyze dependencies, check for vulnerabilities, and manage Python package information.

## Features

### 🔍 Package Discovery & Search
- Search for packages by name or keywords
- Get detailed package metadata and information
- List all available versions of a package
- Compare different versions of packages

### 📊 Dependency Analysis
- Analyze package dependencies and requirements
- Check Python version compatibility
- Identify optional dependencies and extras
- Dependency tree analysis

### 🔒 Security & Vulnerability Checking
- Check for known security vulnerabilities
- Get detailed CVE information
- Security recommendations and mitigation advice
- Package health assessment

### 📈 Statistics & Analytics
- PyPI-wide statistics and top packages
- Package download statistics (when available)
- Package size and file information
- Maintenance and activity metrics

### 🛠️ Advanced Features
- Async/await support for high performance
- Intelligent caching with TTL
- Rate limiting and error handling
- Support for both HTTP and STDIO transports
- Comprehensive logging and monitoring

## Installation

### Using uv (recommended)
```bash
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
uv sync
```

### Using pip
```bash
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
pip install -e .
```

## Quick Start

### Running with STDIO (for local MCP clients)
```bash
# Using the installed script
pypi-mcp

# Or directly with Python
python -m pypi_mcp.server
```

### Running with HTTP transport
```bash
pypi-mcp --transport http --host 0.0.0.0 --port 8000
```

## Available Tools

### Package Information
- `get_package_info(package_name, version?, include_files?)` - Get detailed package metadata
- `get_package_versions(package_name, limit?, include_prereleases?)` - List package versions
- `search_packages(query, limit?, include_description?)` - Search for packages

### Version Management
- `compare_versions(package_name, version1, version2)` - Compare two package versions
- `check_compatibility(package_name, version?, python_version?)` - Check Python compatibility

### Dependencies
- `get_dependencies(package_name, version?, include_extras?)` - Analyze package dependencies

### Security
- `check_vulnerabilities(package_name, version?)` - Check for security vulnerabilities
- `get_package_health(package_name, version?)` - Assess package health and maintenance

### Statistics
- `get_pypi_stats()` - Get PyPI-wide statistics
- `get_cache_info()` - Get server cache information

## Available Resources

- `pypi://stats/overview` - PyPI statistics overview
- `pypi://package/{package_name}` - Package metadata resource

## Available Prompts

- `analyze_package(package_name, version?)` - Generate comprehensive package analysis
- `compare_packages(package1, package2)` - Generate package comparison analysis
- `security_review(package_name)` - Generate security review prompt

## Configuration

The server can be configured using environment variables:

```bash
# PyPI API settings
export PYPI_MCP_PYPI_BASE_URL="https://pypi.org"
export PYPI_MCP_USER_AGENT="pypi-mcp/0.1.0"

# Performance settings
export PYPI_MCP_TIMEOUT=30.0
export PYPI_MCP_RATE_LIMIT=10.0
export PYPI_MCP_CACHE_TTL=300
export PYPI_MCP_CACHE_MAX_SIZE=1000

# Logging
export PYPI_MCP_LOG_LEVEL="INFO"

# Feature flags
export PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true
export PYPI_MCP_ENABLE_STATS=true
export PYPI_MCP_ENABLE_SEARCH=true
```

## Usage Examples

### With Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "pypi": {
      "command": "pypi-mcp",
      "args": []
    }
  }
}
```

### Example Queries

1. **Package Information**: "What is the latest version of FastAPI and what are its dependencies?"

2. **Security Check**: "Check if Django 3.2.0 has any known vulnerabilities"

3. **Package Comparison**: "Compare FastAPI vs Flask for building web APIs"

4. **Dependency Analysis**: "What are the runtime dependencies of requests?"

5. **Compatibility Check**: "Is numpy 1.24.0 compatible with Python 3.11?"

## Development

### Setting up development environment

```bash
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
uv sync --dev
```

### Running tests

```bash
uv run pytest
```

### Code formatting

```bash
uv run black pypi_mcp/
uv run isort pypi_mcp/
```

### Type checking

```bash
uv run mypy pypi_mcp/
```

## Architecture

The server is built with:

- **FastMCP**: Modern MCP framework for Python
- **httpx**: Async HTTP client for PyPI API calls
- **Pydantic**: Data validation and serialization
- **packaging**: Python package version handling
- **cachetools**: Intelligent caching system

### Key Components

- `server.py` - Main FastMCP server with tool definitions
- `client.py` - PyPI API client with async support
- `models.py` - Pydantic data models
- `cache.py` - Caching utilities
- `config.py` - Configuration management
- `utils.py` - Helper functions
- `exceptions.py` - Custom exceptions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [PyPI](https://pypi.org/) for providing the package index API
- [FastMCP](https://gofastmcp.com/) for the excellent MCP framework
- The Python packaging community for their tools and standards
