# Debugging Guide

Advanced debugging techniques and tools for the PyPI MCP Server.

## Debug Configuration

### Enable Debug Logging

```bash
# Environment variable
export PYPI_MCP_LOG_LEVEL=DEBUG

# Command line
pypi-mcp --log-level DEBUG

# Programmatic
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug Output Example

```
2025-01-15 10:30:15 - pypi_mcp.server - DEBUG - Starting PyPI MCP Server
2025-01-15 10:30:15 - pypi_mcp.client - DEBUG - Initializing PyPI client
2025-01-15 10:30:15 - pypi_mcp.cache - DEBUG - Cache initialized: TTL=300, max_size=1000
2025-01-15 10:30:16 - pypi_mcp.server - DEBUG - Tool called: get_package_info(package_name='requests')
2025-01-15 10:30:16 - pypi_mcp.cache - DEBUG - Cache miss for key: package:requests:latest
2025-01-15 10:30:16 - pypi_mcp.client - DEBUG - Making request to: https://pypi.org/pypi/requests/json
2025-01-15 10:30:16 - pypi_mcp.client - DEBUG - Response received: 200 OK
2025-01-15 10:30:16 - pypi_mcp.cache - DEBUG - Cached result for key: package:requests:latest
2025-01-15 10:30:16 - pypi_mcp.server - DEBUG - Tool completed successfully
```

## Debugging Tools

### 1. Interactive Debugging

#### Python Debugger (pdb)

```python
import pdb
import asyncio
from pypi_mcp.client import client

async def debug_package_info():
    """Debug package info retrieval."""
    async with client:
        pdb.set_trace()  # Debugger breakpoint
        result = await client.get_package_info("requests")
        return result

# Run with debugger
asyncio.run(debug_package_info())
```

#### IPython Debugger

```python
import IPython
import asyncio
from pypi_mcp.client import client

async def debug_with_ipython():
    """Debug with IPython."""
    async with client:
        IPython.embed()  # Interactive IPython session
        result = await client.get_package_info("requests")
        return result

asyncio.run(debug_with_ipython())
```

### 2. Logging and Tracing

#### Custom Debug Logger

```python
import logging
import functools
import time

def debug_trace(func):
    """Decorator to trace function calls."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = time.time()

        logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")

        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"Exiting {func.__name__} after {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Error in {func.__name__} after {duration:.3f}s: {e}")
            raise

    return wrapper

# Usage
@debug_trace
async def get_package_info_traced(package_name):
    """Traced version of get_package_info."""
    async with client:
        return await client.get_package_info(package_name)
```

#### Request/Response Logging

```python
import httpx
import logging

class DebugTransport(httpx.AsyncHTTPTransport):
    """HTTP transport with debug logging."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    async def arequest(self, request):
        """Log request and response."""
        self.logger.debug(f"Request: {request.method} {request.url}")
        self.logger.debug(f"Headers: {dict(request.headers)}")

        response = await super().arequest(request)

        self.logger.debug(f"Response: {response.status_code}")
        self.logger.debug(f"Response headers: {dict(response.headers)}")

        return response

# Use debug transport
async def debug_http_requests():
    """Debug HTTP requests."""
    transport = DebugTransport()
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get("https://pypi.org/pypi/requests/json")
        return response.json()
```

### 3. Performance Debugging

#### Response Time Analysis

```python
import time
import statistics
import asyncio
from pypi_mcp.client import client

async def analyze_response_times():
    """Analyze response time patterns."""
    times = []

    async with client:
        for i in range(20):
            start = time.time()
            await client.get_package_info("requests")
            duration = time.time() - start
            times.append(duration)
            print(f"Request {i+1}: {duration:.3f}s")

    print(f"\nStatistics:")
    print(f"Mean: {statistics.mean(times):.3f}s")
    print(f"Median: {statistics.median(times):.3f}s")
    print(f"Std Dev: {statistics.stdev(times):.3f}s")
    print(f"Min: {min(times):.3f}s")
    print(f"Max: {max(times):.3f}s")

asyncio.run(analyze_response_times())
```

#### Memory Usage Tracking

```python
import psutil
import os
import asyncio
import time
from pypi_mcp.client import client

async def track_memory_usage():
    """Track memory usage over time."""
    process = psutil.Process(os.getpid())
    memory_samples = []

    async with client:
        for i in range(10):
            # Take memory sample
            memory_mb = process.memory_info().rss / 1024 / 1024
            memory_samples.append(memory_mb)
            print(f"Sample {i+1}: {memory_mb:.1f} MB")

            # Perform operation
            await client.get_package_info(f"package-{i}")

            # Wait between samples
            await asyncio.sleep(1)

    print(f"\nMemory growth: {memory_samples[-1] - memory_samples[0]:.1f} MB")

