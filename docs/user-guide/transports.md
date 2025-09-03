# Transport Configuration

Learn about the different transport protocols supported by PyPI MCP Server and how to configure them.

## Overview

The PyPI MCP Server supports two transport protocols:

- **STDIO Transport**: Direct stdin/stdout communication (default)
- **HTTP Transport**: RESTful HTTP API

Each transport has different use cases and configuration options.

## STDIO Transport

STDIO transport is the default and recommended transport for MCP clients like Claude Desktop.

### How It Works

STDIO transport uses JSON-RPC messages over stdin/stdout:

1. Client sends JSON-RPC requests to server's stdin
2. Server processes requests and sends responses to stdout
3. Communication follows the MCP protocol specification

### Configuration

```bash
# Default STDIO transport
pypi-mcp

# Explicit STDIO transport
pypi-mcp --transport stdio

# With logging configuration
pypi-mcp --transport stdio --log-level INFO
```

### Use Cases

STDIO transport is ideal for:

- **MCP Client Integration**: Claude Desktop, custom MCP clients
- **Process-to-Process Communication**: Direct subprocess communication
- **Local Development**: Testing and development scenarios
- **Embedded Applications**: When the server runs as a subprocess

### Example Integration

#### Claude Desktop Configuration

```json title="claude_desktop_config.json"
{
  "mcpServers": {
    "pypi": {
      "command": "pypi-mcp",
      "args": [],
      "env": {
        "PYPI_MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### Python Subprocess Integration

```python
import asyncio
import json
import subprocess

class STDIOMCPClient:
    def __init__(self):
        self.process = None

    async def start(self):
        self.process = await asyncio.create_subprocess_exec(
            'pypi-mcp',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def send_request(self, method, params=None):
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }

        request_json = json.dumps(request) + '\n'
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()

        response_line = await self.process.stdout.readline()
        return json.loads(response_line.decode())

    async def close(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()

# Usage
client = STDIOMCPClient()
await client.start()
response = await client.send_request("tools/list")
await client.close()
```

### Advantages

- **Low Latency**: Direct process communication
- **Simple Protocol**: Standard JSON-RPC over pipes
- **Resource Efficient**: No network overhead
- **Secure**: No network exposure

### Limitations

- **Single Client**: One client per server instance
- **Local Only**: Cannot be accessed remotely
- **Process Coupling**: Client and server lifecycles are coupled

## HTTP Transport

HTTP transport provides a RESTful API for remote access and multiple client support.

### How It Works

HTTP transport runs a web server that accepts JSON-RPC requests:

1. Server starts HTTP listener on specified host/port
2. Clients send POST requests with JSON-RPC payloads
3. Server responds with JSON-RPC responses
4. Supports multiple concurrent clients

### Configuration

```bash
# Basic HTTP transport
pypi-mcp --transport http

# Custom host and port
pypi-mcp --transport http --host 0.0.0.0 --port 8080

# Production configuration
pypi-mcp --transport http --host 127.0.0.1 --port 8000 --log-level WARNING
```

### Configuration Options

| Option   | Default     | Description             |
| -------- | ----------- | ----------------------- |
| `--host` | `localhost` | Host to bind the server |
| `--port` | `8000`      | Port to bind the server |

### Use Cases

HTTP transport is ideal for:

- **Web Applications**: Integration with web services
- **Remote Access**: Accessing the server from different machines
- **Multiple Clients**: Supporting concurrent client connections
- **Microservices**: Running as a standalone service
- **Load Balancing**: Deploying multiple instances behind a load balancer

### Example Integration

#### Python HTTP Client

```python
import httpx
import json

class HTTPMCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.request_id = 1

    async def send_request(self, method, params=None):
        async with httpx.AsyncClient() as client:
            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params or {},
                "id": self.request_id
            }
            self.request_id += 1

            response = await client.post(
                self.base_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            return response.json()

    async def get_package_info(self, package_name):
        return await self.send_request("tools/call", {
            "name": "get_package_info",
            "arguments": {"package_name": package_name}
        })

# Usage
client = HTTPMCPClient()
result = await client.get_package_info("requests")
```

#### JavaScript/Node.js Client

```javascript
const axios = require("axios");

class HTTPMCPClient {
  constructor(baseUrl = "http://localhost:8000") {
    this.baseUrl = baseUrl;
    this.requestId = 1;
  }

  async sendRequest(method, params = {}) {
    const payload = {
      jsonrpc: "2.0",
      method: method,
      params: params,
      id: this.requestId++,
    };

    const response = await axios.post(this.baseUrl, payload, {
      headers: { "Content-Type": "application/json" },
    });

    return response.data;
  }

  async getPackageInfo(packageName) {
    return await this.sendRequest("tools/call", {
      name: "get_package_info",
      arguments: { package_name: packageName },
    });
  }
}

// Usage
const client = new HTTPMCPClient();
const result = await client.getPackageInfo("fastapi");
```

#### cURL Examples

```bash
# Initialize connection
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "curl-client", "version": "1.0.0"}
    },
    "id": 1
  }'

