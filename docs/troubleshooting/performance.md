# Performance Guide

Optimize PyPI MCP Server performance for your specific use case and environment.

## Performance Overview

The PyPI MCP Server is designed for high performance with:

- **Async Architecture**: Non-blocking I/O operations
- **Intelligent Caching**: TTL-based cache with LRU eviction
- **Rate Limiting**: Configurable request throttling
- **Connection Pooling**: Efficient HTTP connection reuse

## Performance Metrics

### Key Performance Indicators

| Metric             | Good      | Acceptable | Poor      |
| ------------------ | --------- | ---------- | --------- |
| **Response Time**  | <100ms    | <500ms     | >1s       |
| **Cache Hit Rate** | >80%      | >60%       | <40%      |
| **Memory Usage**   | <100MB    | <200MB     | >500MB    |
| **CPU Usage**      | <10%      | <25%       | >50%      |
| **Throughput**     | >50 req/s | >20 req/s  | <10 req/s |

### Measuring Performance

#### Response Time Monitoring

```python
import time
import asyncio
from pypi_mcp.client import client

async def measure_response_time():
    """Measure average response time."""
    times = []

    async with client:
        for _ in range(10):
            start = time.time()
            await client.get_package_info("requests")
            end = time.time()
            times.append(end - start)

    avg_time = sum(times) / len(times)
    print(f"Average response time: {avg_time:.3f}s")
    return avg_time

# Run measurement
asyncio.run(measure_response_time())
```

#### Cache Performance Monitoring

```python
import asyncio
from pypi_mcp.cache import get_cache_stats

async def monitor_cache():
    """Monitor cache performance."""
    stats = await get_cache_stats()

    print(f"Cache hit rate: {stats['hit_rate']:.2%}")
    print(f"Cache utilization: {stats['current_size']}/{stats['max_size']}")
    print(f"Total hits: {stats['hits']}")
    print(f"Total misses: {stats['misses']}")

    return stats

# Monitor cache
asyncio.run(monitor_cache())
```

#### Memory Usage Monitoring

```python
import psutil
import os

def monitor_memory():
    """Monitor memory usage."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    print(f"RSS Memory: {memory_info.rss / 1024 / 1024:.1f} MB")
    print(f"VMS Memory: {memory_info.vms / 1024 / 1024:.1f} MB")
    print(f"Memory %: {process.memory_percent():.1f}%")

    return memory_info

# Monitor memory
monitor_memory()
```

## Performance Optimization

### 1. Cache Optimization

#### Optimal Cache Settings

```bash
# High-performance configuration
export PYPI_MCP_CACHE_TTL=1800      # 30 minutes
export PYPI_MCP_CACHE_MAX_SIZE=10000 # 10,000 items

# Balanced configuration
export PYPI_MCP_CACHE_TTL=900       # 15 minutes
export PYPI_MCP_CACHE_MAX_SIZE=5000  # 5,000 items

# Memory-constrained configuration
export PYPI_MCP_CACHE_TTL=300       # 5 minutes
export PYPI_MCP_CACHE_MAX_SIZE=1000  # 1,000 items
```

#### Cache Warming

Pre-populate cache with frequently accessed packages:

```python
import asyncio
from pypi_mcp.client import client

async def warm_cache():
    """Warm up cache with popular packages."""
    popular_packages = [
        'requests', 'urllib3', 'certifi', 'charset-normalizer',
        'idna', 'numpy', 'pandas', 'matplotlib', 'scipy',
        'django', 'flask', 'fastapi', 'sqlalchemy', 'pytest',
        'setuptools', 'wheel', 'pip', 'packaging', 'six'
    ]

    async with client:
        print("Warming cache...")
        for i, package in enumerate(popular_packages):
            try:
                await client.get_package_info(package)
                print(f"Cached {package} ({i+1}/{len(popular_packages)})")
            except Exception as e:
                print(f"Failed to cache {package}: {e}")

    print("Cache warming complete")

# Run cache warming
asyncio.run(warm_cache())
```

