# Integration Guide

Learn how to integrate PyPI MCP Server with different MCP clients and platforms.

## Overview

The PyPI MCP Server can be integrated with any MCP-compatible client. This guide covers the most common integration scenarios and provides step-by-step instructions.

## Claude Desktop Integration

Claude Desktop is the most popular MCP client. Here's how to integrate the PyPI MCP Server:

### Configuration File Location

The Claude Desktop configuration file is located at:

=== "macOS"
`    ~/Library/Application Support/Claude/claude_desktop_config.json
   `

=== "Windows"
`    %APPDATA%\Claude\claude_desktop_config.json
   `

=== "Linux"
`    ~/.config/claude/claude_desktop_config.json
   `

### Basic Configuration

Add the PyPI MCP Server to your configuration:

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

### Advanced Configuration

For more control, you can specify environment variables and arguments:

```json
{
  "mcpServers": {
    "pypi": {
      "command": "pypi-mcp",
      "args": ["--log-level", "INFO"],
      "env": {
        "PYPI_MCP_LOG_LEVEL": "INFO",
        "PYPI_MCP_CACHE_TTL": "600",
        "PYPI_MCP_RATE_LIMIT": "15.0",
        "PYPI_MCP_TIMEOUT": "45.0"
      }
    }
  }
}
```

### Multiple Server Configuration

You can run multiple MCP servers alongside PyPI MCP:

```json
{
  "mcpServers": {
    "pypi": {
      "command": "pypi-mcp",
      "args": []
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/files"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Troubleshooting Claude Desktop Integration

!!! warning "Common Issues" - **Server not found**: Ensure `pypi-mcp` is in your PATH - **Permission denied**: Check file permissions and PATH configuration - **Configuration not loaded**: Restart Claude Desktop after configuration changes

## HTTP Transport Integration

For custom clients or web applications, use HTTP transport:

### Starting HTTP Server

```bash
# Start server on default port (8000)
pypi-mcp --transport http

# Start on custom port
pypi-mcp --transport http --port 8080

# Start with specific host binding
pypi-mcp --transport http --host 0.0.0.0 --port 8000
```

### HTTP Client Example

Here's a Python example of connecting to the HTTP transport:

```python
import httpx
import json

