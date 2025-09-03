# Tools Reference

Complete reference for all PyPI MCP Server tools with parameters, return values, and examples.

## Overview

The PyPI MCP Server provides 10 tools for comprehensive PyPI package management and analysis. All tools follow the JSON-RPC 2.0 protocol and return structured data.

## Package Information Tools

### get_package_info

Get detailed information about a PyPI package.

#### Parameters

| Parameter       | Type      | Required | Default | Description                                |
| --------------- | --------- | -------- | ------- | ------------------------------------------ |
| `package_name`  | `string`  | Yes      | -       | Name of the package to look up             |
| `version`       | `string`  | No       | `null`  | Specific version (latest if not specified) |
| `include_files` | `boolean` | No       | `false` | Whether to include file information        |

#### Returns

```json
{
  "name": "requests",
  "version": "2.31.0",
  "summary": "Python HTTP for Humans.",
  "description": "Requests is a simple, yet elegant HTTP library...",
  "author": "Kenneth Reitz",
  "author_email": "me@kennethreitz.org",
  "maintainer": "Kenneth Reitz",
  "maintainer_email": "me@kennethreitz.org",
  "license": "Apache 2.0",
  "home_page": "https://requests.readthedocs.io",
  "project_urls": {
    "Homepage": "https://requests.readthedocs.io",
    "Repository": "https://github.com/psf/requests",
    "Documentation": "https://requests.readthedocs.io"
  },
  "classifiers": [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3"
  ],
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
  "yanked_reason": null,
  "package_url": "https://pypi.org/project/requests/",
  "project_url": "https://pypi.org/project/requests/",
  "release_url": "https://pypi.org/project/requests/2.31.0/",
  "version_type": "stable",
  "vulnerabilities": []
}
```

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_info",
      "arguments": {
        "package_name": "requests",
        "include_files": true
      }
    }
    `

=== "Natural Language"
`    Get detailed information about the requests package including files
   `

#### Error Cases

- **Package not found**: Returns error if package doesn't exist
- **Invalid version**: Returns error if version format is invalid
- **Network error**: Returns error if PyPI is unreachable

### get_package_versions

Get all available versions of a package.

#### Parameters

| Parameter             | Type      | Required | Default | Description                                       |
| --------------------- | --------- | -------- | ------- | ------------------------------------------------- |
| `package_name`        | `string`  | Yes      | -       | Name of the package                               |
| `limit`               | `integer` | No       | `null`  | Maximum versions to return (all if not specified) |
| `include_prereleases` | `boolean` | No       | `true`  | Whether to include pre-release versions           |

#### Returns

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
    },
    {
      "version": "4.2.0rc1",
      "type": "pre-release",
      "is_latest": false
    }
  ]
}
```

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_versions",
      "arguments": {
        "package_name": "django",
        "limit": 20,
        "include_prereleases": false
      }
    }
    `

=== "Natural Language"
`    List the latest 20 stable versions of Django
   `

## Discovery Tools

### search_packages

Search for packages by name or keywords.

#### Parameters

| Parameter             | Type      | Required | Default | Description                             |
| --------------------- | --------- | -------- | ------- | --------------------------------------- |
| `query`               | `string`  | Yes      | -       | Search query (package name or keywords) |
| `limit`               | `integer` | No       | `10`    | Maximum results to return (1-100)       |
| `include_description` | `boolean` | No       | `false` | Whether to include package descriptions |

#### Returns

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

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "search_packages",
      "arguments": {
        "query": "web framework",
        "limit": 5,
        "include_description": true
      }
    }
    `

=== "Natural Language"
`    Search for Python web framework packages
   `

## Analysis Tools

### compare_versions

Compare two versions of a package.

#### Parameters

| Parameter      | Type     | Required | Default | Description               |
| -------------- | -------- | -------- | ------- | ------------------------- |
| `package_name` | `string` | Yes      | -       | Name of the package       |
| `version1`     | `string` | Yes      | -       | First version to compare  |
| `version2`     | `string` | Yes      | -       | Second version to compare |

#### Returns

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

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "compare_versions",
      "arguments": {
        "package_name": "django",
        "version1": "4.1.0",
        "version2": "4.2.0"
      }
    }
    `

=== "Natural Language"
`    Compare Django version 4.1.0 vs 4.2.0
   `

### check_compatibility

Check Python version compatibility for a package.

#### Parameters

| Parameter        | Type     | Required | Default  | Description                               |
| ---------------- | -------- | -------- | -------- | ----------------------------------------- |
| `package_name`   | `string` | Yes      | -        | Name of the package                       |
| `version`        | `string` | No       | `null`   | Package version (latest if not specified) |
| `python_version` | `string` | No       | `"3.11"` | Python version to check against           |

#### Returns

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

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "check_compatibility",
      "arguments": {
        "package_name": "numpy",
        "version": "1.24.0",
        "python_version": "3.11"
      }
    }
    `

=== "Natural Language"
`    Check if numpy 1.24.0 is compatible with Python 3.11
   `

### get_package_health

Assess package health and maintenance status.

#### Parameters

