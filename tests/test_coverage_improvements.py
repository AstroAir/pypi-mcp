"""Additional tests to improve code coverage."""

import pytest
from unittest.mock import AsyncMock, patch

from fastmcp import Client
from pypi_mcp.server import create_server
from pypi_mcp.client import PyPIClient
from pypi_mcp.exceptions import PyPIAPIError, RateLimitError
from pypi_mcp.utils import (
    extract_keywords,
    get_package_type_description,
    parse_requirements,
    classify_version_type,
    is_version_compatible,
)


@pytest.fixture
def server():
    """Create a test server instance."""
    return create_server()


class TestUtilsCoverage:
    """Test uncovered utility functions."""

    def test_extract_keywords(self):
        """Test keyword extraction from package metadata."""
        # Test with string keywords
        keywords = extract_keywords("python,web,framework")
        assert "python" in keywords
        assert "web" in keywords
        assert "framework" in keywords

        # Test with semicolon separated keywords
        keywords = extract_keywords("testing; pytest; automation")
        assert "testing" in keywords
        assert "pytest" in keywords
        assert "automation" in keywords

        # Test with empty/None keywords
        keywords = extract_keywords("")
        assert keywords == []

        keywords = extract_keywords(None)
        assert keywords == []

    def test_get_package_type_description(self):
        """Test package type descriptions."""
        assert "wheel" in get_package_type_description("bdist_wheel").lower()
        assert "source" in get_package_type_description("sdist").lower()
        assert "unknown" in get_package_type_description("unknown_type").lower()

    def test_parse_requirements(self):
        """Test requirement parsing."""
        requirements = [
            "requests>=2.25.0",
            "pydantic[email]>=1.8.0",
            "pytest; extra == 'dev'",
        ]
        
        deps = parse_requirements(requirements)
        assert len(deps) >= 2  # At least requests and pydantic
        
        # Check that we can parse basic requirements
        req_names = [dep.name for dep in deps]
        assert "requests" in req_names
        assert "pydantic" in req_names

    def test_classify_version_type(self):
        """Test version classification."""
        assert classify_version_type("1.0.0") == "stable"
        assert classify_version_type("1.0.0a1") == "pre-release"
        assert classify_version_type("1.0.0b1") == "pre-release"
        assert classify_version_type("1.0.0rc1") == "pre-release"
        assert classify_version_type("1.0.0.dev1") == "pre-release"

    def test_is_version_compatible(self):
        """Test version compatibility checking."""
        # Test compatible versions
        assert is_version_compatible("3.8", ">=3.7")
        assert is_version_compatible("3.9", ">=3.8,<4.0")
        
        # Test incompatible versions
        assert not is_version_compatible("3.6", ">=3.7")
        assert not is_version_compatible("4.0", ">=3.8,<4.0")


class TestClientCoverage:
    """Test uncovered client functionality."""

    @pytest.mark.asyncio
    async def test_client_error_handling(self):
        """Test client error handling paths."""
        client = PyPIClient()

        # Test with mocked HTTP errors
        with patch('pypi_mcp.client.httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)

            # Test 429 rate limit error
            mock_response = AsyncMock()
            mock_response.status_code = 429
            mock_response.headers = {"Retry-After": "60"}
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.aclose = AsyncMock()

            with pytest.raises(RateLimitError):
                async with client:
                    await client._make_request("https://test.com")

    def test_client_initialization(self):
        """Test client initialization and basic properties."""
        client = PyPIClient()
        assert client.session is None  # Should be None before entering context
        assert hasattr(client, '_rate_limiter')  # Should have rate limiter


class TestServerCoverage:
    """Test uncovered server functionality."""

    @pytest.mark.asyncio
    async def test_server_main_function(self):
        """Test the main server function."""
        # Test that main function can be imported and called
        from pypi_mcp.server import main
        import sys

        # Mock sys.argv to avoid actual server startup
        with patch.object(sys, 'argv', ['pypi-mcp']):
            with patch('pypi_mcp.server.FastMCP.run') as mock_run:
                main()
                mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling_in_tools(self, server):
        """Test error handling in various tools."""
        with patch('pypi_mcp.server.client') as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_package_info = AsyncMock(
                side_effect=PyPIAPIError("API Error")
            )
            
            async with Client(server) as client:
                # Test that tools handle API errors gracefully
                with pytest.raises(Exception):  # Should raise some kind of error
                    await client.call_tool("get_package_info", {
                        "package_name": "nonexistent-package"
                    })


class TestCacheCoverage:
    """Test uncovered cache functionality."""

    @pytest.mark.asyncio
    async def test_cache_delete_and_clear(self):
        """Test cache delete and clear operations."""
        from pypi_mcp.cache import AsyncTTLCache
        
        cache = AsyncTTLCache(maxsize=10, ttl=300)
        
        # Add some items
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        
        # Test delete
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None
        
        # key2 should still exist
        result = await cache.get("key2")
        assert result == "value2"
        
        # Test clear
        await cache.clear()
        result = await cache.get("key2")
        assert result is None
        
        # Size should be 0
        size = await cache.size()
        assert size == 0