async def call_pypi_mcp(method: str, params: dict = None):
    """Call PyPI MCP server via HTTP transport."""
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }

        response = await client.post(
            "http://localhost:8000",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        return response.json()

# Example usage
async def main():
    # Initialize the connection
    init_response = await call_pypi_mcp("initialize")
    print("Initialized:", init_response)

    # Call a tool
    result = await call_pypi_mcp("tools/call", {
        "name": "get_package_info",
        "arguments": {"package_name": "requests"}
    })
    print("Package info:", result)

# Run the example
import asyncio
asyncio.run(main())
```

### JavaScript/Node.js Client Example

```javascript
const axios = require("axios");

class PyPIMCPClient {
  constructor(baseUrl = "http://localhost:8000") {
    this.baseUrl = baseUrl;
    this.requestId = 1;
  }

  async call(method, params = {}) {
    const payload = {
      jsonrpc: "2.0",
      method: method,
      params: params,
      id: this.requestId++,
    };

    try {
      const response = await axios.post(this.baseUrl, payload, {
        headers: { "Content-Type": "application/json" },
      });
      return response.data;
    } catch (error) {
      console.error("Error calling PyPI MCP:", error);
      throw error;
    }
  }

  async getPackageInfo(packageName, version = null) {
    return await this.call("tools/call", {
      name: "get_package_info",
      arguments: {
        package_name: packageName,
        ...(version && { version }),
      },
    });
  }

  async searchPackages(query, limit = 10) {
    return await this.call("tools/call", {
      name: "search_packages",
      arguments: { query, limit },
    });
  }
}

// Example usage
async function main() {
  const client = new PyPIMCPClient();

  // Initialize
  await client.call("initialize");

  // Get package info
  const packageInfo = await client.getPackageInfo("fastapi");
  console.log("FastAPI info:", packageInfo);

  // Search packages
  const searchResults = await client.searchPackages("web framework");
  console.log("Search results:", searchResults);
}

main().catch(console.error);
```

## Docker Integration

### Running in Docker

Create a Dockerfile for containerized deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone and install PyPI MCP
RUN git clone https://github.com/AstroAir/pypi-mcp.git .
RUN pip install -e .

# Expose port for HTTP transport
EXPOSE 8000

# Default command
CMD ["pypi-mcp", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
# Build the image
docker build -t pypi-mcp .

# Run with STDIO transport
docker run -it pypi-mcp pypi-mcp

# Run with HTTP transport
docker run -p 8000:8000 pypi-mcp

# Run with environment variables
docker run -p 8000:8000 \
  -e PYPI_MCP_LOG_LEVEL=DEBUG \
  -e PYPI_MCP_CACHE_TTL=600 \
  pypi-mcp
```

### Docker Compose

For more complex deployments, use Docker Compose:

```yaml
version: "3.8"

services:
  pypi-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYPI_MCP_LOG_LEVEL=INFO
      - PYPI_MCP_CACHE_TTL=600
      - PYPI_MCP_RATE_LIMIT=20.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Kubernetes Deployment

Deploy to Kubernetes with this configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pypi-mcp
  labels:
    app: pypi-mcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pypi-mcp
  template:
    metadata:
      labels:
        app: pypi-mcp
    spec:
      containers:
        - name: pypi-mcp
          image: pypi-mcp:latest
          ports:
            - containerPort: 8000
          env:
            - name: PYPI_MCP_LOG_LEVEL
              value: "INFO"
            - name: PYPI_MCP_CACHE_TTL
              value: "600"
            - name: PYPI_MCP_RATE_LIMIT
              value: "20.0"
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: pypi-mcp-service
spec:
  selector:
    app: pypi-mcp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Custom MCP Client Integration

### Protocol Overview

The PyPI MCP Server implements the Model Context Protocol. Here's how to integrate with a custom client:

1. **Initialize**: Send an `initialize` request
2. **List Tools**: Call `tools/list` to get available tools
3. **Call Tools**: Use `tools/call` to execute specific tools
4. **Access Resources**: Use `resources/read` for static resources

### Example Integration Flow

```python
import json
import subprocess
import asyncio

class CustomMCPClient:
    def __init__(self):
        self.process = None

    async def start(self):
        """Start the PyPI MCP server process."""
        self.process = await asyncio.create_subprocess_exec(
            'pypi-mcp',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

    async def send_request(self, method, params=None):
        """Send a JSON-RPC request to the server."""
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

    async def initialize(self):
        """Initialize the MCP session."""
        return await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "custom-client",
                "version": "1.0.0"
            }
        })

    async def list_tools(self):
        """List available tools."""
        return await self.send_request("tools/list")

    async def call_tool(self, name, arguments):
        """Call a specific tool."""
        return await self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })

    async def close(self):
        """Close the connection."""
        if self.process:
            self.process.terminate()
            await self.process.wait()

# Example usage
async def main():
    client = CustomMCPClient()
    await client.start()

    try:
        # Initialize
        init_result = await client.initialize()
        print("Initialized:", init_result)

        # List tools
        tools = await client.list_tools()
        print("Available tools:", [tool['name'] for tool in tools['tools']])

        # Call a tool
        result = await client.call_tool("get_package_info", {
            "package_name": "requests"
        })
        print("Package info:", result)

    finally:
        await client.close()

asyncio.run(main())
```

## Integration Best Practices

### Performance Optimization

1. **Enable Caching**: Set appropriate cache TTL values
2. **Rate Limiting**: Configure rate limits based on your usage patterns
3. **Connection Pooling**: Reuse connections when possible
4. **Batch Requests**: Group related requests when possible

### Error Handling

1. **Retry Logic**: Implement exponential backoff for transient failures
2. **Timeout Handling**: Set appropriate timeouts for your use case
3. **Graceful Degradation**: Handle server unavailability gracefully
4. **Logging**: Log integration events for debugging

### Security Considerations

1. **Network Security**: Use HTTPS in production environments
2. **Access Control**: Implement authentication if needed
3. **Input Validation**: Validate all inputs before sending to the server
4. **Resource Limits**: Set appropriate resource limits in containerized environments

## Next Steps

- [Configuration Guide](../user-guide/configuration.md) - Customize server behavior
- [API Reference](../api-reference/tools.md) - Explore all available tools
- [Troubleshooting](../troubleshooting/common-issues.md) - Solve integration issues
