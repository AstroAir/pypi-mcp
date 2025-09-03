# Configuration

Learn how to configure the PyPI MCP Server for optimal performance and functionality.

## Configuration Methods

The PyPI MCP server can be configured using multiple methods, listed in order of precedence:

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration file** (`.env`)
4. **Default values** (lowest priority)

## Environment Variables

All configuration options use the `PYPI_MCP_` prefix. Here's a complete reference:

### PyPI API Settings

Configure how the server interacts with PyPI:

| Variable                   | Default                   | Description                         |
| -------------------------- | ------------------------- | ----------------------------------- |
| `PYPI_MCP_PYPI_BASE_URL`   | `https://pypi.org`        | Base URL for PyPI API               |
| `PYPI_MCP_PYPI_SIMPLE_URL` | `https://pypi.org/simple` | PyPI simple index URL               |
| `PYPI_MCP_USER_AGENT`      | `pypi-mcp/0.1.0 (...)`    | User-Agent header for HTTP requests |

```bash
# Example PyPI API configuration
export PYPI_MCP_PYPI_BASE_URL="https://pypi.org"
export PYPI_MCP_USER_AGENT="my-app/1.0.0 (contact@example.com)"
```

### Performance Settings

Control server performance and resource usage:

| Variable                  | Default | Description                         |
| ------------------------- | ------- | ----------------------------------- |
| `PYPI_MCP_TIMEOUT`        | `30.0`  | HTTP request timeout in seconds     |
| `PYPI_MCP_MAX_RETRIES`    | `3`     | Maximum retries for failed requests |
| `PYPI_MCP_RATE_LIMIT`     | `10.0`  | Maximum requests per second         |
| `PYPI_MCP_CACHE_TTL`      | `300`   | Cache TTL in seconds                |
| `PYPI_MCP_CACHE_MAX_SIZE` | `1000`  | Maximum cache entries               |

```bash
# Example performance configuration
export PYPI_MCP_TIMEOUT=60.0
export PYPI_MCP_RATE_LIMIT=20.0
export PYPI_MCP_CACHE_TTL=600
export PYPI_MCP_CACHE_MAX_SIZE=2000
```

### Logging Configuration

Control logging behavior:

| Variable              | Default                                                | Description                                 |
| --------------------- | ------------------------------------------------------ | ------------------------------------------- |
| `PYPI_MCP_LOG_LEVEL`  | `INFO`                                                 | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `PYPI_MCP_LOG_FORMAT` | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` | Log format string                           |

```bash
# Example logging configuration
export PYPI_MCP_LOG_LEVEL=DEBUG
export PYPI_MCP_LOG_FORMAT="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
```

### Server Settings

Configure server identification and behavior:

| Variable                  | Default           | Description                    |
| ------------------------- | ----------------- | ------------------------------ |
| `PYPI_MCP_SERVER_NAME`    | `PyPI MCP Server` | Server name for identification |
| `PYPI_MCP_SERVER_VERSION` | `0.1.0`           | Server version                 |

```bash
# Example server configuration
export PYPI_MCP_SERVER_NAME="My PyPI MCP Server"
export PYPI_MCP_SERVER_VERSION="1.0.0"
```

### Feature Flags

Enable or disable specific features:

| Variable                              | Default | Description                         |
| ------------------------------------- | ------- | ----------------------------------- |
| `PYPI_MCP_ENABLE_VULNERABILITY_CHECK` | `true`  | Enable vulnerability checking       |
| `PYPI_MCP_ENABLE_STATS`               | `true`  | Enable statistics endpoints         |
| `PYPI_MCP_ENABLE_SEARCH`              | `true`  | Enable package search functionality |

```bash
# Example feature flag configuration
export PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true
export PYPI_MCP_ENABLE_STATS=false
export PYPI_MCP_ENABLE_SEARCH=true
```

## Configuration File

Create a `.env` file in your project root for persistent configuration:

```env title=".env"
# PyPI API Settings
PYPI_MCP_PYPI_BASE_URL=https://pypi.org
PYPI_MCP_USER_AGENT=my-app/1.0.0

# Performance Settings
PYPI_MCP_TIMEOUT=45.0
PYPI_MCP_RATE_LIMIT=15.0
PYPI_MCP_CACHE_TTL=600
PYPI_MCP_CACHE_MAX_SIZE=1500

# Logging
PYPI_MCP_LOG_LEVEL=INFO

# Feature Flags
PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true
PYPI_MCP_ENABLE_STATS=true
PYPI_MCP_ENABLE_SEARCH=true
```

## Command-Line Arguments

Override configuration with command-line arguments:

```bash
# Transport configuration
pypi-mcp --transport stdio          # Default STDIO transport
pypi-mcp --transport http           # HTTP transport

# HTTP transport options
pypi-mcp --transport http --host 0.0.0.0 --port 8080

# Logging level
pypi-mcp --log-level DEBUG

# Combined example
pypi-mcp --transport http --host localhost --port 8000 --log-level INFO
```

### Available Arguments

| Argument      | Options                             | Description              |
| ------------- | ----------------------------------- | ------------------------ |
| `--transport` | `stdio`, `http`                     | Transport protocol       |
| `--host`      | IP address                          | Host to bind (HTTP only) |
| `--port`      | Port number                         | Port to bind (HTTP only) |
| `--log-level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Logging level            |

## Configuration Examples

### Development Configuration

For development environments with detailed logging and relaxed limits:

```env title=".env.development"
PYPI_MCP_LOG_LEVEL=DEBUG
PYPI_MCP_TIMEOUT=60.0
PYPI_MCP_RATE_LIMIT=5.0
PYPI_MCP_CACHE_TTL=60
PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true
PYPI_MCP_ENABLE_STATS=true
PYPI_MCP_ENABLE_SEARCH=true
```

