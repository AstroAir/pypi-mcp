#!/usr/bin/env python3
"""
Basic usage example for the PyPI MCP server.

This script demonstrates how to use the PyPI MCP server programmatically
to query package information, check dependencies, and analyze security.
"""

import asyncio
import json
from pypi_mcp.client import client
from pypi_mcp.utils import format_file_size, classify_version_type


async def demonstrate_package_info() -> None:
    """Demonstrate getting package information."""
    print("=== Package Information Demo ===")

    async with client:
        try:
            # Get info for a popular package
            package_info = await client.get_package_info("requests")

            print(f"Package: {package_info.name}")
            print(f"Version: {package_info.version}")
            print(f"Summary: {package_info.summary}")
            print(f"Author: {package_info.author}")
            print(f"License: {package_info.license}")
            print(f"Python requirement: {package_info.requires_python}")
            print(f"Dependencies: {len(package_info.requires_dist)}")
            print(f"Vulnerabilities: {len(package_info.vulnerabilities)}")

            if package_info.files:
                total_size = sum(f.size for f in package_info.files)
                print(f"Total package size: {format_file_size(total_size)}")

            print()

        except Exception as e:
            print(f"Error getting package info: {e}")


async def demonstrate_version_listing() -> None:
    """Demonstrate listing package versions."""
    print("=== Package Versions Demo ===")

    async with client:
        try:
            # Get versions for a package
            versions = await client.get_package_versions("django")

            print(f"Django has {len(versions)} versions available")
            print("Latest 10 versions:")

            for version in versions[:10]:
                version_type = classify_version_type(version)
                print(f"  {version} ({version_type})")

            print()

        except Exception as e:
            print(f"Error getting versions: {e}")


async def demonstrate_stats() -> None:
    """Demonstrate PyPI statistics."""
    print("=== PyPI Statistics Demo ===")

    async with client:
        try:
            stats = await client.get_pypi_stats()

            print(
                f"Total PyPI size: {format_file_size(stats.total_packages_size)}")
            print("Top 5 largest packages:")

            for i, (name, info) in enumerate(list(stats.top_packages.items())[:5]):
                size = info.get("size", 0)
                print(f"  {i+1}. {name}: {format_file_size(size)}")

            print()

        except Exception as e:
            print(f"Error getting stats: {e}")


async def demonstrate_dependency_analysis() -> None:
    """Demonstrate dependency analysis."""
    print("=== Dependency Analysis Demo ===")

    async with client:
        try:
            # Analyze dependencies for FastAPI
            package_info = await client.get_package_info("fastapi")

            print(
                f"Analyzing dependencies for {package_info.name} {package_info.version}")
            print(f"Total dependencies: {len(package_info.requires_dist)}")

            if package_info.requires_dist:
                print("Dependencies:")
                for dep in package_info.requires_dist[:5]:  # Show first 5
                    print(f"  - {dep}")

                if len(package_info.requires_dist) > 5:
                    print(
                        f"  ... and {len(package_info.requires_dist) - 5} more")

            if package_info.provides_extra:
                print(
                    f"Optional extras: {', '.join(package_info.provides_extra)}")

            print()

        except Exception as e:
            print(f"Error analyzing dependencies: {e}")


async def demonstrate_security_check() -> None:
    """Demonstrate security vulnerability checking."""
    print("=== Security Check Demo ===")

    async with client:
        try:
            # Check a package that might have vulnerabilities
            # Note: This is just an example - the package may or may not have vulnerabilities
            package_info = await client.get_package_info("django", "2.0.0")

            print(
                f"Security check for {package_info.name} {package_info.version}")

            if package_info.vulnerabilities:
                print(
                    f"⚠️  Found {len(package_info.vulnerabilities)} vulnerabilities:")
                for vuln in package_info.vulnerabilities:
                    print(f"  - {vuln.id}: {vuln.summary}")
                    if vuln.fixed_in:
                        print(f"    Fixed in: {', '.join(vuln.fixed_in)}")
            else:
                print("✅ No known vulnerabilities found")

            print()

        except Exception as e:
            print(f"Error checking security: {e}")


async def main() -> None:
    """Run all demonstrations."""
    print("PyPI MCP Server - Basic Usage Examples")
    print("=" * 50)
    print()

    await demonstrate_package_info()
    await demonstrate_version_listing()
    await demonstrate_stats()
    await demonstrate_dependency_analysis()
    await demonstrate_security_check()

    print("Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())