asyncio.run(track_memory_usage())
```

## Debugging Specific Issues

### 1. Cache Debugging

#### Cache State Inspection

```python
import asyncio
from pypi_mcp.cache import get_cache_stats

async def debug_cache_state():
    """Debug cache state and behavior."""
    # Get initial stats
    initial_stats = await get_cache_stats()
    print(f"Initial cache state: {initial_stats}")

    # Perform operations
    async with client:
        await client.get_package_info("requests")  # Should be cache miss
        await client.get_package_info("requests")  # Should be cache hit

    # Get final stats
    final_stats = await get_cache_stats()
    print(f"Final cache state: {final_stats}")

    # Calculate changes
    hit_change = final_stats['hits'] - initial_stats['hits']
    miss_change = final_stats['misses'] - initial_stats['misses']

    print(f"Cache hits added: {hit_change}")
    print(f"Cache misses added: {miss_change}")

asyncio.run(debug_cache_state())
```

#### Cache Key Analysis

```python
def debug_cache_keys():
    """Debug cache key generation."""
    from pypi_mcp.utils import generate_cache_key

    # Test different cache keys
    test_cases = [
        ("get_package_info", {"package_name": "requests"}),
        ("get_package_info", {"package_name": "requests", "version": "2.31.0"}),
        ("search_packages", {"query": "web framework", "limit": 10}),
    ]

    for operation, params in test_cases:
        key = generate_cache_key(operation, params)
        print(f"Operation: {operation}")
        print(f"Params: {params}")
        print(f"Cache key: {key}")
        print()

debug_cache_keys()
```

### 2. Network Debugging

#### Connection Pool Analysis

```python
import httpx
import asyncio

async def debug_connection_pool():
    """Debug HTTP connection pool behavior."""

    class DebugClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.request_count = 0

        async def request(self, *args, **kwargs):
            self.request_count += 1
            print(f"Request #{self.request_count}: {args[0]} {args[1]}")

            # Check connection pool
            pool = self._transport._pool
            print(f"Pool connections: {len(pool._connections)}")

            return await super().request(*args, **kwargs)

    async with DebugClient() as client:
        # Make multiple requests
        for i in range(5):
            response = await client.get("https://pypi.org/pypi/requests/json")
            print(f"Response {i+1}: {response.status_code}")

asyncio.run(debug_connection_pool())
```

#### Rate Limiting Debug

```python
import time
import asyncio
from pypi_mcp.client import client

async def debug_rate_limiting():
    """Debug rate limiting behavior."""
    request_times = []

    async with client:
        for i in range(15):  # More than default rate limit
            start = time.time()
            try:
                await client.get_package_info("requests")
                request_times.append(time.time() - start)
                print(f"Request {i+1}: {request_times[-1]:.3f}s")
            except Exception as e:
                print(f"Request {i+1} failed: {e}")

    # Analyze timing patterns
    if len(request_times) > 1:
        intervals = [request_times[i] - request_times[i-1] for i in range(1, len(request_times))]
        print(f"Average interval: {sum(intervals)/len(intervals):.3f}s")

asyncio.run(debug_rate_limiting())
```

### 3. Error Debugging

#### Exception Tracing

```python
import traceback
import asyncio
from pypi_mcp.client import client

async def debug_exceptions():
    """Debug exception handling."""

    test_cases = [
        "requests",  # Valid package
        "nonexistent-package-12345",  # Invalid package
        "",  # Empty name
        "a" * 1000,  # Very long name
    ]

    async with client:
        for package_name in test_cases:
            try:
                print(f"Testing package: '{package_name}'")
                result = await client.get_package_info(package_name)
                print(f"Success: {result.name}")
            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}")
                print("Traceback:")
                traceback.print_exc()
            print("-" * 50)

asyncio.run(debug_exceptions())
```

#### Error Context Collection

```python
import sys
import traceback
from datetime import datetime

class ErrorCollector:
    """Collect detailed error information."""

    def __init__(self):
        self.errors = []

    def collect_error(self, error, context=None):
        """Collect error with context."""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'python_version': sys.version,
        }

        self.errors.append(error_info)
        return error_info

    def print_summary(self):
        """Print error summary."""
        print(f"Collected {len(self.errors)} errors:")
        for i, error in enumerate(self.errors):
            print(f"{i+1}. {error['error_type']}: {error['error_message']}")

# Usage
collector = ErrorCollector()

async def debug_with_collector():
    """Debug with error collection."""
    try:
        async with client:
            await client.get_package_info("nonexistent")
    except Exception as e:
        collector.collect_error(e, {'operation': 'get_package_info'})

    collector.print_summary()

