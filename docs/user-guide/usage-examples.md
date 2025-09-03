# Usage Examples

Practical examples demonstrating how to use the PyPI MCP Server effectively.

## Basic Package Information

### Get Package Details

Get comprehensive information about a package:

=== "Natural Language (Claude)"
`    What is the latest version of FastAPI and what are its dependencies?
   `

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_info",
      "arguments": {
        "package_name": "fastapi",
        "include_files": true
      }
    }
    `

=== "Python Client"
```python # Using the programmatic client
from pypi_mcp.client import client

    async with client:
        package_info = await client.get_package_info("fastapi")
        print(f"Package: {package_info.name}")
        print(f"Version: {package_info.version}")
        print(f"Summary: {package_info.summary}")
        print(f"Dependencies: {len(package_info.requires_dist)}")
    ```

### Get Specific Version Information

Query information for a specific package version:

=== "Natural Language (Claude)"
`    Show me details about Django version 4.2.0, including its files
   `

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_info",
      "arguments": {
        "package_name": "django",
        "version": "4.2.0",
        "include_files": true
      }
    }
    `

## Package Search and Discovery

### Search by Name

Find packages by name or keywords:

=== "Natural Language (Claude)"
`    Find Python packages related to web frameworks
   `

=== "MCP Tool Call"
`json
    {
      "tool": "search_packages",
      "arguments": {
        "query": "web framework",
        "limit": 10,
        "include_description": true
      }
    }
    `

=== "Python Client"
`python
    async with client:
        # Search for web frameworks
        results = await client.search_packages("web framework", limit=5)
        for result in results:
            print(f"- {result['name']}: {result['summary']}")
    `

### Version Listing

Get all available versions of a package:

=== "Natural Language (Claude)"
`    List all stable versions of numpy, excluding pre-releases
   `

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_versions",
      "arguments": {
        "package_name": "numpy",
        "limit": 20,
        "include_prereleases": false
      }
    }
    `

## Security Analysis

### Vulnerability Checking

Check for known security vulnerabilities:

=== "Natural Language (Claude)"
`    Check if Django 3.2.0 has any known security vulnerabilities
   `

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

=== "Python Client"
```python
async with client:
vuln_check = await client.check_vulnerabilities("django", "3.2.0")

        if vuln_check["has_vulnerabilities"]:
            print(f"⚠️ Found {vuln_check['vulnerability_count']} vulnerabilities:")
            for vuln in vuln_check["vulnerabilities"]:
                print(f"- {vuln['id']}: {vuln['summary']}")
                if vuln["fixed_in"]:
                    print(f"  Fixed in: {', '.join(vuln['fixed_in'])}")
        else:
            print("✅ No known vulnerabilities")
    ```

### Package Health Assessment

Assess overall package health and maintenance:

=== "Natural Language (Claude)"
`    Analyze the health and maintenance status of the requests package
   `

=== "MCP Tool Call"
`json
    {
      "tool": "get_package_health",
      "arguments": {
        "package_name": "requests"
      }
    }
    `

## Dependency Analysis

### Basic Dependency Information

Analyze package dependencies:

=== "Natural Language (Claude)"
`    What are the runtime dependencies of FastAPI, including optional extras?
   `

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

=== "Python Client"
```python
async with client:
deps = await client.get_dependencies("fastapi", include_extras=True)

        print(f"Runtime dependencies: {len(deps['runtime_dependencies'])}")
        for dep in deps['runtime_dependencies']:
            print(f"- {dep['name']} {dep['version_spec']}")

        if deps['optional_dependencies']:
            print("\nOptional dependencies:")
            for extra, deps_list in deps['optional_dependencies'].items():
                print(f"  {extra}: {len(deps_list)} packages")
    ```

### Compatibility Checking

Check Python version compatibility:

=== "Natural Language (Claude)"
`    Is numpy version 1.24.0 compatible with Python 3.11?
   `

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

## Version Comparison

### Compare Package Versions

Compare two versions of the same package:

=== "Natural Language (Claude)"
`    Compare Django 4.1.0 vs 4.2.0 - what are the differences?
   `

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

=== "Python Client"
```python
async with client:
comparison = await client.compare_versions("django", "4.1.0", "4.2.0")

        newer = comparison["comparison"]["newer_version"]
        print(f"Newer version: {newer}")

        v1 = comparison["version1"]
        v2 = comparison["version2"]
        print(f"Version 1: {v1['version']} ({v1['type']})")
        print(f"Version 2: {v2['version']} ({v2['type']})")
        print(f"Dependencies: {v1['dependencies_count']} vs {v2['dependencies_count']}")
    ```

## Statistics and Analytics

### PyPI Statistics

Get overall PyPI statistics:

=== "Natural Language (Claude)"
`    What are the current PyPI statistics and top largest packages?
   `

=== "MCP Tool Call"
`json
    {
      "tool": "get_pypi_stats"
    }
    `

=== "Python Client"
```python
async with client:
stats = await client.get_pypi_stats()

        print(f"Total PyPI size: {stats['total_size_formatted']}")
        print("Top 5 largest packages:")

        for i, package in enumerate(stats['top_packages'][:5]):
            print(f"  {i+1}. {package['name']}: {package['size_formatted']}")
    ```

### Cache Information

Monitor server cache performance:

=== "MCP Tool Call"
`json
    {
      "tool": "get_cache_info"
    }
    `

=== "Python Client"
```python
async with client:
cache_info = await client.get_cache_info()

        stats = cache_info['cache_stats']
        print(f"Cache hit rate: {stats['hit_rate']:.2%}")
        print(f"Cache size: {stats['current_size']}/{stats['max_size']}")
        print(f"TTL: {cache_info['cache_ttl_seconds']} seconds")
    ```

## Advanced Usage Patterns

### Batch Analysis

Analyze multiple packages efficiently:

```python
async def analyze_packages(package_names):
    """Analyze multiple packages in batch."""
    results = {}

    async with client:
        for package_name in package_names:
            try:
                # Get basic info
                info = await client.get_package_info(package_name)

                # Check vulnerabilities
                vulns = await client.check_vulnerabilities(package_name)

                # Get health assessment
                health = await client.get_package_health(package_name)

                results[package_name] = {
                    'version': info.version,
                    'summary': info.summary,
                    'vulnerabilities': len(vulns['vulnerabilities']),
                    'health_score': health['health_score'],
                    'health_status': health['health_status']
                }

            except Exception as e:
                results[package_name] = {'error': str(e)}

    return results

# Usage
packages = ['requests', 'django', 'fastapi', 'flask', 'numpy']
analysis = await analyze_packages(packages)

for package, data in analysis.items():
    if 'error' in data:
        print(f"{package}: Error - {data['error']}")
    else:
        print(f"{package} v{data['version']}: "
              f"Health {data['health_status']} ({data['health_score']}), "
              f"{data['vulnerabilities']} vulnerabilities")
```

### Dependency Tree Analysis

Build a dependency tree for a package:

```python
async def build_dependency_tree(package_name, max_depth=2, current_depth=0):
    """Build a dependency tree for a package."""
    if current_depth >= max_depth:
        return {}

    async with client:
        try:
            deps = await client.get_dependencies(package_name)
            tree = {
                'package': package_name,
                'dependencies': {}
            }

            for dep in deps['runtime_dependencies']:
                dep_name = dep['name']
                tree['dependencies'][dep_name] = await build_dependency_tree(
                    dep_name, max_depth, current_depth + 1
                )

            return tree

        except Exception as e:
            return {'error': str(e)}