# List available tools
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
  }'

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
    "id": 3
  }'
```

### Advantages

- **Multiple Clients**: Support concurrent connections
- **Remote Access**: Access from any network location
- **Standard Protocol**: HTTP/JSON-RPC is widely supported
- **Scalable**: Can be load balanced and clustered
- **Stateless**: Each request is independent

### Limitations

- **Network Overhead**: HTTP protocol overhead
- **Security Considerations**: Requires proper authentication/authorization
- **Resource Usage**: Higher memory and CPU usage
- **Complexity**: More complex deployment and configuration

## Transport Comparison

| Feature                | STDIO               | HTTP               |
| ---------------------- | ------------------- | ------------------ |
| **Latency**            | Very Low            | Low                |
| **Concurrent Clients** | Single              | Multiple           |
| **Remote Access**      | No                  | Yes                |
| **Resource Usage**     | Minimal             | Moderate           |
| **Security**           | Process-level       | Network-level      |
| **Deployment**         | Simple              | Complex            |
| **Protocol**           | JSON-RPC over pipes | JSON-RPC over HTTP |

## Security Considerations

### STDIO Transport Security

- **Process Isolation**: Runs in isolated process space
- **No Network Exposure**: Not accessible over network
- **File System Permissions**: Controlled by OS permissions
- **Input Validation**: Still validate all inputs

### HTTP Transport Security

- **Network Security**: Consider HTTPS in production
- **Authentication**: Implement authentication if needed
- **Authorization**: Control access to specific tools
- **Rate Limiting**: Built-in rate limiting protection
- **Input Validation**: Comprehensive input validation

#### Production HTTP Security

```bash
# Bind to localhost only (more secure)
pypi-mcp --transport http --host 127.0.0.1 --port 8000

# Use reverse proxy with HTTPS
# nginx/apache -> pypi-mcp HTTP server
```

#### Reverse Proxy Configuration (nginx)

```nginx
server {
    listen 443 ssl;
    server_name pypi-mcp.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Performance Considerations

### STDIO Transport Performance

- **Minimal Overhead**: Direct process communication
- **Memory Efficient**: No HTTP server overhead
- **CPU Efficient**: No HTTP parsing overhead
- **Optimal for**: Single client, local usage

### HTTP Transport Performance

- **Connection Pooling**: Reuse HTTP connections
- **Concurrent Requests**: Handle multiple requests simultaneously
- **Caching**: Leverage HTTP caching headers
- **Optimal for**: Multiple clients, remote usage

#### HTTP Performance Tuning

```bash
# Increase rate limit for high-throughput scenarios
export PYPI_MCP_RATE_LIMIT=50.0

# Optimize cache settings
export PYPI_MCP_CACHE_TTL=1800
export PYPI_MCP_CACHE_MAX_SIZE=5000

# Reduce timeout for faster responses
export PYPI_MCP_TIMEOUT=15.0
```

## Deployment Patterns

### Development

```bash
# STDIO for local development
pypi-mcp --log-level DEBUG

# HTTP for web development
pypi-mcp --transport http --log-level DEBUG
```

### Production

```bash
# STDIO with process manager
systemctl start pypi-mcp-stdio

# HTTP with reverse proxy
pypi-mcp --transport http --host 127.0.0.1 --port 8000
```

### Container Deployment

```dockerfile
# STDIO container
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -e .
CMD ["pypi-mcp"]

# HTTP container
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -e .
EXPOSE 8000
CMD ["pypi-mcp", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
```

## Choosing the Right Transport

### Use STDIO When:

- Integrating with MCP clients (Claude Desktop)
- Building single-user applications
- Developing locally
- Minimizing resource usage
- Security is paramount (no network exposure)

### Use HTTP When:

- Building web applications
- Supporting multiple concurrent users
- Deploying as a microservice
- Requiring remote access
- Integrating with existing HTTP infrastructure

## Next Steps

- [Configuration Guide](configuration.md) - Configure transport-specific settings
- [Integration Guide](../getting-started/integration.md) - Detailed integration examples
- [Performance Guide](../troubleshooting/performance.md) - Optimize transport performance