#### Cache Hit Rate Optimization

```python
async def optimize_cache_hit_rate():
    """Analyze and optimize cache hit rate."""
    stats = await get_cache_stats()
    hit_rate = stats['hit_rate']

    if hit_rate < 0.6:
        print("Low hit rate detected. Recommendations:")
        print("1. Increase cache size: PYPI_MCP_CACHE_MAX_SIZE")
        print("2. Increase cache TTL: PYPI_MCP_CACHE_TTL")
        print("3. Warm up cache with popular packages")
    elif hit_rate < 0.8:
        print("Moderate hit rate. Consider:")
        print("1. Slightly increase cache size")
        print("2. Analyze access patterns")
    else:
        print("Good hit rate! Cache is performing well.")

    return hit_rate

# Analyze cache performance
asyncio.run(optimize_cache_hit_rate())
```

### 2. Network Optimization

#### Connection Settings

```bash
# Optimize for high-throughput
export PYPI_MCP_TIMEOUT=15.0         # Faster timeouts
export PYPI_MCP_RATE_LIMIT=50.0      # Higher rate limit
export PYPI_MCP_MAX_RETRIES=1        # Fewer retries

# Optimize for reliability
export PYPI_MCP_TIMEOUT=60.0         # Longer timeouts
export PYPI_MCP_RATE_LIMIT=10.0      # Conservative rate limit
export PYPI_MCP_MAX_RETRIES=3        # More retries
```

#### Connection Pooling

The server automatically uses connection pooling. Monitor connection efficiency:

```python
import httpx

async def test_connection_pooling():
    """Test connection pooling efficiency."""
    async with httpx.AsyncClient() as client:
        # Multiple requests should reuse connections
        tasks = []
        for _ in range(10):
            task = client.get("https://pypi.org/pypi/requests/json")
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(f"Completed {len(responses)} requests")

asyncio.run(test_connection_pooling())
```

### 3. Rate Limiting Optimization

#### Dynamic Rate Limiting

```python
import time
from collections import deque

class AdaptiveRateLimiter:
    """Adaptive rate limiter based on response times."""

    def __init__(self, initial_rate=10.0):
        self.rate = initial_rate
        self.response_times = deque(maxlen=100)
        self.last_adjustment = time.time()

    def record_response_time(self, response_time):
        """Record response time and adjust rate if needed."""
        self.response_times.append(response_time)

        # Adjust rate every 60 seconds
        if time.time() - self.last_adjustment > 60:
            self.adjust_rate()
            self.last_adjustment = time.time()

    def adjust_rate(self):
        """Adjust rate based on recent response times."""
        if not self.response_times:
            return

        avg_time = sum(self.response_times) / len(self.response_times)

        if avg_time < 0.1:  # Very fast responses
            self.rate = min(self.rate * 1.2, 100.0)  # Increase rate
        elif avg_time > 1.0:  # Slow responses
            self.rate = max(self.rate * 0.8, 1.0)   # Decrease rate

        print(f"Adjusted rate to {self.rate:.1f} req/s (avg time: {avg_time:.3f}s)")

# Usage example
rate_limiter = AdaptiveRateLimiter()
```

### 4. Memory Optimization

#### Memory-Efficient Configuration

```bash
# Minimize memory usage
export PYPI_MCP_CACHE_MAX_SIZE=500   # Smaller cache
export PYPI_MCP_CACHE_TTL=300        # Shorter TTL
```

#### Memory Monitoring

```python
import gc
import psutil
import os

def memory_profile():
    """Profile memory usage."""
    process = psutil.Process(os.getpid())

    # Before garbage collection
    before = process.memory_info().rss / 1024 / 1024

    # Force garbage collection
    gc.collect()

    # After garbage collection
    after = process.memory_info().rss / 1024 / 1024

    print(f"Memory before GC: {before:.1f} MB")
    print(f"Memory after GC: {after:.1f} MB")
    print(f"Memory freed: {before - after:.1f} MB")

    return after

# Profile memory
memory_profile()
```

