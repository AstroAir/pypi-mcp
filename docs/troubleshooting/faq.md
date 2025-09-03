# Frequently Asked Questions

Common questions and answers about the PyPI MCP Server.

## General Questions

### What is PyPI MCP Server?

PyPI MCP Server is a Model Context Protocol (MCP) server that provides AI models with tools to query PyPI package information, analyze dependencies, check for vulnerabilities, and manage Python package data.

### What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI models to external data sources and tools. It allows AI assistants like Claude to access and interact with external services through a standardized interface.

### Why use PyPI MCP Server instead of direct PyPI API calls?

PyPI MCP Server provides:

- **Intelligent Caching**: Reduces API calls and improves performance
- **Rate Limiting**: Respects PyPI's rate limits automatically
- **Data Enrichment**: Adds vulnerability checking and package health assessment
- **Standardized Interface**: Consistent API across different tools
- **Error Handling**: Robust error handling and retry logic
- **AI Integration**: Designed specifically for AI model integration

## Installation and Setup

### What Python versions are supported?

Python 3.11 or higher is required. The server is tested on:

- Python 3.11
- Python 3.12

### Can I install PyPI MCP Server with pip?

Yes, you can install it with pip:

```bash
pip install pypi-mcp
```

However, we recommend using `uv` for better dependency management:

```bash
uv add pypi-mcp
```

### How do I integrate with Claude Desktop?

Add this configuration to your Claude Desktop config file:

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

Configuration file locations:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

### Do I need an API key for PyPI?

No, PyPI MCP Server uses PyPI's public API which doesn't require authentication. However, you should respect rate limits to avoid being blocked.

## Configuration

### How do I configure the server?

Use environment variables with the `PYPI_MCP_` prefix:

```bash
export PYPI_MCP_LOG_LEVEL=INFO
export PYPI_MCP_CACHE_TTL=300
export PYPI_MCP_RATE_LIMIT=10.0
```

Or create a `.env` file:

```env
PYPI_MCP_LOG_LEVEL=INFO
PYPI_MCP_CACHE_TTL=300
PYPI_MCP_RATE_LIMIT=10.0
```

### What are the recommended settings for production?

```bash
export PYPI_MCP_LOG_LEVEL=WARNING
export PYPI_MCP_CACHE_TTL=900
export PYPI_MCP_CACHE_MAX_SIZE=5000
export PYPI_MCP_RATE_LIMIT=20.0
export PYPI_MCP_TIMEOUT=30.0
```

### How do I increase performance?

1. **Increase cache size and TTL**:

   ```bash
   export PYPI_MCP_CACHE_MAX_SIZE=10000
   export PYPI_MCP_CACHE_TTL=1800
   ```

2. **Increase rate limit** (if your network can handle it):

   ```bash
   export PYPI_MCP_RATE_LIMIT=50.0
   ```

3. **Use HTTP transport** for multiple clients:
   ```bash
   pypi-mcp --transport http
   ```

## Features and Capabilities

### What tools are available?

The server provides 10 tools:

1. **get_package_info** - Get detailed package metadata
2. **get_package_versions** - List all package versions
3. **search_packages** - Search for packages by name/keywords
4. **compare_versions** - Compare two package versions
5. **check_compatibility** - Check Python version compatibility
6. **get_dependencies** - Analyze package dependencies
7. **check_vulnerabilities** - Check for security vulnerabilities
8. **get_package_health** - Assess package health
9. **get_pypi_stats** - Get PyPI statistics
10. **get_cache_info** - Get cache information

### Does it check for security vulnerabilities?

Yes, the `check_vulnerabilities` tool checks for known security vulnerabilities using multiple sources including the GitHub Advisory Database.

### Can I search for packages?

Yes, use the `search_packages` tool:

```json
{
  "tool": "search_packages",
  "arguments": {
    "query": "web framework",
    "limit": 10
  }
}
```

### Does it support dependency analysis?

Yes, the `get_dependencies` tool provides comprehensive dependency analysis including:

- Runtime dependencies
- Optional dependencies (extras)
- Environment markers
- Version specifications

## Performance and Caching

### How does caching work?

The server uses TTL-based caching with LRU eviction:

- **TTL (Time To Live)**: Items expire after configured time (default: 5 minutes)
- **LRU (Least Recently Used)**: Removes oldest items when cache is full
- **Configurable**: Both TTL and size limits are configurable

### How can I monitor cache performance?

Use the `get_cache_info` tool:

```json
{
  "tool": "get_cache_info"
}
```

This returns hit rate, cache size, and other statistics.

### What's a good cache hit rate?

- **Excellent**: >80%
- **Good**: 60-80%
- **Poor**: <60%

If your hit rate is low, consider increasing cache size or TTL.

### How much memory does the cache use?

Approximately 10KB per cached item. For the default cache size (1000 items), expect ~10MB of memory usage.

## Troubleshooting

### The server won't start. What should I check?

1. **Python version**: Ensure Python 3.11+
2. **Installation**: Verify with `pypi-mcp --help`
3. **Dependencies**: Check all dependencies are installed
4. **Configuration**: Verify environment variables are valid
5. **Ports**: For HTTP transport, ensure port isn't in use

