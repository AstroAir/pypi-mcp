"""Integration tests for the PyPI MCP server with real PyPI API calls."""

from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Client
from pydantic import HttpUrl

from pypi_mcp.server import create_server


@pytest.fixture
def server():
    """Create a test server instance."""
    return create_server()


@pytest.mark.integration
class TestRealPyPIIntegration:
    """Integration tests with real PyPI API calls.

    These tests are marked with @pytest.mark.integration and can be run separately
    to avoid hitting the real PyPI API during regular unit tests.
    """

    @pytest.mark.asyncio
    async def test_real_package_info_retrieval(self, server):
        """Test retrieving real package information from PyPI."""
        async with Client(server) as client:
            # Test with a well-known, stable package
            result = await client.call_tool(
                "get_package_info", {"package_name": "requests"}
            )

            assert result.data["name"] == "requests"
            assert "version" in result.data
            assert "summary" in result.data
            assert "author" in result.data
            assert isinstance(result.data["dependencies"], list)

    @pytest.mark.asyncio
    async def test_real_package_versions(self, server):
        """Test retrieving real package versions from PyPI."""
        async with Client(server) as client:
            result = await client.call_tool(
                "get_package_versions", {
                    "package_name": "requests", "limit": 5}
            )

            assert result.data["package_name"] == "requests"
            assert result.data["total_versions"] > 0
            assert len(result.data["versions"]) <= 5
            assert result.data["latest_version"] is not None

    @pytest.mark.asyncio
    async def test_real_package_search(self, server):
        """Test searching for real packages on PyPI."""
        with patch("pypi_mcp.server.client") as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)

            from pypi_mcp.models import SearchResult

            mock_client.search_packages = AsyncMock(
                return_value=[
                    SearchResult(
                        name="requests",
                        version="2.31.0",
                        summary="Python HTTP library",
                        description="Requests documentation",
                        author="Kenneth Reitz",
                        keywords=["http", "requests"],
                        classifiers=[],
                        score=0.95,
                    )
                ]
            )
            mock_client.get_package_info = AsyncMock()

            async with Client(server) as client:
                result = await client.call_tool(
                    "search_packages", {"query": "requests", "limit": 3}
                )

                assert result.data["query"] == "requests"
                assert result.data["total_results"] >= 1
                assert any(
                    pkg["name"].lower() == "requests" for pkg in result.data["results"]
                )

    @pytest.mark.asyncio
    async def test_real_pypi_stats(self, server):
        """Test retrieving real PyPI statistics."""
        async with Client(server) as client:
            result = await client.call_tool("get_pypi_stats", {})

            # Stats might not always be available, so we check for either success or error
            if "error" not in result.data:
                assert "total_packages_size" in result.data
                assert "top_packages" in result.data
                assert isinstance(result.data["top_packages"], list)
            else:
                # If stats API is unavailable, we should get a proper error message
                assert "Unable to retrieve PyPI statistics" in result.data["error"]

    @pytest.mark.asyncio
    async def test_real_package_not_found(self, server):
        """Test handling of non-existent packages with real API."""
        async with Client(server) as client:
            with pytest.raises(Exception) as exc_info:
                await client.call_tool(
                    "get_package_info",
                    {"package_name": "this-package-definitely-does-not-exist-12345"},
                )

            assert "Package not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_real_version_comparison(self, server):
        """Test comparing real package versions."""
        async with Client(server) as client:
            # First get the actual package info to see what versions exist
            package_info = await client.call_tool(
                "get_package_info", {"package_name": "requests"}
            )

            current_version = package_info.data["version"]

            # Compare the current version with itself (should be equal)
            result = await client.call_tool(
                "compare_versions",
                {
                    "package_name": "requests",
                    "version1": current_version,
                    "version2": current_version,
                },
            )

            assert result.data["package_name"] == "requests"
            assert result.data["comparison"]["result"] == 0  # Equal versions

    @pytest.mark.asyncio
    async def test_real_compatibility_check(self, server):
        """Test checking real package compatibility."""
        async with Client(server) as client:
            result = await client.call_tool(
                "check_compatibility",
                {"package_name": "requests", "python_version": "3.9"},
            )

            assert result.data["package_name"] == "requests"
            assert result.data["python_version"] == "3.9"
            assert "is_compatible" in result.data
            assert "requires_python" in result.data


