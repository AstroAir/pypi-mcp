# Quick Start

Get up and running with PyPI MCP Server in minutes.

## Prerequisites

Before you begin, ensure you have:

- Python 3.11 or higher installed
- [Completed the installation](installation.md)

## Running the Server

The PyPI MCP server supports two transport protocols:

### STDIO Transport (Default)

STDIO transport is used for direct integration with MCP clients like Claude Desktop:

```bash
# Run with default STDIO transport
pypi-mcp

# With debug logging
pypi-mcp --log-level DEBUG
```

The server will start and wait for MCP protocol messages on stdin/stdout.

### HTTP Transport

HTTP transport allows you to run the server as a web service:

```bash
# Run with HTTP transport on default port (8000)
pypi-mcp --transport http

# Specify custom host and port
pypi-mcp --transport http --host 0.0.0.0 --port 8080

# With debug logging
pypi-mcp --transport http --log-level DEBUG
```

The server will start and be accessible at `http://localhost:8000` (or your specified host/port).

## Basic Usage Examples

Once the server is running, you can interact with it through an MCP client. Here are some basic examples:

### Package Information

Get detailed information about a package:

```json
{
  "tool": "get_package_info",
  "arguments": {
    "package_name": "requests"
  }
}
```

### Search Packages

Search for packages by name or keywords:

```json
{
  "tool": "search_packages",
  "arguments": {
    "query": "web framework",
    "limit": 5
  }
}
```

### Check Vulnerabilities

Check for security vulnerabilities:

```json
{
  "tool": "check_vulnerabilities",
  "arguments": {
    "package_name": "django",
    "version": "3.2.0"
  }
}
```

### Analyze Dependencies

Get dependency information:

```json
{
  "tool": "get_dependencies",
  "arguments": {
    "package_name": "fastapi",
    "include_extras": true
  }
}
```

## Testing the Installation

### Command Line Test

Test that the server is properly installed:

```bash
# Check version and help
pypi-mcp --help

# Test with debug output
pypi-mcp --log-level DEBUG
```

### HTTP Transport Test

If using HTTP transport, you can test with curl:

```bash
# Start the server
pypi-mcp --transport http &

# Test the server (replace with actual MCP request)
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": 1}'
```

## Environment Configuration

### Basic Configuration

Set up basic environment variables:

```bash
# Set log level
export PYPI_MCP_LOG_LEVEL=INFO

# Configure cache
export PYPI_MCP_CACHE_TTL=300
export PYPI_MCP_CACHE_MAX_SIZE=1000

# Set rate limiting
export PYPI_MCP_RATE_LIMIT=10.0
```

### Configuration File

Create a `.env` file in your project directory:

```env
# .env file
PYPI_MCP_LOG_LEVEL=INFO
PYPI_MCP_CACHE_TTL=300
PYPI_MCP_RATE_LIMIT=10.0
PYPI_MCP_TIMEOUT=30.0
```

## Integration Examples

### Claude Desktop Integration

Add to your Claude Desktop configuration file:

=== "Basic Configuration"

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

=== "With Environment Variables"

    ```json
    {
      "mcpServers": {
        "pypi": {
          "command": "pypi-mcp",
          "args": [],
          "env": {
            "PYPI_MCP_LOG_LEVEL": "INFO",
            "PYPI_MCP_CACHE_TTL": "600"
          }
        }
      }
    }
    ```

=== "With Custom Arguments"

    ```json
    {
      "mcpServers": {
        "pypi": {
          "command": "pypi-mcp",
          "args": ["--log-level", "DEBUG"]
        }
      }
    }
    ```

### Example Queries for AI Assistants

Once integrated with an AI assistant, you can ask natural language questions:

!!! example "Package Information Queries" - "What is the latest version of FastAPI and what are its dependencies?" - "Show me information about the requests package" - "What Python versions does Django 4.2 support?"

!!! example "Security Queries" - "Check if Django 3.2.0 has any known vulnerabilities" - "Are there any security issues with requests version 2.25.0?" - "What's the security status of the latest numpy version?"

!!! example "Comparison Queries" - "Compare FastAPI vs Flask for building web APIs" - "What are the differences between Django 4.1 and 4.2?" - "Should I use requests or httpx for HTTP client?"

!!! example "Analysis Queries" - "Analyze the health of the pandas package" - "What are the dependencies of scikit-learn?" - "Show me the top 10 largest packages on PyPI"

## Verification

### Successful Installation Indicators

You'll know the installation is successful when:

1. **Command Help Works**: `pypi-mcp --help` shows usage information
2. **Server Starts**: No errors when starting with `pypi-mcp`
3. **Logs Appear**: You see startup logs when using `--log-level DEBUG`
4. **MCP Client Connects**: Your MCP client can successfully connect and use tools

### Common Success Messages

When everything is working correctly, you should see logs like:

```
2025-01-XX XX:XX:XX - pypi_mcp.server - INFO - Starting PyPI MCP Server with stdio transport
2025-01-XX XX:XX:XX - pypi_mcp.client - INFO - PyPI client initialized
2025-01-XX XX:XX:XX - pypi_mcp.cache - INFO - Cache initialized with TTL=300, max_size=1000
```

## Next Steps

Now that you have the server running:

1. **[Configure the Server](../user-guide/configuration.md)** - Customize settings for your needs
2. **[Explore Usage Examples](../user-guide/usage-examples.md)** - See practical usage patterns
3. **[Learn About Integration](integration.md)** - Integrate with different MCP clients
4. **[API Reference](../api-reference/tools.md)** - Explore all available tools and features

## Getting Help

If you encounter issues during quick start:

- Check the [Common Issues](../troubleshooting/common-issues.md) guide
- Review the [Installation](installation.md) guide
- Visit our [GitHub Issues](https://github.com/AstroAir/pypi-mcp/issues) page