### I'm getting timeout errors. How do I fix this?

1. **Increase timeout**:

   ```bash
   export PYPI_MCP_TIMEOUT=60.0
   ```

2. **Check network connectivity**:

   ```bash
   curl -I https://pypi.org
   ```

3. **Reduce rate limit**:
   ```bash
   export PYPI_MCP_RATE_LIMIT=5.0
   ```

### Claude Desktop doesn't see the server. What's wrong?

1. **Check server is installed**: `pypi-mcp --help`
2. **Verify configuration file** syntax and location
3. **Restart Claude Desktop** after configuration changes
4. **Check logs** with debug logging enabled

### How do I enable debug logging?

```bash
export PYPI_MCP_LOG_LEVEL=DEBUG
pypi-mcp --log-level DEBUG
```

### The server is using too much memory. How do I reduce it?

1. **Reduce cache size**:

   ```bash
   export PYPI_MCP_CACHE_MAX_SIZE=500
   ```

2. **Reduce cache TTL**:

   ```bash
   export PYPI_MCP_CACHE_TTL=300
   ```

3. **Monitor memory usage**:
   ```python
   import psutil
   import os
   process = psutil.Process(os.getpid())
   print(f'Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB')
   ```

## Development and Contributing

### How do I set up a development environment?

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AstroAir/pypi-mcp.git
   cd pypi-mcp
   ```

2. **Install with development dependencies**:

   ```bash
   uv sync --dev
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

### How do I run tests?

```bash
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# With coverage
pytest --cov=pypi_mcp
```

### How do I contribute?

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make changes** following coding standards
4. **Write tests** for new functionality
5. **Submit a pull request**

See the [Contributing Guide](../developer-guide/contributing.md) for details.

### What coding standards do you use?

- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **ruff** for linting
- **Type hints** for all functions
- **Docstrings** for all public APIs

## Integration and Usage

### Can I use this with other AI models besides Claude?

Yes, any MCP-compatible client can use the server. The server implements the standard MCP protocol.

### Can I run multiple instances?

Yes, you can run multiple instances:

- **STDIO transport**: One instance per client
- **HTTP transport**: Multiple clients can connect to one instance

### How do I use HTTP transport?

```bash
# Start HTTP server
pypi-mcp --transport http --host 0.0.0.0 --port 8000

# Test with curl
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

### Can I deploy this in production?

Yes, the server is designed for production use. Consider:

- **Security**: Use HTTPS and network isolation
- **Monitoring**: Monitor performance and error rates
- **Scaling**: Use HTTP transport with load balancing
- **Caching**: Optimize cache settings for your workload

### Is there a Docker image?

You can build your own Docker image:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["pypi-mcp", "--transport", "http", "--host", "0.0.0.0"]
```

## Limitations and Known Issues

### What are the current limitations?

1. **No authentication**: Currently no built-in authentication
2. **No manual cache invalidation**: Cache can only be cleared by restarting
3. **PyPI dependency**: Requires PyPI API availability
4. **Memory usage**: Cache is stored in memory only

### Are there rate limits?

Yes, the server implements client-side rate limiting to respect PyPI's limits. Default is 10 requests per second, configurable via `PYPI_MCP_RATE_LIMIT`.

### What happens if PyPI is down?

The server will return errors for new requests. Cached data will still be available until it expires.

### Can I use private PyPI repositories?

Currently, the server only supports the public PyPI repository. Private repository support may be added in future versions.

## Future Plans

### What features are planned?

- Authentication and authorization
- Private PyPI repository support
- Manual cache invalidation
- Persistent caching
- GraphQL API
- WebSocket transport
- Package download statistics
- Enhanced security scanning

### How can I request a feature?

1. **Check existing issues** for similar requests
2. **Create a feature request** on GitHub
3. **Participate in discussions** about the feature
4. **Consider contributing** the feature yourself

### Is there a roadmap?

Check the [GitHub Issues](https://github.com/AstroAir/pypi-mcp/issues) and [Discussions](https://github.com/AstroAir/pypi-mcp/discussions) for planned features and roadmap discussions.

## Getting Help

### Where can I get help?

- **Documentation**: Read the complete documentation
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and discuss
- **Common Issues**: Check the troubleshooting guide

### How do I report a bug?

1. **Search existing issues** first
2. **Use the bug report template**
3. **Include system information**:
   - OS and version
   - Python version
   - PyPI MCP version
   - Configuration (sanitized)
   - Complete error message
   - Steps to reproduce

### What information should I include in bug reports?

- **Environment details**: OS, Python version, package version
- **Configuration**: Environment variables (remove sensitive data)
- **Error messages**: Complete error output
- **Steps to reproduce**: Minimal example that reproduces the issue
- **Expected vs actual behavior**: What you expected vs what happened

## License and Legal

### What license is PyPI MCP Server under?

MIT License. See the [LICENSE](https://github.com/AstroAir/pypi-mcp/blob/main/LICENSE) file for details.

### Can I use this commercially?

Yes, the MIT license allows commercial use.

### Are there any legal considerations?

- **Respect PyPI's terms of service**
- **Don't abuse rate limits**
- **Consider data privacy** if handling sensitive package information
- **Review security implications** for your use case
