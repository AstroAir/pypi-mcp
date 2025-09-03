"""PyPI API client for fetching package information."""

import asyncio
import logging
from typing import Dict, List, Optional
from urllib.parse import quote

import httpx
from packaging.version import parse

from .cache import cached
from .config import settings
from .exceptions import (PackageNotFoundError, PyPIAPIError, RateLimitError,
                         VersionNotFoundError)
from .models import PackageInfo, PyPIStats

logger = logging.getLogger(__name__)


class PyPIClient:
    """Async client for PyPI API."""

    def __init__(self):
        self.session: Optional[httpx.AsyncClient] = None
        self._rate_limiter = asyncio.Semaphore(int(settings.rate_limit))

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            timeout=settings.timeout,
            headers={"User-Agent": settings.user_agent},
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()

    async def _make_request(
        self, url: str, headers: Optional[Dict[str, str]] = None
    ) -> Dict:
        """Make an HTTP request with rate limiting and error handling."""
        if not self.session:
            raise PyPIAPIError("Client not initialized. Use async context manager.")

        async with self._rate_limiter:
            try:
                response = await self.session.get(url, headers=headers or {})

                if response.status_code == 404:
                    raise PackageNotFoundError("Resource not found")
                elif response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    raise RateLimitError(int(retry_after) if retry_after else None)
                elif response.status_code >= 400:
                    raise PyPIAPIError(
                        f"HTTP {response.status_code}: {response.text}",
                        response.status_code,
                    )

                return response.json()

            except httpx.RequestError as e:
                raise PyPIAPIError(f"Request failed: {str(e)}")

    @cached(ttl=300)
    async def get_package_info(
        self, package_name: str, version: Optional[str] = None
    ) -> PackageInfo:
        """Get package information from PyPI."""
        package_name = package_name.lower().replace("_", "-")

        if version:
            url = f"{settings.pypi_base_url}/pypi/{quote(package_name)}/{quote(version)}/json"
        else:
            url = f"{settings.pypi_base_url}/pypi/{quote(package_name)}/json"

        try:
            data = await self._make_request(url)

            # Extract package info
            info = data["info"]
            files = data.get("urls", [])
            vulnerabilities = data.get("vulnerabilities", [])

            # Convert to our model
            package_info = PackageInfo(
                name=info["name"],
                version=info["version"],
                summary=info.get("summary", ""),
                description=info.get("description", ""),
                description_content_type=info.get("description_content_type"),
                author=info.get("author", ""),
                author_email=info.get("author_email", ""),
                maintainer=info.get("maintainer", ""),
                maintainer_email=info.get("maintainer_email", ""),
                license=info.get("license", ""),
                home_page=info.get("home_page", ""),
                download_url=info.get("download_url", ""),
                project_urls=info.get("project_urls", {}),
                platform=info.get("platform"),
                classifiers=info.get("classifiers", []),
                keywords=info.get("keywords", ""),
                requires_python=info.get("requires_python"),
                requires_dist=info.get("requires_dist", []),
                provides_extra=info.get("provides_extra", []),
                yanked=info.get("yanked", False),
                yanked_reason=info.get("yanked_reason"),
                package_url=info["package_url"],
                project_url=info["project_url"],
                release_url=info["release_url"],
                urls=files,
                vulnerabilities=vulnerabilities,
            )

            return package_info

        except PackageNotFoundError:
            if version:
                raise VersionNotFoundError(package_name, version)
            else:
                raise PackageNotFoundError(package_name)

    @cached(ttl=600)
    async def get_package_versions(self, package_name: str) -> List[str]:
        """Get all versions of a package."""
        package_name = package_name.lower().replace("_", "-")
        url = f"{settings.pypi_base_url}/pypi/{quote(package_name)}/json"

        try:
            data = await self._make_request(url)
            releases = data.get("releases", {})

            # Filter out versions with no files and sort by version
            versions = []
            for version, files in releases.items():
                if files:  # Only include versions with files
                    versions.append(version)

            # Sort versions properly
            try:
                versions.sort(key=lambda v: parse(v), reverse=True)
            except Exception:
                # Fallback to string sorting if version parsing fails
                versions.sort(reverse=True)

            return versions

        except PackageNotFoundError:
            raise PackageNotFoundError(package_name)

    @cached(ttl=3600)
    async def get_pypi_stats(self) -> PyPIStats:
        """Get PyPI statistics."""
        url = f"{settings.pypi_base_url}/stats/"
        headers = {"Accept": "application/json"}

        try:
            data = await self._make_request(url, headers)
            return PyPIStats(
                total_packages_size=data["total_packages_size"],
                top_packages=data["top_packages"],
            )
        except Exception as e:
            logger.warning(f"Failed to get PyPI stats: {e}")
            # Return empty stats if API fails
            return PyPIStats(total_packages_size=0, top_packages={})


# Global client instance
client = PyPIClient()