#### Memory Leak Detection

```python
import tracemalloc
import asyncio

async def detect_memory_leaks():
    """Detect potential memory leaks."""
    tracemalloc.start()

    # Take initial snapshot
    snapshot1 = tracemalloc.take_snapshot()

    # Perform operations
    async with client:
        for _ in range(100):
            await client.get_package_info("requests")

    # Take final snapshot
    snapshot2 = tracemalloc.take_snapshot()

    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("Top 10 memory allocations:")
    for stat in top_stats[:10]:
        print(stat)

# Run leak detection
asyncio.run(detect_memory_leaks())
```

## Performance Tuning by Use Case

### 1. High-Throughput Scenarios

For applications requiring high request rates:

```bash
# Configuration for high throughput
export PYPI_MCP_CACHE_TTL=3600       # 1 hour cache
export PYPI_MCP_CACHE_MAX_SIZE=20000 # Large cache
export PYPI_MCP_RATE_LIMIT=100.0     # High rate limit
export PYPI_MCP_TIMEOUT=10.0         # Fast timeouts
export PYPI_MCP_MAX_RETRIES=1        # Minimal retries
```

### 2. Memory-Constrained Environments

For environments with limited memory:

```bash
# Configuration for low memory
export PYPI_MCP_CACHE_TTL=300        # 5 minute cache
export PYPI_MCP_CACHE_MAX_SIZE=200   # Small cache
export PYPI_MCP_RATE_LIMIT=5.0       # Conservative rate
export PYPI_MCP_TIMEOUT=30.0         # Standard timeout
```

### 3. Reliability-Focused Scenarios

For applications prioritizing reliability over speed:

```bash
# Configuration for reliability
export PYPI_MCP_CACHE_TTL=1800       # 30 minute cache
export PYPI_MCP_CACHE_MAX_SIZE=5000  # Moderate cache
export PYPI_MCP_RATE_LIMIT=10.0      # Conservative rate
export PYPI_MCP_TIMEOUT=60.0         # Long timeout
export PYPI_MCP_MAX_RETRIES=5        # More retries
```

### 4. Development Environments

For development and testing:

```bash
# Configuration for development
export PYPI_MCP_CACHE_TTL=60         # 1 minute cache
export PYPI_MCP_CACHE_MAX_SIZE=100   # Small cache
export PYPI_MCP_RATE_LIMIT=20.0      # Higher rate for testing
export PYPI_MCP_LOG_LEVEL=DEBUG      # Detailed logging
```

## Load Testing

### Basic Load Test

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

async def load_test(concurrent_requests=10, total_requests=100):
    """Perform basic load test."""
    print(f"Starting load test: {total_requests} requests, {concurrent_requests} concurrent")

    start_time = time.time()
    completed = 0
    errors = 0

    async def make_request():
        nonlocal completed, errors
        try:
            async with client:
                await client.get_package_info("requests")
            completed += 1
        except Exception as e:
            errors += 1
            print(f"Error: {e}")

    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(concurrent_requests)

    async def limited_request():
        async with semaphore:
            await make_request()

    # Create tasks
    tasks = [limited_request() for _ in range(total_requests)]

    # Execute tasks
    await asyncio.gather(*tasks)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Load test completed in {duration:.2f}s")
    print(f"Requests per second: {total_requests / duration:.2f}")
    print(f"Completed: {completed}, Errors: {errors}")
    print(f"Success rate: {completed / total_requests:.2%}")