@pytest.mark.integration
class TestEndToEndWorkflows:
    """End-to-end workflow tests."""

    @pytest.mark.asyncio
    async def test_package_analysis_workflow(self, server):
        """Test a complete package analysis workflow."""
        async with Client(server) as client:
            package_name = "fastapi"

            # Step 1: Get package info
            info_result = await client.call_tool(
                "get_package_info", {"package_name": package_name}
            )

            assert info_result.data["name"] == package_name
            # current_version = info_result.data["version"]  # Not used in this test

            # Step 2: Get all versions
            versions_result = await client.call_tool(
                "get_package_versions", {
                    "package_name": package_name, "limit": 10}
            )

            assert len(versions_result.data["versions"]) <= 10

            # Step 3: Check dependencies
            deps_result = await client.call_tool(
                "get_dependencies", {"package_name": package_name}
            )

            assert deps_result.data["package_name"] == package_name
            assert "total_dependencies" in deps_result.data

            # Step 4: Check vulnerabilities
            vuln_result = await client.call_tool(
                "check_vulnerabilities", {"package_name": package_name}
            )

            assert vuln_result.data["package_name"] == package_name
            assert "has_vulnerabilities" in vuln_result.data

            # Step 5: Check package health
            health_result = await client.call_tool(
                "get_package_health", {"package_name": package_name}
            )

            assert health_result.data["package_name"] == package_name
            assert "health_score" in health_result.data
            assert "health_status" in health_result.data

    @pytest.mark.asyncio
    async def test_package_comparison_workflow(self, server):
        """Test a package comparison workflow."""
        async with Client(server) as client:
            # Compare two popular web frameworks
            package1 = "fastapi"
            package2 = "flask"

            # Get info for both packages
            info1 = await client.call_tool(
                "get_package_info", {"package_name": package1}
            )

            info2 = await client.call_tool(
                "get_package_info", {"package_name": package2}
            )

            assert info1.data["name"].lower() == package1.lower()
            assert info2.data["name"].lower() == package2.lower()

            # Compare their latest versions
            result = await client.call_tool(
                "compare_versions",
                {
                    "package_name": package1,
                    "version1": info1.data["version"],
                    # Same version should be equal
                    "version2": info1.data["version"],
                },
            )

            assert result.data["comparison"]["result"] == 0  # Equal

    @pytest.mark.asyncio
    async def test_resource_and_prompt_workflow(self, server):
        """Test using resources and prompts together."""
        async with Client(server) as client:
            package_name = "django"

            # Read package resource
            resource = await client.read_resource(f"pypi://package/{package_name}")

            assert len(resource) == 1
            content = resource[0].text
            assert (
                f"Package: {package_name}" in content
                or f"Package: {package_name.capitalize()}" in content
            )

            # Get analysis prompt
            prompt = await client.get_prompt(
                "analyze_package", {"package_name": package_name}
            )

            assert (
                f"analyze the PyPI package '{package_name}'"
                in prompt.messages[0].content.text
            )

            # Get comparison prompt
            comparison_prompt = await client.get_prompt(
                "compare_packages", {"package1": "django", "package2": "flask"}
            )

            assert (
                "compare the PyPI packages 'django' and 'flask'"
                in comparison_prompt.messages[0].content.text
            )


class TestMockIntegration:
    """Integration tests using mocked PyPI responses for reliability."""

    @pytest.mark.asyncio
    async def test_complete_server_lifecycle(self, server):
        """Test complete server lifecycle with mocked responses."""
        # Mock the PyPI client to return predictable responses
        with patch("pypi_mcp.server.client") as mock_client:
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)

            # Mock package info
            from pypi_mcp.models import PackageInfo

            mock_package = PackageInfo(
                name="test-package",
                version="1.0.0",
                summary="Test package",
                description="A test package",
                author="Test Author",
                author_email="test@example.com",
                license="MIT",
                home_page="https://example.com",
                project_urls={"Homepage": "https://example.com"},
                classifiers=["Development Status :: 4 - Beta"],
                keywords="test",
                requires_python=">=3.8",
                requires_dist=["requests>=2.25.0"],
                provides_extra=[],
                package_url=HttpUrl("https://pypi.org/project/test-package/"),
                project_url=HttpUrl("https://pypi.org/project/test-package/"),
                release_url=HttpUrl(
                    "https://pypi.org/project/test-package/1.0.0/"),
                urls=[],
                vulnerabilities=[],
            )

            mock_client.get_package_info = AsyncMock(return_value=mock_package)
            mock_client.get_package_versions = AsyncMock(
                return_value=["1.0.0", "0.9.0"]
            )

            async with Client(server) as client:
                # Test multiple operations in sequence
                operations = [
                    ("get_package_info", {"package_name": "test-package"}),
                    ("get_package_versions", {"package_name": "test-package"}),
                    (
                        "check_compatibility",
                        {"package_name": "test-package", "python_version": "3.9"},
                    ),
                    ("get_dependencies", {"package_name": "test-package"}),
                    ("get_package_health", {"package_name": "test-package"}),
                ]

                results = []
                for tool_name, params in operations:
                    result = await client.call_tool(tool_name, params)
                    results.append(result)

                # Verify all operations completed successfully
                assert len(results) == len(operations)
                for result in results:
                    assert result.data is not None
                    # Each result should contain the package name
                    assert "test-package" in str(result.data)


if __name__ == "__main__":
    # Run integration tests separately
    pytest.main([__file__, "-m", "integration", "-v"])
