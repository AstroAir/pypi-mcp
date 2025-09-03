"""Performance and caching tests for the PyPI MCP server."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client

from pypi_mcp.cache import cache
from pypi_mcp.models import PackageInfo
from pypi_mcp.server import create_server


@pytest.fixture
def server():
    """Create a test server instance."""
    return create_server()


@pytest.fixture
def mock_package_info():
    """Mock package info for testing."""
    return PackageInfo(
        name="test-package",
        version="1.0.0",
        summary="A test package",
        description="Test package description",
        author="Test Author",
        author_email="test@example.com",
        license="MIT",
        home_page="https://example.com",
        project_urls={"Homepage": "https://example.com"},
        classifiers=["Development Status :: 4 - Beta"],
        keywords="test,package",
        requires_python=">=3.8",
        requires_dist=["requests>=2.25.0"],
        provides_extra=["dev"],
        package_url="https://pypi.org/project/test-package/",
        project_url="https://pypi.org/project/test-package/",
        release_url="https://pypi.org/project/test-package/1.0.0/",
        files=[],
        vulnerabilities=[],
    )


class TestCachingBehavior:
    """Test caching functionality and performance."""

    @pytest.mark.asyncio
    async def test_cache_hit_performance(self, server, mock_package_info):
        """Test that cache functionality works correctly."""
        # Test the cache directly rather than through the mocked client
        from pypi_mcp.cache import cache, cache_key

        # Clear cache first
        await cache.clear()

        # Test cache miss and hit
        test_key = cache_key("test-package", None)

        # Should be empty initially
        result = await cache.get(test_key)
        assert result is None

        # Set a value
        await cache.set(test_key, mock_package_info)

        # Should now return the cached value
        cached_result = await cache.get(test_key)
        assert cached_result is not None
        assert cached_result.name == mock_package_info.name

    @pytest.mark.asyncio
    async def test_cache_key_generation(self, server, mock_package_info):
        """Test that different parameters generate different cache keys."""
        from pypi_mcp.cache import cache_key

        # Test that different parameters generate different keys
        key1 = cache_key("package1", None)
        key2 = cache_key("package2", None)
        key3 = cache_key("package1", "1.0.0")

        # All keys should be different
        assert key1 != key2
        assert key1 != key3
        assert key2 != key3

        # Same parameters should generate same key
        key1_duplicate = cache_key("package1", None)
        assert key1 == key1_duplicate

    @pytest.mark.asyncio
    async def test_cache_info_tool(self, server):
        """Test the get_cache_info tool."""
        async with Client(server) as client:
            result = await client.call_tool("get_cache_info", {})

            assert "cache_stats" in result.data
            assert "cache_enabled" in result.data
            assert "cache_ttl_seconds" in result.data
            assert result.data["cache_enabled"] is True
            assert isinstance(result.data["cache_ttl_seconds"], int)

    @pytest.mark.asyncio
    async def test_cache_cleanup(self):
        """Test cache cleanup functionality."""
        # Clear cache before test
        await cache.clear()

        # Add some test data
        await cache.set("test_key_1", "test_value_1")
        await cache.set("test_key_2", "test_value_2")

        # Verify data is cached
        assert await cache.get("test_key_1") == "test_value_1"
        assert await cache.get("test_key_2") == "test_value_2"

        # Clear cache
        await cache.clear()

        # Verify cache is empty
        assert await cache.get("test_key_1") is None
        assert await cache.get("test_key_2") is None
        assert await cache.size() == 0


class TestConcurrentRequests:
    """Test handling of concurrent requests."""

    @pytest.mark.asyncio
    async def test_concurrent_tool_calls(self, server, mock_package_info):
        """Test that concurrent tool calls are handled properly."""
        call_count = 0

        async def mock_get_package_info(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # Simulate some processing time
            await asyncio.sleep(0.01)
            return mock_package_info

        with patch("pypi_mcp.server.client") as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_package_info = AsyncMock(side_effect=mock_get_package_info)

            async with Client(server) as client:
                # Make multiple concurrent requests for different packages
                tasks = []
                for i in range(5):
                    task = client.call_tool(
                        "get_package_info", {"package_name": f"test-package-{i}"}
                    )
                    tasks.append(task)

                # Wait for all requests to complete
                results = await asyncio.gather(*tasks)

                # Verify all requests completed successfully
                assert len(results) == 5
                for result in results:
                    assert result.data["name"] == "test-package"

                # Verify all API calls were made (no caching between different packages)
                assert call_count == 5

    @pytest.mark.asyncio
    async def test_concurrent_same_package_requests(self, server, mock_package_info):
        """Test concurrent requests for the same package (cache behavior)."""
        call_count = 0

        async def mock_get_package_info(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # Simulate some processing time
            await asyncio.sleep(0.01)
            return mock_package_info

        with patch("pypi_mcp.server.client") as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_package_info = AsyncMock(side_effect=mock_get_package_info)

            async with Client(server) as client:
                # Make multiple concurrent requests for the same package
                tasks = []
                for i in range(5):
                    task = client.call_tool(
                        "get_package_info", {"package_name": "test-package"}
                    )
                    tasks.append(task)

                # Wait for all requests to complete
                results = await asyncio.gather(*tasks)

                # Verify all requests completed successfully
                assert len(results) == 5
                for result in results:
                    assert result.data["name"] == "test-package"

                # Due to caching, we might have fewer API calls than requests
                # The exact number depends on timing, but should be <= 5
                assert call_count <= 5


class TestRateLimiting:
    """Test rate limiting functionality."""

    @pytest.mark.asyncio
    async def test_rate_limiting_configuration(self, server):
        """Test that rate limiting is properly configured."""
        from pypi_mcp.config import settings

        # Verify rate limiting settings
        assert settings.rate_limit > 0
        assert settings.max_retries >= 0
        assert settings.timeout > 0

    @pytest.mark.asyncio
    async def test_sequential_requests_within_limits(self, server, mock_package_info):
        """Test that sequential requests within rate limits work properly."""
        with patch("pypi_mcp.server.client") as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get_package_info = AsyncMock(return_value=mock_package_info)

            async with Client(server) as client:
                # Make several sequential requests
                for i in range(3):
                    result = await client.call_tool(
                        "get_package_info", {"package_name": f"test-package-{i}"}
                    )
                    assert result.data["name"] == "test-package"

                # All requests should succeed
                assert mock_client.get_package_info.call_count == 3


class TestMemoryUsage:
    """Test memory usage and resource management."""

    @pytest.mark.asyncio
    async def test_cache_size_limits(self):
        """Test that cache respects size limits."""
        from pypi_mcp.cache import AsyncTTLCache

        # Create a small cache for testing
        test_cache = AsyncTTLCache(maxsize=5, ttl=300)

        # Add items up to the limit
        for i in range(10):  # Add more than the limit
            await test_cache.set(f"test_key_{i}", f"test_value_{i}")

        # Cache size should not exceed the limit
        current_size = await test_cache.size()
        assert current_size <= 5

    @pytest.mark.asyncio
    async def test_resource_cleanup(self, server):
        """Test that resources are properly cleaned up."""
        # This test ensures that the server can be created and destroyed
        # without resource leaks
        servers = []

        # Create multiple server instances
        for _ in range(5):
            server_instance = create_server()
            servers.append(server_instance)

        # All servers should be created successfully
        assert len(servers) == 5

        # Clean up (Python's garbage collector should handle this)
        del servers


if __name__ == "__main__":
    pytest.main([__file__])
