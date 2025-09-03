# Resources Reference

Complete reference for PyPI MCP Server resources that provide static and dynamic content.

## Overview

Resources in the PyPI MCP Server provide access to static or dynamic content that can be read by MCP clients. Unlike tools, resources are accessed via URI patterns and return text content.

The server provides 2 resources:

1. **PyPI Stats Overview** - General PyPI statistics
2. **Package Resource** - Individual package metadata

## Resource Access

### Protocol

Resources are accessed using the `resources/read` method:

```json
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": {
    "uri": "pypi://stats/overview"
  },
  "id": 1
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": {
    "contents": [
      {
        "uri": "pypi://stats/overview",
        "mimeType": "text/plain",
        "text": "PyPI Statistics Overview:\n- Total packages size: 14.6 GB\n..."
      }
    ]
  },
  "id": 1
}
```

## Available Resources

### PyPI Stats Overview

Provides a text summary of PyPI statistics.

#### URI Pattern

```
pypi://stats/overview
```

#### Description

Returns a formatted text overview of PyPI statistics including:

- Total package size across PyPI
- Number of top packages tracked
- Data source information
- Last updated timestamp

#### Example Content

```
PyPI Statistics Overview:
- Total packages size: 14.6 GB
- Top packages tracked: 20
- Data source: PyPI API
- Last updated: Real-time
```

#### Usage Examples

=== "MCP Resource Read"
`json
    {
      "jsonrpc": "2.0",
      "method": "resources/read",
      "params": {
        "uri": "pypi://stats/overview"
      },
      "id": 1
    }
    `

=== "Natural Language"
`    Show me the PyPI statistics overview resource
   `

#### Error Cases

- **Service Unavailable**: Returns error message if PyPI stats are unavailable
- **Network Error**: Returns error if unable to fetch current statistics

### Package Resource

Provides metadata for a specific package as formatted text.

#### URI Pattern

```
pypi://package/{package_name}
```

Where `{package_name}` is the name of the PyPI package.

#### Description

Returns a formatted text summary of package metadata including:

- Package name and current version
- Summary description
- Author information
- License information
- Homepage URL
- Number of dependencies
- Number of known vulnerabilities

#### Example Content

```
Package: requests
Version: 2.31.0
Summary: Python HTTP for Humans.
Author: Kenneth Reitz
License: Apache 2.0
Homepage: https://requests.readthedocs.io
Dependencies: 5
Vulnerabilities: 0
```

#### Usage Examples

=== "MCP Resource Read"
`json
    {
      "jsonrpc": "2.0",
      "method": "resources/read",
      "params": {
        "uri": "pypi://package/requests"
      },
      "id": 1
    }
    `

=== "Natural Language"
`    Show me the package resource for requests
   `

#### URI Examples

- `pypi://package/requests` - Requests HTTP library
- `pypi://package/django` - Django web framework
- `pypi://package/numpy` - NumPy scientific computing
- `pypi://package/fastapi` - FastAPI web framework

#### Error Cases

- **Package Not Found**: Returns error message if package doesn't exist on PyPI
- **Invalid Package Name**: Returns error for malformed package names

## Resource Listing

### List Available Resources

Get a list of all available resources:

```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "params": {},
  "id": 1
}
```

#### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "resources": [
      {
        "uri": "pypi://stats/overview",
        "name": "PyPI Statistics Overview",
        "description": "Provides PyPI statistics overview",
        "mimeType": "text/plain"
      },
      {
        "uri": "pypi://package/{package_name}",
        "name": "Package Metadata",
        "description": "Provides package metadata as a resource",
        "mimeType": "text/plain"
      }
    ]
  },
  "id": 1
}
```

## Resource Templates

### URI Templates

Resources support URI templates for dynamic content:

| Template                        | Description      | Example                   |
| ------------------------------- | ---------------- | ------------------------- |
| `pypi://package/{package_name}` | Package metadata | `pypi://package/requests` |

### Template Variables

| Variable       | Type     | Description       | Validation                 |
| -------------- | -------- | ----------------- | -------------------------- |
| `package_name` | `string` | PyPI package name | Must be valid package name |

## Content Types

### MIME Types

All resources return `text/plain` content type with UTF-8 encoding.

### Content Format

Resources return human-readable text formatted for:

- **Console Display**: Suitable for terminal output
- **Log Files**: Structured for logging systems
- **Documentation**: Readable in documentation contexts

## Caching Behavior

### Cache Policy

