# PyPI MCP Server

A comprehensive Model Context Protocol (MCP) server for PyPI package information and management.

## Overview

PyPI MCP Server provides AI models with powerful tools to query PyPI package information, analyze dependencies, check for vulnerabilities, and manage Python package data. Built with FastMCP, it offers async/await support, intelligent caching, and comprehensive package analysis capabilities.

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI models to external data sources and tools. This server acts as a bridge between AI models (like Claude) and the Python Package Index (PyPI), enabling AI assistants to:

- 🔍 Search and analyze Python packages
- 📊 Analyze dependencies and compatibility
- 🔒 Check for security vulnerabilities
- 📈 Access PyPI statistics and metrics
- 🛠️ Compare package versions and health

## Key Features

### Package Discovery & Search

- Search for packages by name or keywords
- Get detailed package metadata and information
- List all available versions of a package
- Compare different versions of packages

### Dependency Analysis

- Analyze package dependencies and requirements
- Check Python version compatibility
- Identify optional dependencies and extras
- Dependency tree analysis

### Security & Vulnerability Checking

- Check for known security vulnerabilities
- Get detailed CVE information
- Security recommendations and mitigation advice
- Package health assessment

### Statistics & Analytics

- PyPI-wide statistics and top packages
- Package download statistics (when available)
- Package size and file information
- Maintenance and activity metrics

### Advanced Features

- Async/await support for high performance
- Intelligent caching with TTL
- Rate limiting and error handling
- Support for both HTTP and STDIO transports
- Comprehensive logging and monitoring

## Architecture

The server is built with modern Python technologies:

- **FastMCP**: Modern MCP framework providing the server foundation
- **httpx**: Async HTTP client for PyPI API interactions
- **Pydantic**: Data validation and serialization with type safety
- **packaging**: Python package version handling and requirement parsing
- **cachetools**: Intelligent caching system with TTL support

## Quick Start

### Installation

```bash
# Using uv (recommended)
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
uv sync
```

### Running the Server

```bash
# STDIO transport (for MCP clients)
pypi-mcp

# HTTP transport
pypi-mcp --transport http --host 0.0.0.0 --port 8000
```

### Integration with Claude Desktop

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

## Example Queries

Once integrated, you can ask AI assistants questions like:

- "What is the latest version of FastAPI and what are its dependencies?"
- "Check if Django 3.2.0 has any known vulnerabilities"
- "Compare FastAPI vs Flask for building web APIs"
- "Is numpy 1.24.0 compatible with Python 3.11?"
- "What are the top 10 largest packages on PyPI?"

## Next Steps

- [Installation Guide](getting-started/installation.md) - Detailed installation instructions
- [Configuration](user-guide/configuration.md) - Configure the server for your needs
- [API Reference](api-reference/tools.md) - Complete API documentation
- [Usage Examples](user-guide/usage-examples.md) - Practical usage examples
- [Development Setup](developer-guide/development-setup.md) - Contributing to the project

## Support

- [GitHub Repository](https://github.com/AstroAir/pypi-mcp)
- [Issues](https://github.com/AstroAir/pypi-mcp/issues)
- [Discussions](https://github.com/AstroAir/pypi-mcp/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/AstroAir/pypi-mcp/blob/main/LICENSE) file for details.
