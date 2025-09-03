"""Main FastMCP server for PyPI package information."""

import logging
from typing import Dict, List, Optional

from fastmcp import FastMCP

from .cache import get_cache_stats
from .client import client
from .config import settings
from .exceptions import PackageNotFoundError, PyPIMCPError, ValidationError
from .utils import classify_version_type
from .utils import compare_versions as compare_version_strings
from .utils import (extract_keywords, format_file_size,
                    get_package_type_description, is_version_compatible,
                    parse_requirements,
                    validate_package_name, validate_version)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format=settings.log_format,
)
logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""

    mcp = FastMCP(
        name=settings.server_name,
        instructions="""
        This server provides comprehensive PyPI package information and management tools.
        Use these tools to search for packages, get detailed metadata, analyze dependencies,
        check for vulnerabilities, and manage Python package information.
        
        Key capabilities:
        - Package discovery and search
        - Detailed package metadata retrieval
        - Version management and comparison
        - Dependency analysis
        - Security vulnerability checking
        - Package statistics and analytics
        """,
    )

    @mcp.tool
    async def get_package_info(
        package_name: str,
        version: Optional[str] = None,
        include_files: bool = False,
    ) -> Dict:
        """
        Get detailed information about a PyPI package.

        Args:
            package_name: Name of the package to look up
            version: Specific version to get info for (latest if not specified)
            include_files: Whether to include file information in the response

        Returns:
            Detailed package information including metadata, dependencies, and files
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        if version and not validate_version(version):
            raise ValidationError("version", version, "Invalid version format")

        async with client:
            try:
                package_info = await client.get_package_info(package_name, version)

                result = {
                    "name": package_info.name,
                    "version": package_info.version,
                    "summary": package_info.summary,
                    "description": (
                        package_info.description[:500] + "..."
                        if len(package_info.description) > 500
                        else package_info.description
                    ),
                    "author": package_info.author,
                    "author_email": package_info.author_email,
                    "maintainer": package_info.maintainer,
                    "maintainer_email": package_info.maintainer_email,
                    "license": package_info.license,
                    "home_page": package_info.home_page,
                    "project_urls": package_info.project_urls,
                    "classifiers": package_info.classifiers,
                    "keywords": extract_keywords(package_info.keywords),
                    "requires_python": package_info.requires_python,
                    "dependencies": [
                        dep.dict()
                        for dep in parse_requirements(package_info.requires_dist)
                    ],
                    "extras": package_info.provides_extra,
                    "yanked": package_info.yanked,
                    "yanked_reason": package_info.yanked_reason,
                    "package_url": str(package_info.package_url),
                    "project_url": str(package_info.project_url),
                    "release_url": str(package_info.release_url),
                    "version_type": classify_version_type(package_info.version),
                    "vulnerabilities": [
                        vuln.dict() for vuln in package_info.vulnerabilities
                    ],
                }

                if include_files:
                    result["files"] = [
                        {
                            "filename": file.filename,
                            "url": str(file.url),
                            "size": file.size,
                            "size_formatted": format_file_size(file.size),
                            "type": get_package_type_description(file.packagetype),
                            "python_version": file.python_version,
                            "upload_time": file.upload_time.isoformat(),
                            "yanked": file.yanked,
                        }
                        for file in package_info.files
                    ]

                return result

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package not found: {e.message}")

    @mcp.tool
    async def get_package_versions(
        package_name: str,
        limit: Optional[int] = None,
        include_prereleases: bool = True,
    ) -> Dict:
        """
        Get all available versions of a package.

        Args:
            package_name: Name of the package
            limit: Maximum number of versions to return (all if not specified)
            include_prereleases: Whether to include pre-release versions

        Returns:
            List of versions with metadata
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        async with client:
            try:
                versions = await client.get_package_versions(package_name)

                # Filter and classify versions
                version_info = []
                for version in versions:
                    version_type = classify_version_type(version)

                    if not include_prereleases and version_type != "stable":
                        continue

                    version_info.append(
                        {
                            "version": version,
                            "type": version_type,
                            "is_latest": version == versions[0] if versions else False,
                        }
                    )

                if limit:
                    version_info = version_info[:limit]

                return {
                    "package_name": package_name,
                    "total_versions": len(versions),
                    "returned_versions": len(version_info),
                    "latest_version": versions[0] if versions else None,
                    "versions": version_info,
                }

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package not found: {e.message}")

    @mcp.tool
    async def search_packages(
        query: str,
        limit: int = 10,
        include_description: bool = False,
    ) -> Dict:
        """
        Search for packages by name or keywords.

        Args:
            query: Search query (package name or keywords)
            limit: Maximum number of results to return
            include_description: Whether to include package descriptions

        Returns:
            List of matching packages with relevance scores
        """
        if not query.strip():
            raise ValidationError("query", query, "Search query cannot be empty")

        if limit <= 0 or limit > 100:
            raise ValidationError(
                "limit", str(limit), "Limit must be between 1 and 100"
            )

        # Simple search implementation - in a real implementation,
        # you might want to use a proper search index or PyPI's search API
        results = []

        # Try exact match first
        if validate_package_name(query):
            async with client:
                try:
                    package_info = await client.get_package_info(query)
                    results.append(
                        {
                            "name": package_info.name,
                            "version": package_info.version,
                            "summary": package_info.summary,
                            "description": (
                                package_info.description[:200] + "..."
                                if include_description
                                and len(package_info.description) > 200
                                else ""
                            ),
                            "author": package_info.author,
                            "keywords": extract_keywords(package_info.keywords),
                            "score": 1.0,
                        }
                    )
                except PackageNotFoundError:
                    pass

        # For a more comprehensive search, you would need to:
        # 1. Use PyPI's search API (if available)
        # 2. Maintain a local index of packages
        # 3. Use external search services

        return {
            "query": query,
            "total_results": len(results),
            "results": results[:limit],
        }

    @mcp.tool
    async def compare_versions(
        package_name: str,
        version1: str,
        version2: str,
    ) -> Dict:
        """
        Compare two versions of a package.

        Args:
            package_name: Name of the package
            version1: First version to compare
            version2: Second version to compare

        Returns:
            Comparison result with detailed information
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        if not validate_version(version1):
            raise ValidationError("version1", version1, "Invalid version format")

        if not validate_version(version2):
            raise ValidationError("version2", version2, "Invalid version format")

        async with client:
            try:
                # Get info for both versions
                info1 = await client.get_package_info(package_name, version1)
                info2 = await client.get_package_info(package_name, version2)

                comparison_result = compare_version_strings(version1, version2)

                return {
                    "package_name": package_name,
                    "version1": {
                        "version": version1,
                        "type": classify_version_type(version1),
                        "upload_time": (
                            info1.files[0].upload_time.isoformat()
                            if info1.files
                            else None
                        ),
                        "dependencies_count": len(info1.requires_dist),
                        "vulnerabilities_count": len(info1.vulnerabilities),
                    },
                    "version2": {
                        "version": version2,
                        "type": classify_version_type(version2),
                        "upload_time": (
                            info2.files[0].upload_time.isoformat()
                            if info2.files
                            else None
                        ),
                        "dependencies_count": len(info2.requires_dist),
                        "vulnerabilities_count": len(info2.vulnerabilities),
                    },
                    "comparison": {
                        "result": comparison_result,
                        "newer_version": (
                            version1
                            if comparison_result > 0
                            else version2 if comparison_result < 0 else "equal"
                        ),
                        "is_upgrade": comparison_result > 0,
                        "is_downgrade": comparison_result < 0,
                    },
                }

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package or version not found: {e.message}")

    @mcp.tool
    async def check_compatibility(
        package_name: str,
        version: Optional[str] = None,
        python_version: str = "3.11",
    ) -> Dict:
        """
        Check Python version compatibility for a package.

        Args:
            package_name: Name of the package
            version: Package version (latest if not specified)
            python_version: Python version to check compatibility against

        Returns:
            Compatibility information
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        if version and not validate_version(version):
            raise ValidationError("version", version, "Invalid version format")

        async with client:
            try:
                package_info = await client.get_package_info(package_name, version)

                is_compatible = True
                compatibility_notes = []

                if package_info.requires_python:
                    try:
                        is_compatible = is_version_compatible(
                            python_version, package_info.requires_python
                        )
                        if not is_compatible:
                            compatibility_notes.append(
                                f"Python {python_version} does not satisfy requirement: {package_info.requires_python}"
                            )
                    except Exception:
                        compatibility_notes.append(
                            f"Could not parse Python requirement: {package_info.requires_python}"
                        )

                return {
                    "package_name": package_info.name,
                    "package_version": package_info.version,
                    "python_version": python_version,
                    "is_compatible": is_compatible,
                    "requires_python": package_info.requires_python,
                    "compatibility_notes": compatibility_notes,
                    "classifiers": [
                        c
                        for c in package_info.classifiers
                        if "Programming Language :: Python" in c
                    ],
                }

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package not found: {e.message}")

    @mcp.tool
    async def get_dependencies(
        package_name: str,
        version: Optional[str] = None,
        include_extras: bool = False,
    ) -> Dict:
        """
        Get package dependencies with detailed analysis.

        Args:
            package_name: Name of the package
            version: Package version (latest if not specified)
            include_extras: Whether to include optional dependencies

        Returns:
            Detailed dependency information
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        if version and not validate_version(version):
            raise ValidationError("version", version, "Invalid version format")

        async with client:
            try:
                package_info = await client.get_package_info(package_name, version)

                dependencies = parse_requirements(package_info.requires_dist)

                # Categorize dependencies
                runtime_deps = []
                dev_deps = []
                optional_deps: Dict[str, List[str]] = {}

                for dep in dependencies:
                    if dep.environment_marker:
                        if "extra ==" in dep.environment_marker:
                            # Extract extra name
                            extra_match = (
                                dep.environment_marker.split("extra ==")[1]
                                .strip()
                                .strip("\"'")
                            )
                            if extra_match not in optional_deps:
                                optional_deps[extra_match] = []
                            optional_deps[extra_match].append(dep.dict())
                        elif any(
                            marker in dep.environment_marker
                            for marker in ["dev", "test", "lint"]
                        ):
                            dev_deps.append(dep.dict())
                        else:
                            runtime_deps.append(dep.dict())
                    else:
                        runtime_deps.append(dep.dict())

                result = {
                    "package_name": package_info.name,
                    "package_version": package_info.version,
                    "total_dependencies": len(dependencies),
                    "runtime_dependencies": runtime_deps,
                    "development_dependencies": dev_deps,
                    "available_extras": list(package_info.provides_extra),
                }

                if include_extras:
                    result["optional_dependencies"] = optional_deps

                return result

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package not found: {e.message}")

    @mcp.tool
    async def check_vulnerabilities(
        package_name: str,
        version: Optional[str] = None,
    ) -> Dict:
        """
        Check for known security vulnerabilities in a package.

        Args:
            package_name: Name of the package
            version: Package version (latest if not specified)

        Returns:
            Security vulnerability information
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        if version and not validate_version(version):
            raise ValidationError("version", version, "Invalid version format")

        async with client:
            try:
                package_info = await client.get_package_info(package_name, version)

                vulnerabilities = []
                for vuln in package_info.vulnerabilities:
                    vulnerabilities.append(
                        {
                            "id": vuln.id,
                            "source": vuln.source,
                            "summary": vuln.summary,
                            "details": vuln.details,
                            "aliases": vuln.aliases,
                            "fixed_in": vuln.fixed_in,
                            "link": str(vuln.link) if vuln.link else None,
                            "withdrawn": (
                                vuln.withdrawn.isoformat() if vuln.withdrawn else None
                            ),
                            "severity": (
                                "high"
                                if any(
                                    alias.startswith("CVE-") for alias in vuln.aliases
                                )
                                else "medium"
                            ),
                        }
                    )

                return {
                    "package_name": package_info.name,
                    "package_version": package_info.version,
                    "vulnerability_count": len(vulnerabilities),
                    "has_vulnerabilities": len(vulnerabilities) > 0,
                    "vulnerabilities": vulnerabilities,
                    "security_status": "vulnerable" if vulnerabilities else "secure",
                    "recommendation": (
                        "Update to a patched version"
                        if vulnerabilities
                        else "No known vulnerabilities"
                    ),
                }

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package not found: {e.message}")

    @mcp.tool
    async def get_pypi_stats() -> Dict:
        """
        Get overall PyPI statistics and top packages.

        Returns:
            PyPI statistics including top packages by size
        """
        async with client:
            try:
                stats = await client.get_pypi_stats()

                # Format top packages
                top_packages = []
                for name, info in list(stats.top_packages.items())[:20]:  # Top 20
                    top_packages.append(
                        {
                            "name": name,
                            "size": info["size"],
                            "size_formatted": format_file_size(info["size"]),
                        }
                    )

                return {
                    "total_packages_size": stats.total_packages_size,
                    "total_size_formatted": format_file_size(stats.total_packages_size),
                    "top_packages_count": len(top_packages),
                    "top_packages": top_packages,
                    "last_updated": "real-time",
                }

            except Exception as e:
                logger.warning(f"Failed to get PyPI stats: {e}")
                return {
                    "error": "Unable to retrieve PyPI statistics",
                    "message": str(e),
                }

    @mcp.tool
    async def get_package_health(
        package_name: str,
        version: Optional[str] = None,
    ) -> Dict:
        """
        Assess package health and maintenance status.

        Args:
            package_name: Name of the package
            version: Package version (latest if not specified)

        Returns:
            Package health assessment
        """
        if not validate_package_name(package_name):
            raise ValidationError(
                "package_name", package_name, "Invalid package name format"
            )

        if version and not validate_version(version):
            raise ValidationError("version", version, "Invalid version format")

        async with client:
            try:
                package_info = await client.get_package_info(package_name, version)
                versions = await client.get_package_versions(package_name)

                # Calculate health metrics
                health_score = 100
                health_notes = []

                # Check for vulnerabilities
                if package_info.vulnerabilities:
                    health_score -= 30
                    health_notes.append(
                        f"Has {len(package_info.vulnerabilities)} known vulnerabilities"
                    )

                # Check if yanked
                if package_info.yanked:
                    health_score -= 50
                    health_notes.append("Version is yanked")

                # Check version freshness
                version_type = classify_version_type(package_info.version)
                if version_type == "pre-release":
                    health_score -= 10
                    health_notes.append("Using pre-release version")

                # Check for basic metadata
                if not package_info.description:
                    health_score -= 5
                    health_notes.append("Missing description")

                if not package_info.home_page and not package_info.project_urls:
                    health_score -= 5
                    health_notes.append("Missing project URLs")

                # Determine health status
                if health_score >= 80:
                    health_status = "excellent"
                elif health_score >= 60:
                    health_status = "good"
                elif health_score >= 40:
                    health_status = "fair"
                else:
                    health_status = "poor"

                return {
                    "package_name": package_info.name,
                    "package_version": package_info.version,
                    "health_score": max(0, health_score),
                    "health_status": health_status,
                    "health_notes": health_notes,
                    "total_versions": len(versions),
                    "is_latest": (
                        package_info.version == versions[0] if versions else False
                    ),
                    "has_vulnerabilities": len(package_info.vulnerabilities) > 0,
                    "is_yanked": package_info.yanked,
                    "version_type": version_type,
                }

            except PackageNotFoundError as e:
                raise PyPIMCPError(f"Package not found: {e.message}")

    @mcp.tool
    async def get_cache_info() -> Dict:
        """
        Get information about the server's cache status.

        Returns:
            Cache statistics and configuration
        """
        stats = await get_cache_stats()
        return {
            "cache_stats": stats,
            "cache_enabled": True,
            "cache_ttl_seconds": settings.cache_ttl,
        }

    # Resources
    @mcp.resource("pypi://stats/overview")
    async def pypi_stats_resource() -> str:
        """Provides PyPI statistics overview."""
        async with client:
            try:
                stats = await client.get_pypi_stats()
                return f"""PyPI Statistics Overview:
- Total packages size: {format_file_size(stats.total_packages_size)}
- Top packages tracked: {len(stats.top_packages)}
- Data source: PyPI API
- Last updated: Real-time"""
            except Exception:
                return "PyPI statistics are currently unavailable."

    @mcp.resource("pypi://package/{package_name}")
    async def package_resource(package_name: str) -> str:
        """Provides package metadata as a resource."""
        async with client:
            try:
                package_info = await client.get_package_info(package_name)
                return f"""Package: {package_info.name}
Version: {package_info.version}
Summary: {package_info.summary}
Author: {package_info.author}
License: {package_info.license}
Homepage: {package_info.home_page}
Dependencies: {len(package_info.requires_dist)}
Vulnerabilities: {len(package_info.vulnerabilities)}"""
            except PackageNotFoundError:
                return f"Package '{package_name}' not found on PyPI."

    # Prompts
    @mcp.prompt
    async def analyze_package(package_name: str, version: Optional[str] = None) -> str:
        """Generate a comprehensive package analysis prompt."""
        return f"""Please analyze the PyPI package '{package_name}'{f' version {version}' if version else ''}.

Consider the following aspects:
1. Package purpose and functionality
2. Maintenance status and community health
3. Security considerations and known vulnerabilities
4. Dependencies and their implications
5. Compatibility with different Python versions
6. Documentation quality and project maturity
7. Alternative packages and comparisons
8. Recommendations for usage

Use the available PyPI tools to gather detailed information about this package."""

    @mcp.prompt
    async def compare_packages(package1: str, package2: str) -> str:
        """Generate a package comparison prompt."""
        return f"""Please compare the PyPI packages '{package1}' and '{package2}'.

Analyze and compare:
1. Functionality and feature sets
2. Performance characteristics
3. Community adoption and popularity
4. Maintenance and development activity
5. Security track record
6. Documentation quality
7. Dependencies and ecosystem impact
8. Learning curve and ease of use
9. License compatibility
10. Recommendations for different use cases

Use the PyPI tools to gather comprehensive information about both packages."""

    @mcp.prompt
    async def security_review(package_name: str) -> str:
        """Generate a security review prompt for a package."""
        return f"""Please conduct a security review of the PyPI package '{package_name}'.

Focus on:
1. Known vulnerabilities and CVEs
2. Dependency security analysis
3. Package integrity and authenticity
4. Maintenance status and update frequency
5. Security best practices in the codebase
6. Trust indicators (maintainer reputation, project maturity)
7. Potential security risks and mitigations
8. Recommendations for secure usage

Use the vulnerability checking and package analysis tools to gather security-relevant information."""

    return mcp


def main():
    """Main entry point for the PyPI MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="PyPI MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol to use",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host to bind to (HTTP transport only)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to (HTTP transport only)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=settings.log_level,
        help="Logging level",
    )

    args = parser.parse_args()

    # Update log level if specified
    if args.log_level != settings.log_level:
        logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Create and run server
    server = create_server()

    logger.info(f"Starting PyPI MCP Server with {args.transport} transport")

    if args.transport == "stdio":
        server.run()
    else:
        server.run(transport="http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
