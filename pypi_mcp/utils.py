"""Utility functions for the PyPI MCP server."""

import re
from typing import List, Optional
from urllib.parse import urlparse

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import parse

from .models import DependencyInfo


def normalize_package_name(name: str) -> str:
    """Normalize package name according to PEP 508."""
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirement(req_string: str) -> DependencyInfo:
    """Parse a requirement string into structured dependency info."""
    try:
        req = Requirement(req_string)
        return DependencyInfo(
            name=req.name,
            version_spec=str(req.specifier) if req.specifier else "",
            extras=list(req.extras),
            environment_marker=str(req.marker) if req.marker else None,
        )
    except Exception:
        # Fallback for malformed requirements
        parts = req_string.split()
        name = parts[0] if parts else req_string
        return DependencyInfo(
            name=normalize_package_name(name),
            version_spec="",
            extras=[],
            environment_marker=None,
        )


def parse_requirements(requirements: List[str]) -> List[DependencyInfo]:
    """Parse a list of requirement strings."""
    return [parse_requirement(req) for req in requirements if req.strip()]


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings. Returns -1, 0, or 1."""
    try:
        v1 = parse(version1)
        v2 = parse(version2)

        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        else:
            return 0
    except Exception:
        # Fallback to string comparison
        if version1 < version2:
            return -1
        elif version1 > version2:
            return 1
        else:
            return 0


def is_version_compatible(version: str, spec: str) -> bool:
    """Check if a version satisfies a version specifier."""
    if not spec:
        return True

    try:
        version_obj = parse(version)
        spec_obj = SpecifierSet(spec)
        return version_obj in spec_obj
    except Exception:
        return False


def extract_domain_from_url(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)

    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1

    return f"{size:.1f} {size_names[i]}"


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate simple similarity score between two strings."""
    text1 = text1.lower()
    text2 = text2.lower()

    if text1 == text2:
        return 1.0

    if text1 in text2 or text2 in text1:
        return 0.8

    # Simple word overlap scoring
    words1 = set(text1.split())
    words2 = set(text2.split())

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union) if union else 0.0


def extract_keywords(text: Optional[str]) -> List[str]:
    """Extract keywords from text."""
    if not text:
        return []

    # Split by common separators
    keywords = re.split(r"[,;\s]+", text.lower())

    # Filter out empty strings and common words
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
    }
    keywords = [
        kw.strip() for kw in keywords if kw.strip() and kw.strip() not in stop_words
    ]

    return keywords


def validate_package_name(name: str) -> bool:
    """Validate package name according to PyPI rules."""
    if not name:
        return False

    # PyPI package names can contain letters, numbers, hyphens, underscores, and periods
    pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$"
    return bool(re.match(pattern, name))


def validate_version(version: str) -> bool:
    """Validate version string."""
    if not version:
        return False

    try:
        parse(version)
        return True
    except Exception:
        return False


def get_package_type_description(packagetype: str) -> str:
    """Get human-readable description of package type."""
    descriptions = {
        "bdist_wheel": "Binary wheel distribution",
        "sdist": "Source distribution",
        "bdist_egg": "Binary egg distribution (deprecated)",
        "bdist_wininst": "Windows installer",
        "bdist_msi": "Windows MSI installer",
        "bdist_rpm": "RPM package",
        "bdist_dumb": "Binary distribution",
    }
    return descriptions.get(packagetype, f"Unknown package type: {packagetype}")


def classify_version_type(version: str) -> str:
    """Classify version as stable, pre-release, or development."""
    try:
        v = parse(version)
        if v.is_prerelease:
            return "pre-release"
        elif v.is_devrelease:
            return "development"
        else:
            return "stable"
    except Exception:
        # Check for common pre-release indicators
        version_lower = version.lower()
        if any(
            indicator in version_lower
            for indicator in ["alpha", "beta", "rc", "dev", "pre"]
        ):
            return "pre-release"
        return "stable"
