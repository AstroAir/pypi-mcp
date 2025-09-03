# Installation

This guide covers different methods to install the PyPI MCP Server.

## Prerequisites

- Python 3.11 or higher
- Internet connection for PyPI API access

## Installation Methods

### Method 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is the fastest Python package manager and is recommended for this project:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install the project
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp
uv sync
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp

# Install in development mode
pip install -e .

# Or install from PyPI (when available)
pip install pypi-mcp
```

### Method 3: From Source

```bash
# Clone and install dependencies manually
git clone https://github.com/AstroAir/pypi-mcp.git
cd pypi-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastmcp>=2.12.0 httpx>=0.27.0 packaging>=23.0 cachetools>=5.3.0 pydantic>=2.0.0

# Install the package
pip install -e .
```

## Verification

Verify the installation by running:

```bash
pypi-mcp --help
```

You should see the command-line options for the PyPI MCP server:

```
usage: pypi-mcp [-h] [--transport {stdio,http}] [--host HOST] [--port PORT] [--log-level {DEBUG,INFO,WARNING,ERROR}]

PyPI MCP Server

options:
  -h, --help            show this help message and exit
  --transport {stdio,http}
                        Transport protocol to use
  --host HOST           Host to bind to (HTTP transport only)
  --port PORT           Port to bind to (HTTP transport only)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level
```

## Dependencies

The PyPI MCP server requires the following core dependencies:

- **fastmcp** (>=2.12.0) - MCP framework
- **httpx** (>=0.27.0) - Async HTTP client
- **packaging** (>=23.0) - Python package version handling
- **cachetools** (>=5.3.0) - Caching utilities
- **pydantic** (>=2.0.0) - Data validation and serialization

## System Requirements

### Minimum Requirements

- **Python**: 3.11 or higher
- **Memory**: 256 MB RAM
- **Storage**: 50 MB free space
- **Network**: Internet connection for PyPI API access

### Recommended Requirements

- **Python**: 3.12 or higher
- **Memory**: 512 MB RAM
- **Storage**: 100 MB free space
- **Network**: Stable broadband connection

## Platform Support

The PyPI MCP server is tested and supported on:

- **Linux** (Ubuntu 20.04+, CentOS 8+, Debian 11+)
- **macOS** (10.15+)
- **Windows** (10, 11)

## Docker Installation

You can also run the server using Docker:

```bash
# Build the Docker image
docker build -t pypi-mcp .

# Run with STDIO transport
docker run -it pypi-mcp

# Run with HTTP transport
docker run -p 8000:8000 pypi-mcp --transport http --host 0.0.0.0 --port 8000
```

## Troubleshooting Installation

### Common Issues

#### Python Version Issues

If you encounter Python version errors:

```bash
# Check your Python version
python --version

# Install Python 3.11+ using pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

#### Dependency Conflicts

If you encounter dependency conflicts:

```bash
# Clear package cache
pip cache purge

# Or with uv
uv cache clean

# Try installing in a fresh virtual environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -e .
```

#### Permission Issues

On Unix systems, if you encounter permission issues:

```bash
# Install in user directory
pip install --user -e .

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Getting Help

If you encounter installation issues:

1. Check the [Troubleshooting Guide](../troubleshooting/common-issues.md)
2. Search [existing issues](https://github.com/AstroAir/pypi-mcp/issues)
3. Create a [new issue](https://github.com/AstroAir/pypi-mcp/issues/new) with:
   - Your operating system and version
   - Python version
   - Complete error message
   - Installation method used

## Next Steps

After successful installation:

1. [Quick Start Guide](quick-start.md) - Get up and running quickly
2. [Configuration](../user-guide/configuration.md) - Configure the server
3. [Usage Examples](../user-guide/usage-examples.md) - See practical examples