# Usage
tree = await build_dependency_tree('fastapi', max_depth=2)
print(json.dumps(tree, indent=2))
```

### Security Audit

Perform a comprehensive security audit:

```python
async def security_audit(package_name, version=None):
    """Perform comprehensive security audit of a package."""
    async with client:
        # Get package info
        info = await client.get_package_info(package_name, version)

        # Check vulnerabilities
        vulns = await client.check_vulnerabilities(package_name, version)

        # Get dependencies
        deps = await client.get_dependencies(package_name, version)

        # Check dependency vulnerabilities
        dep_vulns = {}
        for dep in deps['runtime_dependencies']:
            dep_name = dep['name']
            try:
                dep_vuln = await client.check_vulnerabilities(dep_name)
                if dep_vuln['has_vulnerabilities']:
                    dep_vulns[dep_name] = dep_vuln['vulnerability_count']
            except:
                pass

        # Generate report
        report = {
            'package': f"{info.name} v{info.version}",
            'direct_vulnerabilities': vulns['vulnerability_count'],
            'dependency_vulnerabilities': sum(dep_vulns.values()),
            'vulnerable_dependencies': list(dep_vulns.keys()),
            'total_dependencies': len(deps['runtime_dependencies']),
            'security_status': 'SECURE' if vulns['vulnerability_count'] == 0 and len(dep_vulns) == 0 else 'VULNERABLE'
        }

        return report

# Usage
audit = await security_audit('django', '4.2.0')
print(f"Security audit for {audit['package']}:")
print(f"Status: {audit['security_status']}")
print(f"Direct vulnerabilities: {audit['direct_vulnerabilities']}")
print(f"Vulnerable dependencies: {audit['dependency_vulnerabilities']}")
```

## Integration Examples

### Claude Desktop Queries

Natural language queries you can use with Claude Desktop:

!!! example "Package Information" - "What is the latest version of FastAPI and what are its dependencies?" - "Show me information about the requests package" - "What Python versions does Django 4.2 support?" - "Get details about numpy version 1.24.0 including file information"

!!! example "Security Analysis" - "Check if Django 3.2.0 has any known vulnerabilities" - "Are there any security issues with requests version 2.25.0?" - "Perform a security audit of the Flask package" - "What's the security status of the latest numpy version?"

!!! example "Comparison and Analysis" - "Compare FastAPI vs Flask for building web APIs" - "What are the differences between Django 4.1 and 4.2?" - "Should I use requests or httpx for HTTP client?" - "Analyze the health of the pandas package"

!!! example "Dependency Management" - "What are the dependencies of scikit-learn?" - "Is numpy 1.24.0 compatible with Python 3.11?" - "Show me the optional dependencies for FastAPI" - "What packages depend on requests?"

### HTTP API Integration

Example HTTP requests for programmatic access:

```bash
# Get package information
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_package_info",
      "arguments": {"package_name": "requests"}
    },
    "id": 1
  }'

# Check vulnerabilities
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "check_vulnerabilities",
      "arguments": {"package_name": "django", "version": "3.2.0"}
    },
    "id": 2
  }'
```

## Best Practices

### Performance Optimization

1. **Use Caching Effectively**:

   ```python
   # Cache frequently accessed packages
   popular_packages = ['requests', 'numpy', 'pandas', 'django']
   for package in popular_packages:
       await client.get_package_info(package)  # Cached for subsequent calls
   ```

2. **Batch Related Requests**:

   ```python
   # Group related operations
   package_name = "fastapi"
   info, deps, vulns = await asyncio.gather(
       client.get_package_info(package_name),
       client.get_dependencies(package_name),
       client.check_vulnerabilities(package_name)
   )
   ```

3. **Handle Rate Limits**:

   ```python
   import asyncio

   async def rate_limited_requests(packages):
       results = []
       for package in packages:
           result = await client.get_package_info(package)
           results.append(result)
           await asyncio.sleep(0.1)  # Respect rate limits
       return results
   ```

### Error Handling

```python
from pypi_mcp.exceptions import PackageNotFoundError, PyPIMCPError

async def safe_package_lookup(package_name):
    try:
        return await client.get_package_info(package_name)
    except PackageNotFoundError:
        print(f"Package '{package_name}' not found")
        return None
    except PyPIMCPError as e:
        print(f"API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Next Steps

- [Configuration Guide](configuration.md) - Optimize server settings
- [API Reference](../api-reference/tools.md) - Explore all available tools
- [Caching Guide](caching.md) - Understand caching behavior
