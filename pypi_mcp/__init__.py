"""
PyPI MCP Server - A comprehensive Model Context Protocol server for PyPI package information.

This package provides tools for querying PyPI package information, analyzing dependencies,
checking for vulnerabilities, and managing Python package metadata through the MCP protocol.
"""

__version__ = "0.1.0"
__author__ = "PyPI MCP Contributors"
__email__ = "contributors@example.com"

from .server import create_server

__all__ = ["create_server", "__version__"]
