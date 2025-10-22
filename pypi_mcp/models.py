"""Pydantic models for PyPI API responses and internal data structures."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class PackageFile(BaseModel):
    """Represents a package file (wheel or source distribution)."""

    filename: str
    url: HttpUrl
    size: int
    md5_digest: str
    sha256_digest: str = Field(alias="digests")
    upload_time: datetime = Field(alias="upload_time_iso_8601")
    python_version: str
    packagetype: str  # "bdist_wheel", "sdist", etc.
    requires_python: Optional[str] = None
    yanked: bool = False
    yanked_reason: Optional[str] = None

    @field_validator("sha256_digest", mode="before")
    @classmethod
    def extract_sha256(cls, v: Any) -> str:
        if isinstance(v, dict):
            return v.get("sha256", "")  # type: ignore[no-any-return]
        return v  # type: ignore[no-any-return]


class Vulnerability(BaseModel):
    """Represents a security vulnerability."""

    id: str
    source: str
    summary: Optional[str] = ""
    details: Optional[str] = ""
    aliases: List[str] = Field(default_factory=list)
    fixed_in: List[str] = Field(default_factory=list)
    link: Optional[HttpUrl] = None
    withdrawn: Optional[datetime] = None

    @field_validator("summary", "details", mode="before")
    @classmethod
    def handle_none_strings(cls, v: Any) -> str:
        return v or ""


class PackageInfo(BaseModel):
    """Represents package metadata from PyPI."""

    name: str
    version: str
    summary: str
    description: str
    description_content_type: Optional[str] = None
    author: Optional[str] = ""
    author_email: Optional[str] = ""
    maintainer: Optional[str] = ""
    maintainer_email: Optional[str] = ""
    license: Optional[str] = ""
    home_page: Optional[str] = ""
    download_url: Optional[str] = ""
    project_urls: Dict[str, str] = {}
    platform: Optional[str] = None
    classifiers: List[str] = []
    keywords: Optional[str] = ""
    requires_python: Optional[str] = None
    requires_dist: List[str] = []
    provides_extra: List[str] = Field(default_factory=list)
    yanked: bool = False
    yanked_reason: Optional[str] = None

    # URLs and metadata
    package_url: HttpUrl
    project_url: HttpUrl
    release_url: HttpUrl

    # Files for this version
    files: List[PackageFile] = Field(default_factory=list, alias="urls")

    # Security information
    vulnerabilities: List[Vulnerability] = []

    @field_validator(
        "author",
        "author_email",
        "maintainer",
        "maintainer_email",
        "license",
        "home_page",
        "download_url",
        "keywords",
        mode="before",
    )
    @classmethod
    def handle_none_strings(cls, v: Any) -> str:
        return v or ""

    @field_validator("provides_extra", "requires_dist", "classifiers", mode="before")
    @classmethod
    def handle_none_lists(cls, v: Any) -> List[str]:
        return v or []

    @field_validator("project_urls", mode="before")
    @classmethod
    def handle_none_project_urls(cls, v: Any) -> Dict[str, str]:
        return v or {}


class PackageVersions(BaseModel):
    """Represents all versions of a package."""

    name: str
    versions: List[str]
    latest_version: str


class DependencyInfo(BaseModel):
    """Represents dependency information."""

    name: str
    version_spec: str
    extras: List[str] = []
    environment_marker: Optional[str] = None


class PackageStats(BaseModel):
    """Represents package statistics."""

    name: str
    total_size: int
    file_count: int
    version_count: int
    last_updated: datetime


class PyPIStats(BaseModel):
    """Represents overall PyPI statistics."""

    total_packages_size: int
    top_packages: Dict[str, Dict[str, int]]


class SearchResult(BaseModel):
    """Represents a package search result."""

    name: str
    version: str = ""
    summary: str = ""
    description: str = ""
    author: str = ""
    keywords: List[str] = Field(default_factory=list)
    classifiers: List[str] = Field(default_factory=list)
    score: float = 0.0  # Relevance score
