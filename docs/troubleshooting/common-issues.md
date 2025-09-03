# Common Issues

Solutions to frequently encountered problems with the PyPI MCP Server.

## Installation Issues

### Python Version Compatibility

**Problem**: Error about Python version when installing

```
ERROR: Package requires Python >=3.11 but you have Python 3.10
```

**Solution**:

```bash
# Check your Python version
python --version

# Install Python 3.11+ using pyenv
pyenv install 3.11.0
pyenv local 3.11.0

# Or use conda
conda install python=3.11

# Verify version
python --version
```

### Package Installation Failures

**Problem**: `pip install` fails with dependency conflicts

```
ERROR: Could not find a version that satisfies the requirement fastmcp>=2.12.0
```

**Solutions**:

=== "Using uv (Recommended)"
`bash
    # Clear cache and reinstall
    uv cache clean
    uv sync
    `

=== "Using pip"
```bash # Clear pip cache
pip cache purge

    # Upgrade pip
    pip install --upgrade pip

    # Install with no cache
    pip install --no-cache-dir -e .
    ```

=== "Fresh Environment"
`bash
    # Create new virtual environment
    python -m venv fresh_env
    source fresh_env/bin/activate  # Windows: fresh_env\Scripts\activate
    pip install -e .
    `

### Permission Issues

**Problem**: Permission denied during installation

```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions**:

```bash
# Install in user directory
pip install --user -e .

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -e .

# On macOS/Linux, check permissions
ls -la /usr/local/lib/python*/site-packages/
```

## Runtime Issues

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'pypi_mcp'`

**Solutions**:

```bash
# Verify installation
pip list | grep pypi-mcp

# Reinstall in development mode
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"

# Verify you're in the right environment
which python
which pypi-mcp
```

### Server Won't Start

**Problem**: Server fails to start with various errors

**Common Causes and Solutions**:

#### Port Already in Use (HTTP Transport)

```bash
# Error: Address already in use
# Solution: Use different port
pypi-mcp --transport http --port 8080

# Or find and kill process using port
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

#### Configuration Errors

```bash
# Error: Invalid configuration
# Solution: Check environment variables
env | grep PYPI_MCP_

# Reset to defaults
unset PYPI_MCP_CACHE_TTL
unset PYPI_MCP_RATE_LIMIT

# Test with minimal config
pypi-mcp --log-level DEBUG
```

#### Missing Dependencies

```bash
# Error: ImportError
# Solution: Reinstall dependencies
pip install -e ".[dev]"

# Or check specific dependency
python -c "import fastmcp"
python -c "import httpx"
```

### Network and API Issues

#### Connection Timeouts

**Problem**: Requests to PyPI timeout

```
TimeoutError: Request timed out after 30 seconds
```

**Solutions**:

```bash
# Increase timeout
export PYPI_MCP_TIMEOUT=60.0

# Check network connectivity
curl -I https://pypi.org

# Test with different PyPI mirror
export PYPI_MCP_PYPI_BASE_URL="https://pypi.python.org"
```

#### Rate Limiting

**Problem**: Too many requests to PyPI

```
HTTP 429: Too Many Requests
```

**Solutions**:

```bash
# Reduce rate limit
export PYPI_MCP_RATE_LIMIT=5.0

# Increase cache TTL to reduce API calls
export PYPI_MCP_CACHE_TTL=600

# Check current rate limit settings
python -c "from pypi_mcp.config import settings; print(f'Rate limit: {settings.rate_limit}')"
```

#### SSL/TLS Issues

**Problem**: SSL certificate verification fails

```
SSLError: certificate verify failed
```

**Solutions**:

```bash
# Update certificates (macOS)
/Applications/Python\ 3.11/Install\ Certificates.command

# Update certificates (Linux)
sudo apt-get update && sudo apt-get install ca-certificates

# Temporary workaround (not recommended for production)
export PYTHONHTTPSVERIFY=0
```

## Configuration Issues

### Environment Variables Not Loading

**Problem**: Configuration changes don't take effect

**Solutions**:

```bash
# Verify environment variables are set
env | grep PYPI_MCP_

# Check .env file exists and is readable
ls -la .env
cat .env

# Test configuration loading
python -c "
from pypi_mcp.config import settings
print(f'Log level: {settings.log_level}')
print(f'Cache TTL: {settings.cache_ttl}')
"

# Restart server after configuration changes
```

### Invalid Configuration Values

**Problem**: Server fails with configuration validation errors

```
ValidationError: Invalid value for PYPI_MCP_CACHE_TTL
```

**Solutions**:

```bash
# Check valid ranges
export PYPI_MCP_CACHE_TTL=300      # Must be positive integer
export PYPI_MCP_RATE_LIMIT=10.0    # Must be positive float
export PYPI_MCP_TIMEOUT=30.0       # Must be positive float

# Reset to defaults
unset PYPI_MCP_CACHE_TTL
unset PYPI_MCP_RATE_LIMIT
unset PYPI_MCP_TIMEOUT

# Verify configuration
pypi-mcp --log-level DEBUG
```

## MCP Integration Issues

### Claude Desktop Integration

**Problem**: Claude Desktop doesn't recognize the server

**Solutions**:

1. **Verify Installation**:

   ```bash
   # Test server is accessible
   pypi-mcp --help
   which pypi-mcp
   ```

2. **Check Configuration File**:

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

3. **Configuration File Locations**:

   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

4. **Restart Claude Desktop** after configuration changes

5. **Check Logs**:
   ```bash
   # Run server with debug logging
   pypi-mcp --log-level DEBUG
   ```

### STDIO Transport Issues

**Problem**: STDIO communication fails

**Solutions**:

```bash
# Test STDIO manually
echo '{"jsonrpc": "2.0", "method": "initialize", "id": 1}' | pypi-mcp