# Run load test
asyncio.run(load_test(concurrent_requests=20, total_requests=200))
```

### Stress Test

```python
async def stress_test():
    """Perform stress test to find breaking point."""
    concurrent_levels = [1, 5, 10, 20, 50, 100]

    for level in concurrent_levels:
        print(f"\nTesting {level} concurrent requests...")

        try:
            start_time = time.time()

            async def stress_request():
                async with client:
                    await client.get_package_info("requests")

            tasks = [stress_request() for _ in range(level)]
            await asyncio.gather(*tasks)

            duration = time.time() - start_time
            rps = level / duration

            print(f"Success: {level} requests in {duration:.2f}s ({rps:.2f} req/s)")

        except Exception as e:
            print(f"Failed at {level} concurrent requests: {e}")
            break

# Run stress test
asyncio.run(stress_test())
```

## Performance Monitoring

### Real-time Monitoring

```python
import asyncio
import time
from collections import deque

class PerformanceMonitor:
    """Real-time performance monitoring."""

    def __init__(self, window_size=100):
        self.response_times = deque(maxlen=window_size)
        self.error_count = 0
        self.request_count = 0
        self.start_time = time.time()

    def record_request(self, response_time, error=False):
        """Record request metrics."""
        self.response_times.append(response_time)
        self.request_count += 1
        if error:
            self.error_count += 1

    def get_stats(self):
        """Get current performance statistics."""
        if not self.response_times:
            return {}

        duration = time.time() - self.start_time
        avg_response_time = sum(self.response_times) / len(self.response_times)
        rps = self.request_count / duration if duration > 0 else 0
        error_rate = self.error_count / self.request_count if self.request_count > 0 else 0

        return {
            'avg_response_time': avg_response_time,
            'requests_per_second': rps,
            'error_rate': error_rate,
            'total_requests': self.request_count,
            'total_errors': self.error_count
        }

    def print_stats(self):
        """Print current statistics."""
        stats = self.get_stats()
        if stats:
            print(f"Avg Response Time: {stats['avg_response_time']:.3f}s")
            print(f"Requests/sec: {stats['requests_per_second']:.2f}")
            print(f"Error Rate: {stats['error_rate']:.2%}")
            print(f"Total Requests: {stats['total_requests']}")

# Usage
monitor = PerformanceMonitor()

async def monitored_request():
    """Make a monitored request."""
    start = time.time()
    try:
        async with client:
            await client.get_package_info("requests")
        monitor.record_request(time.time() - start)
    except Exception as e:
        monitor.record_request(time.time() - start, error=True)

# Run monitoring
async def run_monitoring():
    for i in range(50):
        await monitored_request()
        if i % 10 == 0:
            monitor.print_stats()

asyncio.run(run_monitoring())
```

## Performance Troubleshooting

### Identifying Bottlenecks

1. **High Response Times**:

   - Check network connectivity
   - Verify PyPI API status
   - Increase cache hit rate
   - Reduce timeout values

2. **Low Cache Hit Rate**:

   - Increase cache size
   - Increase cache TTL
   - Analyze request patterns
   - Warm up cache

3. **High Memory Usage**:

   - Reduce cache size
   - Check for memory leaks
   - Monitor garbage collection
   - Profile memory allocation

4. **High CPU Usage**:
   - Check for infinite loops
   - Profile CPU usage
   - Optimize algorithms
   - Reduce request rate

### Performance Profiling

```python
import cProfile
import pstats
import asyncio

def profile_performance():
    """Profile server performance."""

    async def profile_target():
        async with client:
            for _ in range(20):
                await client.get_package_info("requests")

    # Run with profiling
    cProfile.run('asyncio.run(profile_target())', 'profile_stats')

    # Analyze results
    stats = pstats.Stats('profile_stats')
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions

# Run profiling
profile_performance()
```

## Next Steps

- [Debugging Guide](debugging.md) - Advanced debugging techniques
- [Common Issues](common-issues.md) - Troubleshoot common problems
- [Configuration Guide](../user-guide/configuration.md) - Optimize configuration
