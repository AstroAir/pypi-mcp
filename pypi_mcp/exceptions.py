"""Custom exceptions for the PyPI MCP server."""

from typing import Optional


class PyPIMCPError(Exception):
    """Base exception for PyPI MCP server errors."""

    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(message)


class PackageNotFoundError(PyPIMCPError):
    """Raised when a package is not found on PyPI."""

    def __init__(self, package_name: str):
        super().__init__(f"Package '{package_name}' not found on PyPI")
        self.package_name = package_name


class VersionNotFoundError(PyPIMCPError):
    """Raised when a specific version of a package is not found."""

    def __init__(self, package_name: str, version: str):
        super().__init__(f"Version '{version}' of package '{package_name}' not found")
        self.package_name = package_name
        self.version = version


class PyPIAPIError(PyPIMCPError):
    """Raised when there's an error communicating with the PyPI API."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(PyPIAPIError):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: Optional[int] = None):
        message = "Rate limit exceeded"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message)
        self.retry_after = retry_after


class ValidationError(PyPIMCPError):
    """Raised when input validation fails."""

    def __init__(self, field: str, value: str, reason: str):
        super().__init__(f"Invalid {field}: '{value}' - {reason}")
        self.field = field
        self.value = value
        self.reason = reason