| Parameter      | Type     | Required | Default | Description                               |
| -------------- | -------- | -------- | ------- | ----------------------------------------- |
| `package_name` | `string` | Yes      | -       | Name of the package                       |
| `version`      | `string` | No       | `null`  | Package version (latest if not specified) |

#### Returns

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

#### Health Status Values

| Status      | Score Range | Description                              |
| ----------- | ----------- | ---------------------------------------- |
| `excellent` | 80-100      | Well-maintained, secure package          |
| `good`      | 60-79       | Generally good package with minor issues |
| `fair`      | 40-59       | Some concerns, use with caution          |
| `poor`      | 0-39        | Significant issues, avoid if possible    |

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_health",
      "arguments": {
        "package_name": "requests"
      }
    }
    `

=== "Natural Language"
`    Analyze the health of the requests package
   `

## Dependency Tools

### get_dependencies

Get package dependencies with detailed analysis.

#### Parameters

| Parameter        | Type      | Required | Default | Description                               |
| ---------------- | --------- | -------- | ------- | ----------------------------------------- |
| `package_name`   | `string`  | Yes      | -       | Name of the package                       |
| `version`        | `string`  | No       | `null`  | Package version (latest if not specified) |
| `include_extras` | `boolean` | No       | `false` | Whether to include optional dependencies  |

#### Returns

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
    },
    {
      "name": "pydantic",
      "version_spec": ">=1.7.4,!=1.7.5,!=1.8.0,<3.0.0",
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

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "get_dependencies",
      "arguments": {
        "package_name": "fastapi",
        "include_extras": true
      }
    }
    `

=== "Natural Language"
`    What are the dependencies of FastAPI including optional extras?
   `

## Security Tools

### check_vulnerabilities

Check for known security vulnerabilities in a package.

#### Parameters

| Parameter      | Type     | Required | Default | Description                               |
| -------------- | -------- | -------- | ------- | ----------------------------------------- |
| `package_name` | `string` | Yes      | -       | Name of the package                       |
| `version`      | `string` | No       | `null`  | Package version (latest if not specified) |

#### Returns

```json
{
  "package_name": "django",
  "package_version": "3.2.0",
  "vulnerability_count": 2,
  "has_vulnerabilities": true,
  "vulnerabilities": [
    {
      "id": "GHSA-2hrw-hx67-34x6",
      "source": "GitHub Advisory Database",
      "summary": "Django vulnerable to potential denial of service",
      "details": "An issue was discovered in Django 2.2 before 2.2.28...",
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

#### Severity Levels

| Severity | Description                                   |
| -------- | --------------------------------------------- |
| `high`   | Critical vulnerabilities with CVE assignments |
| `medium` | Moderate security issues                      |
| `low`    | Minor security concerns                       |

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "check_vulnerabilities",
      "arguments": {
        "package_name": "django",
        "version": "3.2.0"
      }
    }
    `

=== "Natural Language"
`    Check if Django 3.2.0 has any security vulnerabilities
   `

## Statistics Tools

### get_pypi_stats

Get overall PyPI statistics and top packages.

#### Parameters

None

#### Returns

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
    },
    {
      "name": "torch",
      "size": 419430400,
      "size_formatted": "400.0 MB"
    }
  ],
  "last_updated": "real-time"
}
```

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "get_pypi_stats"
    }
    `

=== "Natural Language"
`    What are the current PyPI statistics and largest packages?
   `

## System Tools

### get_cache_info

Get information about the server's cache status.

#### Parameters

None

#### Returns

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

#### Cache Metrics

| Metric         | Description                    |
| -------------- | ------------------------------ |
| `hits`         | Number of cache hits           |
| `misses`       | Number of cache misses         |
| `hit_rate`     | Cache hit rate (0.0-1.0)       |
| `current_size` | Current number of cached items |
| `max_size`     | Maximum cache capacity         |

#### Example Usage

=== "MCP Tool Call"
`json
    {
      "tool": "get_cache_info"
    }
    `

=== "Natural Language"
`    Show me the current cache statistics
   `

## Error Handling

### Common Error Responses

#### Package Not Found

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

#### Invalid Parameters

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "parameter": "package_name",
      "value": "",
      "details": "Package name cannot be empty"
    }
  },
  "id": 1
}
```

#### Rate Limit Exceeded

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

## Best Practices

### Parameter Validation

- **Package Names**: Use lowercase, hyphens/underscores allowed
- **Versions**: Follow PEP 440 version specification
- **Limits**: Keep search limits reasonable (≤100)

### Error Handling

- **Check Error Codes**: Handle specific error codes appropriately
- **Retry Logic**: Implement exponential backoff for transient errors
- **Fallback**: Provide fallback behavior for missing packages

### Performance

- **Use Caching**: Leverage server-side caching for better performance
- **Batch Requests**: Group related requests when possible
- **Appropriate Limits**: Use reasonable limits for list operations

### Security

- **Input Validation**: Validate all inputs before sending requests
- **Rate Limiting**: Respect rate limits to avoid being blocked
- **Error Information**: Don't expose sensitive information in error handling

## Next Steps

- [Resources Reference](resources.md) - Static and dynamic resources
- [Prompts Reference](prompts.md) - AI analysis templates
- [Data Models](data-models.md) - Complete data structure reference