asyncio.run(debug_with_collector())
```

## Advanced Debugging Techniques

### 1. Async Debugging

#### Async Stack Traces

```python
import asyncio
import traceback

async def debug_async_stack():
    """Debug async call stack."""

    async def level_3():
        # Simulate error
        raise ValueError("Test error in async function")

    async def level_2():
        await level_3()

    async def level_1():
        await level_2()

    try:
        await level_1()
    except Exception as e:
        print("Async stack trace:")
        traceback.print_exc()

        # Get current task
        task = asyncio.current_task()
        if task:
            print(f"Current task: {task}")
            print(f"Task stack: {task.get_stack()}")

asyncio.run(debug_async_stack())
```

#### Event Loop Debugging

```python
import asyncio
import time

def debug_event_loop():
    """Debug event loop behavior."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Enable debug mode
    loop.set_debug(True)

    async def slow_operation():
        """Simulate slow operation."""
        time.sleep(0.1)  # Blocking call (bad in async)
        return "done"

    async def main():
        await slow_operation()

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

debug_event_loop()
```

### 2. Protocol Debugging

#### MCP Message Tracing

```python
import json
import logging

class MCPMessageTracer:
    """Trace MCP protocol messages."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.message_count = 0

    def trace_request(self, message):
        """Trace outgoing request."""
        self.message_count += 1
        self.logger.debug(f"MCP Request #{self.message_count}:")
        self.logger.debug(json.dumps(message, indent=2))

    def trace_response(self, message):
        """Trace incoming response."""
        self.logger.debug(f"MCP Response #{self.message_count}:")
        self.logger.debug(json.dumps(message, indent=2))

# Usage
tracer = MCPMessageTracer()

def debug_mcp_messages():
    """Debug MCP message flow."""
    # Example request
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_package_info",
            "arguments": {"package_name": "requests"}
        },
        "id": 1
    }

    tracer.trace_request(request)

    # Example response
    response = {
        "jsonrpc": "2.0",
        "result": {
            "content": [{"type": "text", "text": "Package info..."}]
        },
        "id": 1
    }

    tracer.trace_response(response)

debug_mcp_messages()
```

### 3. Integration Debugging

#### Claude Desktop Integration Debug

```python
import subprocess
import json
import sys

def debug_claude_integration():
    """Debug Claude Desktop integration."""

    # Test server startup
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pypi_mcp", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✓ Server executable works")
        else:
            print(f"✗ Server executable failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("✗ Server startup timed out")
    except FileNotFoundError:
        print("✗ Server executable not found")

    # Test JSON-RPC communication
    test_message = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "debug-client", "version": "1.0.0"}
        },
        "id": 1
    }

    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pypi_mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send test message
        stdout, stderr = process.communicate(
            input=json.dumps(test_message) + "\n",
            timeout=10
        )

        if stdout:
            print("✓ Server responds to JSON-RPC")
            print(f"Response: {stdout}")
        else:
            print("✗ No response from server")
            print(f"Stderr: {stderr}")

    except Exception as e:
        print(f"✗ Communication test failed: {e}")

debug_claude_integration()
```

## Debugging Best Practices

### 1. Systematic Approach

1. **Reproduce the Issue**: Create minimal reproduction case
2. **Isolate Components**: Test individual components
3. **Add Logging**: Increase verbosity gradually
4. **Check Assumptions**: Verify expected behavior
5. **Document Findings**: Keep track of what you've tried

### 2. Debug Information Collection

```python
import sys
import platform
import pkg_resources

def collect_debug_info():
    """Collect system and environment information."""
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'architecture': platform.architecture(),
        'pypi_mcp_version': pkg_resources.get_distribution('pypi-mcp').version,
        'dependencies': {}
    }

    # Collect dependency versions
    dependencies = ['fastmcp', 'httpx', 'pydantic', 'packaging', 'cachetools']
    for dep in dependencies:
        try:
            info['dependencies'][dep] = pkg_resources.get_distribution(dep).version
        except pkg_resources.DistributionNotFound:
            info['dependencies'][dep] = 'Not installed'

    return info

# Print debug info
debug_info = collect_debug_info()
for key, value in debug_info.items():
    print(f"{key}: {value}")
```

### 3. Debugging Checklist

Before reporting issues:

- [ ] Enable debug logging
- [ ] Collect system information
- [ ] Create minimal reproduction case
- [ ] Check configuration values
- [ ] Test with default settings
- [ ] Verify network connectivity
- [ ] Check for recent changes
- [ ] Review error logs completely

## Next Steps

- [Common Issues](common-issues.md) - Troubleshoot common problems
- [Performance Guide](performance.md) - Optimize server performance
- [FAQ](faq.md) - Frequently asked questions
