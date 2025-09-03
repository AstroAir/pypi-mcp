# API Reference Overview

Complete reference for the PyPI MCP Server API, including tools, resources, prompts, and data models.

## API Components

The PyPI MCP Server provides a comprehensive API with the following components:

### Tools (10 available)

Tools are the primary interface for interacting with PyPI data:

| Tool                                                      | Purpose                            | Category            |
| --------------------------------------------------------- | ---------------------------------- | ------------------- |
| [`get_package_info`](tools.md#get_package_info)           | Get detailed package metadata      | Package Information |
| [`get_package_versions`](tools.md#get_package_versions)   | List all package versions          | Package Information |
| [`search_packages`](tools.md#search_packages)             | Search for packages                | Discovery           |
| [`compare_versions`](tools.md#compare_versions)           | Compare two package versions       | Analysis            |
| [`check_compatibility`](tools.md#check_compatibility)     | Check Python compatibility         | Analysis            |
| [`get_dependencies`](tools.md#get_dependencies)           | Analyze package dependencies       | Dependencies        |
| [`check_vulnerabilities`](tools.md#check_vulnerabilities) | Check for security vulnerabilities | Security            |
| [`get_package_health`](tools.md#get_package_health)       | Assess package health              | Analysis            |
| [`get_pypi_stats`](tools.md#get_pypi_stats)               | Get PyPI statistics                | Statistics          |
| [`get_cache_info`](tools.md#get_cache_info)               | Get cache information              | System              |

### Resources (2 available)

Resources provide static or dynamic content:

| Resource                                          | URI Pattern             | Purpose                   |
| ------------------------------------------------- | ----------------------- | ------------------------- |
| [PyPI Stats](resources.md#pypi-stats-overview)    | `pypi://stats/overview` | PyPI statistics overview  |
| [Package Resource](resources.md#package-resource) | `pypi://package/{name}` | Package metadata resource |

### Prompts (3 available)

Prompts provide structured templates for AI analysis:

| Prompt                                            | Purpose                        | Use Case             |
| ------------------------------------------------- | ------------------------------ | -------------------- |
| [`analyze_package`](prompts.md#analyze_package)   | Comprehensive package analysis | Package evaluation   |
| [`compare_packages`](prompts.md#compare_packages) | Package comparison analysis    | Technology selection |
| [`security_review`](prompts.md#security_review)   | Security review template       | Security assessment  |

## Protocol Information

### JSON-RPC 2.0

The PyPI MCP Server uses JSON-RPC 2.0 protocol for communication:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_package_info",
    "arguments": {
      "package_name": "requests"
    }
  },
  "id": 1
}
```

### MCP Protocol Version

- **Supported Version**: `2024-11-05`
- **Protocol**: Model Context Protocol (MCP)
- **Transport**: STDIO and HTTP

### Request/Response Format

#### Tool Call Request

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param1": "value1",
      "param2": "value2"
    }
  },
  "id": 1
}
```

#### Tool Call Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Tool execution result"
      }
    ]
  },
  "id": 1
}
```

#### Error Response

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "details": "Package name is required"
    }
  },
  "id": 1
}
```

## Data Types

### Common Data Types

| Type      | Description      | Example              |
| --------- | ---------------- | -------------------- |
| `string`  | Text string      | `"requests"`         |
| `integer` | Whole number     | `42`                 |
| `float`   | Decimal number   | `3.14`               |
| `boolean` | True/false value | `true`               |
| `array`   | List of items    | `["item1", "item2"]` |
| `object`  | Key-value pairs  | `{"key": "value"}`   |
| `null`    | Null value       | `null`               |

### Package-Specific Types

| Type             | Description       | Format                                 |
| ---------------- | ----------------- | -------------------------------------- |
| `package_name`   | PyPI package name | Lowercase, hyphens/underscores allowed |
| `version`        | Package version   | PEP 440 compliant version string       |
| `version_spec`   | Version specifier | `>=1.0.0,<2.0.0`                       |
| `python_version` | Python version    | `3.11`, `3.12.1`                       |
| `url`            | HTTP/HTTPS URL    | `https://example.com`                  |
| `datetime`       | ISO 8601 datetime | `2025-01-15T10:30:00Z`                 |

## Error Handling

### Error Codes

The server uses standard JSON-RPC error codes plus custom codes:

| Code     | Name                | Description                   |
| -------- | ------------------- | ----------------------------- |
| `-32700` | Parse error         | Invalid JSON                  |
| `-32600` | Invalid Request     | Invalid JSON-RPC request      |
| `-32601` | Method not found    | Unknown method                |
| `-32602` | Invalid params      | Invalid parameters            |
| `-32603` | Internal error      | Server internal error         |
| `-32000` | Package not found   | Package doesn't exist on PyPI |
| `-32001` | Validation error    | Parameter validation failed   |
| `-32002` | Rate limit exceeded | Too many requests             |
| `-32003` | Timeout error       | Request timed out             |

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Package not found",
    "data": {
      "package_name": "nonexistent-package",
      "details": "The package 'nonexistent-package' was not found on PyPI"
    }
  },
  "id": 1
}
```

## Rate Limiting

### Rate Limit Policy

- **Default Limit**: 10 requests per second
- **Configurable**: Via `PYPI_MCP_RATE_LIMIT` environment variable
- **Per-Client**: Rate limiting is applied per client connection
- **Burst Handling**: Short bursts are allowed within limits

### Rate Limit Headers (HTTP Transport)

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1642694400
```

### Rate Limit Exceeded Response

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32002,
    "message": "Rate limit exceeded",
    "data": {
      "limit": 10,
      "reset_time": "2025-01-15T10:31:00Z"
    }
  },
  "id": 1
}
```

## Caching Behavior

### Cache Strategy

- **TTL-based**: Items expire after configured time
- **LRU Eviction**: Least recently used items removed when full
- **Transparent**: Caching is transparent to clients
- **Configurable**: TTL and size limits are configurable

### Cache Headers (HTTP Transport)

```http
X-Cache-Status: HIT
X-Cache-TTL: 300
X-Cache-Age: 45
```

### Cached Operations

All read operations are cached:

- Package information queries
- Version listings
- Search results
- Dependency analysis
- Vulnerability checks
- Statistics

## Authentication

### Current Status

- **No Authentication**: Currently no authentication required
- **Network Security**: Rely on network-level security
- **Future Plans**: Authentication may be added in future versions

### Security Recommendations

For production deployments:

1. **Network Isolation**: Run on private networks
2. **Reverse Proxy**: Use nginx/apache with authentication
3. **Firewall Rules**: Restrict access to authorized clients
4. **HTTPS**: Use HTTPS for HTTP transport

## Versioning

### API Versioning

- **Current Version**: 0.1.0
- **Compatibility**: Backward compatibility maintained within major versions
- **Changes**: Breaking changes increment major version

### Version Information

Get server version information:

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "client-name",
      "version": "1.0.0"
    }
  },
  "id": 1
}
```

Response includes server information:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "serverInfo": {
      "name": "PyPI MCP Server",
      "version": "0.1.0"
    }
  },
  "id": 1
}
```

## Performance Characteristics

### Response Times

Typical response times (with cache):

| Operation        | Cold Cache | Warm Cache |
| ---------------- | ---------- | ---------- |
| Package Info     | 200-500ms  | 1-5ms      |
| Package Versions | 300-800ms  | 1-5ms      |
| Search           | 500-1000ms | 1-5ms      |
| Dependencies     | 200-500ms  | 1-5ms      |
| Vulnerabilities  | 300-700ms  | 1-5ms      |

### Throughput

- **STDIO Transport**: ~100 requests/second
- **HTTP Transport**: ~200 requests/second (concurrent)
- **Rate Limited**: Configurable (default: 10 req/sec)

### Resource Usage

- **Memory**: 50-200 MB (depending on cache size)
- **CPU**: Low (mostly I/O bound)
- **Network**: Depends on cache hit rate

## Client Libraries

### Official Clients

Currently, no official client libraries are provided. The server uses standard JSON-RPC 2.0 protocol.

### Community Clients

Examples available for:

- Python (using `httpx` or subprocess)
- JavaScript/Node.js (using `axios`)
- cURL (command-line examples)

### Building Custom Clients

Requirements for custom clients:

1. **JSON-RPC 2.0**: Support JSON-RPC 2.0 protocol
2. **MCP Protocol**: Implement MCP initialization
3. **Transport**: Support STDIO or HTTP transport
4. **Error Handling**: Handle error responses appropriately

## Next Steps

- [Tools Reference](tools.md) - Detailed tool documentation
- [Resources Reference](resources.md) - Resource documentation
- [Prompts Reference](prompts.md) - Prompt templates
- [Data Models](data-models.md) - Complete data model reference