Resources are cached using the same policy as tools:

- **TTL**: Same as configured cache TTL (default: 5 minutes)
- **Invalidation**: Automatic expiration and LRU eviction
- **Consistency**: Consistent with tool responses

### Cache Keys

Resource cache keys follow the pattern:

```
resource:{uri_path}
```

Examples:

- `resource:stats/overview`
- `resource:package/requests`

## Error Handling

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Resource not found",
    "data": {
      "uri": "pypi://package/nonexistent",
      "details": "Package 'nonexistent' not found on PyPI"
    }
  },
  "id": 1
}
```

### Common Errors

| Error Code | Description        | Example                    |
| ---------- | ------------------ | -------------------------- |
| `-32000`   | Resource not found | Invalid package name       |
| `-32602`   | Invalid URI        | Malformed URI pattern      |
| `-32603`   | Internal error     | Server error fetching data |

## Performance Characteristics

### Response Times

| Resource         | Cold Cache | Warm Cache |
| ---------------- | ---------- | ---------- |
| Stats Overview   | 300-800ms  | 1-5ms      |
| Package Resource | 200-500ms  | 1-5ms      |

### Content Size

| Resource         | Typical Size  |
| ---------------- | ------------- |
| Stats Overview   | 200-500 bytes |
| Package Resource | 300-800 bytes |

## Use Cases

### Documentation Generation

Resources can be used to generate documentation:

```python
async def generate_package_docs(packages):
    """Generate documentation from package resources."""
    docs = []

    for package in packages:
        uri = f"pypi://package/{package}"
        resource = await client.read_resource(uri)
        docs.append(resource['text'])

    return '\n\n'.join(docs)
```

### Status Monitoring

Monitor PyPI status using the stats resource:

```python
async def check_pypi_status():
    """Check PyPI status from stats resource."""
    try:
        stats = await client.read_resource("pypi://stats/overview")
        return "available" if "Total packages size" in stats['text'] else "degraded"
    except Exception:
        return "unavailable"
```

### Report Generation

Generate reports using resource content:

```python
async def generate_package_report(package_names):
    """Generate a package report."""
    report = ["# Package Report\n"]

    # Add stats overview
    stats = await client.read_resource("pypi://stats/overview")
    report.append("## PyPI Overview")
    report.append(stats['text'])
    report.append("")

    # Add package details
    report.append("## Package Details")
    for package in package_names:
        uri = f"pypi://package/{package}"
        try:
            resource = await client.read_resource(uri)
            report.append(f"### {package}")
            report.append(resource['text'])
            report.append("")
        except Exception as e:
            report.append(f"### {package}")
            report.append(f"Error: {e}")
            report.append("")

    return '\n'.join(report)
```

## Best Practices

### URI Construction

- **Validate Package Names**: Ensure package names are valid before constructing URIs
- **URL Encoding**: Properly encode special characters in package names
- **Case Sensitivity**: Use lowercase package names for consistency

### Error Handling

- **Graceful Degradation**: Handle missing resources gracefully
- **Retry Logic**: Implement retry for transient failures
- **Fallback Content**: Provide fallback content when resources are unavailable

### Performance

- **Cache Awareness**: Leverage caching for frequently accessed resources
- **Batch Processing**: Process multiple resources efficiently
- **Content Parsing**: Parse resource content appropriately for your use case

## Integration Examples

### Claude Desktop

Resources can be referenced in Claude Desktop conversations:

```
Please read the PyPI stats overview resource and summarize the current state of PyPI.
```

### Custom Applications

```python
class PyPIResourceClient:
    def __init__(self, mcp_client):
        self.client = mcp_client

    async def get_stats_overview(self):
        """Get PyPI statistics overview."""
        resource = await self.client.read_resource("pypi://stats/overview")
        return resource['text']

    async def get_package_summary(self, package_name):
        """Get package summary."""
        uri = f"pypi://package/{package_name}"
        resource = await self.client.read_resource(uri)
        return resource['text']

    async def get_multiple_packages(self, package_names):
        """Get summaries for multiple packages."""
        results = {}
        for package in package_names:
            try:
                summary = await self.get_package_summary(package)
                results[package] = summary
            except Exception as e:
                results[package] = f"Error: {e}"
        return results
```

## Next Steps

- [Prompts Reference](prompts.md) - AI analysis templates
- [Data Models](data-models.md) - Complete data structure reference
- [Tools Reference](tools.md) - Interactive tools for data manipulation