# Check for output buffering issues
export PYTHONUNBUFFERED=1
pypi-mcp

# Verify JSON-RPC format
# Ensure messages end with newline
```

### HTTP Transport Issues

**Problem**: HTTP transport not working

**Solutions**:

```bash
# Test HTTP server
pypi-mcp --transport http --log-level DEBUG

# Test with curl
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": 1}'

# Check firewall settings
# Ensure port 8000 is not blocked

# Try different host/port
pypi-mcp --transport http --host 127.0.0.1 --port 8080
```

## Performance Issues

### Slow Response Times

**Problem**: Server responds slowly

**Diagnostic Steps**:

```bash
# Check cache hit rate
python -c "
import asyncio
from pypi_mcp.cache import get_cache_stats
stats = asyncio.run(get_cache_stats())
print(f'Hit rate: {stats[\"hit_rate\"]:.2%}')
"

# Monitor network latency
ping pypi.org

# Check system resources
top
htop
```

**Solutions**:

```bash
# Increase cache size and TTL
export PYPI_MCP_CACHE_MAX_SIZE=5000
export PYPI_MCP_CACHE_TTL=1800

# Reduce timeout for faster failures
export PYPI_MCP_TIMEOUT=15.0

# Increase rate limit if network allows
export PYPI_MCP_RATE_LIMIT=20.0
```

### High Memory Usage

**Problem**: Server uses too much memory

**Diagnostic Steps**:

```bash
# Monitor memory usage
ps aux | grep pypi-mcp

# Check cache size
python -c "
import asyncio
from pypi_mcp.cache import get_cache_stats
stats = asyncio.run(get_cache_stats())
print(f'Cache size: {stats[\"current_size\"]}/{stats[\"max_size\"]}')
"
```

**Solutions**:

```bash
# Reduce cache size
export PYPI_MCP_CACHE_MAX_SIZE=500

# Reduce cache TTL
export PYPI_MCP_CACHE_TTL=300

# Monitor memory usage
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB')
```

## Data and Cache Issues

### Stale Data

**Problem**: Server returns outdated information

**Solutions**:

```bash
# Reduce cache TTL for fresher data
export PYPI_MCP_CACHE_TTL=300  # 5 minutes

# Clear cache by restarting server
# (No manual cache clearing API currently)

# Check PyPI API directly
curl https://pypi.org/pypi/requests/json
```

### Cache Performance Issues

**Problem**: Low cache hit rate

**Diagnostic Steps**:

```bash
# Check cache statistics
python -c "
import asyncio
from pypi_mcp.cache import get_cache_stats
stats = asyncio.run(get_cache_stats())
print(f'Hit rate: {stats[\"hit_rate\"]:.2%}')
print(f'Hits: {stats[\"hits\"]}, Misses: {stats[\"misses\"]}')
"
```

**Solutions**:

```bash
# Increase cache size
export PYPI_MCP_CACHE_MAX_SIZE=2000

# Increase cache TTL
export PYPI_MCP_CACHE_TTL=900

# Warm up cache with popular packages
python -c "
import asyncio
from pypi_mcp.client import client

async def warm_cache():
    packages = ['requests', 'numpy', 'django', 'flask']
    async with client:
        for pkg in packages:
            try:
                await client.get_package_info(pkg)
            except:
                pass

asyncio.run(warm_cache())
"
```

## Error Messages and Debugging

### Enable Debug Logging

```bash
# Set debug logging
export PYPI_MCP_LOG_LEVEL=DEBUG

# Run with debug output
pypi-mcp --log-level DEBUG

# Check specific component logs
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# ... run your code ...
"
```

### Common Error Patterns

#### JSON-RPC Errors

```json
{
  "error": {
    "code": -32602,
    "message": "Invalid params"
  }
}
```

**Solution**: Check parameter names and types

#### Package Not Found

```json
{
  "error": {
    "code": -32000,
    "message": "Package not found"
  }
}
```

**Solution**: Verify package name spelling and existence on PyPI

#### Rate Limit Exceeded

```json
{
  "error": {
    "code": -32002,
    "message": "Rate limit exceeded"
  }
}
```

**Solution**: Reduce request rate or increase rate limit

### Debugging Tools

```bash
# Test individual components
python -c "
import asyncio
from pypi_mcp.client import client

async def test():
    async with client:
        info = await client.get_package_info('requests')
        print(info.name)

asyncio.run(test())
"

# Test configuration
python -c "
from pypi_mcp.config import settings
print(settings.dict())
"

# Test cache
python -c "
import asyncio
from pypi_mcp.cache import get_cache_stats
print(asyncio.run(get_cache_stats()))
"
```

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing issues** on GitHub
3. **Enable debug logging** and check logs
4. **Test with minimal configuration**
5. **Verify your environment** (Python version, dependencies)

### Information to Include

When reporting issues, include:

- **Operating System**: Version and architecture
- **Python Version**: `python --version`
- **Package Version**: `pip show pypi-mcp`
- **Configuration**: Environment variables (sanitized)
- **Error Messages**: Complete error output
- **Steps to Reproduce**: Minimal example
- **Expected vs Actual**: What you expected vs what happened

### Where to Get Help

- **GitHub Issues**: [Report bugs and issues](https://github.com/AstroAir/pypi-mcp/issues)
- **GitHub Discussions**: [Ask questions and discuss](https://github.com/AstroAir/pypi-mcp/discussions)
- **Documentation**: [Read the full documentation](../index.md)

## Next Steps

- [Performance Guide](performance.md) - Optimize server performance
- [Debugging Guide](debugging.md) - Advanced debugging techniques
- [FAQ](faq.md) - Frequently asked questions
