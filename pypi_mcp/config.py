"""Configuration management for the PyPI MCP server."""


from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the PyPI MCP server."""

    # PyPI API settings
    pypi_base_url: str = Field(
        default="https://pypi.org", description="Base URL for PyPI API"
    )

    pypi_simple_url: str = Field(
        default="https://pypi.org/simple", description="PyPI simple index URL"
    )

    # HTTP client settings
    user_agent: str = Field(
        default="pypi-mcp/0.1.0 (https://github.com/AstroAir/pypi-mcp)",
        description="User-Agent header for HTTP requests",
    )

    timeout: float = Field(
        default=30.0, description="HTTP request timeout in seconds", gt=0.0
    )

    max_retries: int = Field(
        default=3, description="Maximum number of retries for failed requests"
    )

    # Rate limiting
    rate_limit: float = Field(
        default=10.0, description="Maximum requests per second", gt=0.0
    )

    # Caching settings
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds", gt=0)

    cache_max_size: int = Field(
        default=1000, description="Maximum number of items in cache", gt=0
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")

    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
    )

    # Server settings
    server_name: str = Field(
        default="PyPI MCP Server", description="Server name for identification"
    )

    server_version: str = Field(default="0.1.0", description="Server version")

    # Feature flags
    enable_vulnerability_check: bool = Field(
        default=True, description="Enable vulnerability checking"
    )

    enable_stats: bool = Field(default=True, description="Enable statistics endpoints")

    enable_search: bool = Field(
        default=True, description="Enable package search functionality"
    )

    model_config = {
        "env_prefix": "PYPI_MCP_",
        "env_file": ".env",
        "case_sensitive": False,
    }


# Global settings instance
settings = Settings()