### Production Configuration

For production environments with optimized performance:

```env title=".env.production"
PYPI_MCP_LOG_LEVEL=WARNING
PYPI_MCP_TIMEOUT=30.0
PYPI_MCP_RATE_LIMIT=20.0
PYPI_MCP_CACHE_TTL=900
PYPI_MCP_CACHE_MAX_SIZE=5000
PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true
PYPI_MCP_ENABLE_STATS=false
PYPI_MCP_ENABLE_SEARCH=true
```

### High-Performance Configuration

For high-throughput scenarios:

```env title=".env.high-performance"
PYPI_MCP_LOG_LEVEL=ERROR
PYPI_MCP_TIMEOUT=15.0
PYPI_MCP_RATE_LIMIT=50.0
PYPI_MCP_CACHE_TTL=1800
PYPI_MCP_CACHE_MAX_SIZE=10000
PYPI_MCP_MAX_RETRIES=1
```

### Security-Focused Configuration

For security-sensitive environments:

```env title=".env.security"
PYPI_MCP_LOG_LEVEL=INFO
PYPI_MCP_TIMEOUT=20.0
PYPI_MCP_RATE_LIMIT=5.0
PYPI_MCP_CACHE_TTL=300
PYPI_MCP_ENABLE_VULNERABILITY_CHECK=true
PYPI_MCP_ENABLE_STATS=false
PYPI_MCP_ENABLE_SEARCH=false
```

## Configuration Validation

The server validates configuration on startup. Common validation errors:

!!! error "Invalid Configuration Examples"
```bash # Invalid timeout (must be positive)
PYPI_MCP_TIMEOUT=-1.0

    # Invalid rate limit (must be positive)
    PYPI_MCP_RATE_LIMIT=0

    # Invalid cache size (must be positive)
    PYPI_MCP_CACHE_MAX_SIZE=0

    # Invalid log level
    PYPI_MCP_LOG_LEVEL=INVALID
    ```

## Dynamic Configuration

Some settings can be changed at runtime:

### Cache Management

```python
# Get current cache statistics
result = await get_cache_info()
print(f"Cache hit rate: {result['cache_stats']['hit_rate']:.2%}")

# Cache is automatically managed based on TTL and size limits
```

### Rate Limiting

Rate limiting is enforced per-client and resets automatically. Monitor rate limit status through logs:

```
2025-01-XX XX:XX:XX - pypi_mcp.client - WARNING - Rate limit approached: 9/10 requests
```

## Configuration Best Practices

### Performance Optimization

1. **Cache Settings**: Balance memory usage vs. performance

   ```bash
   # For memory-constrained environments
   PYPI_MCP_CACHE_MAX_SIZE=500
   PYPI_MCP_CACHE_TTL=300

   # For performance-critical environments
   PYPI_MCP_CACHE_MAX_SIZE=5000
   PYPI_MCP_CACHE_TTL=1800
   ```

2. **Rate Limiting**: Adjust based on PyPI's rate limits and your needs

   ```bash
   # Conservative (recommended for shared environments)
   PYPI_MCP_RATE_LIMIT=5.0

   # Aggressive (for dedicated environments)
   PYPI_MCP_RATE_LIMIT=20.0
   ```

3. **Timeouts**: Balance responsiveness vs. reliability

   ```bash
   # Fast responses (may fail on slow networks)
   PYPI_MCP_TIMEOUT=15.0

   # Reliable (slower but more robust)
   PYPI_MCP_TIMEOUT=60.0
   ```

### Security Considerations

1. **Disable Unnecessary Features**:

   ```bash
   # Disable statistics if not needed
   PYPI_MCP_ENABLE_STATS=false

   # Disable search if only using specific packages
   PYPI_MCP_ENABLE_SEARCH=false
   ```

2. **Logging Levels**:

   ```bash
   # Production: minimal logging
   PYPI_MCP_LOG_LEVEL=WARNING

   # Development: detailed logging
   PYPI_MCP_LOG_LEVEL=DEBUG
   ```

### Monitoring and Debugging

1. **Enable Debug Logging**:

   ```bash
   PYPI_MCP_LOG_LEVEL=DEBUG
   ```

2. **Monitor Cache Performance**:

   ```python
   # Check cache statistics regularly
   cache_info = await get_cache_info()
   hit_rate = cache_info['cache_stats']['hit_rate']

   # Adjust cache settings if hit rate is low
   if hit_rate < 0.8:
       # Consider increasing cache size or TTL
       pass
   ```

## Troubleshooting Configuration

### Common Issues

1. **Environment Variables Not Loaded**:

   ```bash
   # Verify variables are set
   env | grep PYPI_MCP_

   # Check if .env file exists and is readable
   ls -la .env
   ```

2. **Invalid Configuration Values**:

   ```bash
   # Check server startup logs for validation errors
   pypi-mcp --log-level DEBUG
   ```

3. **Performance Issues**:
   ```bash
   # Monitor cache hit rate
   # Adjust rate limiting
   # Increase timeout for slow networks
   ```

### Configuration Testing

Test your configuration:

```bash
# Test with debug logging
pypi-mcp --log-level DEBUG

# Verify environment variables
python -c "from pypi_mcp.config import settings; print(settings.dict())"

# Test specific configuration
PYPI_MCP_CACHE_TTL=60 pypi-mcp --log-level DEBUG
```

## Next Steps

- [Usage Examples](usage-examples.md) - See practical configuration examples
- [Caching Guide](caching.md) - Optimize cache performance
- [Transport Configuration](transports.md) - Configure STDIO vs HTTP transport
