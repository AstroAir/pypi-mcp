# Data Models Reference

Complete reference for all data structures used by the PyPI MCP Server.

## Overview

The PyPI MCP Server uses Pydantic models for data validation and serialization. This document provides complete schemas for all data structures returned by tools, resources, and prompts.

## Core Models

### PackageInfo

Complete package metadata from PyPI.

```python
class PackageInfo:
    name: str                           # Package name
    version: str                        # Package version
    summary: str                        # Short description
    description: str                    # Long description
    description_content_type: str       # Description format (e.g., "text/markdown")
    author: str                         # Package author
    author_email: str                   # Author email
    maintainer: str                     # Package maintainer
    maintainer_email: str               # Maintainer email
    license: str                        # License information
    home_page: str                      # Homepage URL
    download_url: str                   # Download URL
    project_urls: Dict[str, str]        # Project URLs (homepage, repository, etc.)
    platform: str                       # Target platform
    classifiers: List[str]              # PyPI classifiers
    keywords: str                       # Package keywords
    requires_python: str                # Python version requirement
    requires_dist: List[str]            # Package dependencies
    provides_extra: List[str]           # Optional extras
    yanked: bool                        # Whether version is yanked
    yanked_reason: str                  # Reason for yanking
    package_url: str                    # PyPI package URL
    project_url: str                    # PyPI project URL
    release_url: str                    # PyPI release URL
    files: List[PackageFile]            # Package files
    vulnerabilities: List[Vulnerability] # Security vulnerabilities
```

#### Example JSON

```json
{
  "name": "requests",
  "version": "2.31.0",
  "summary": "Python HTTP for Humans.",
  "description": "Requests is a simple, yet elegant HTTP library.",
  "description_content_type": "text/markdown",
  "author": "Kenneth Reitz",
  "author_email": "me@kennethreitz.org",
  "maintainer": "Kenneth Reitz",
  "maintainer_email": "me@kennethreitz.org",
  "license": "Apache 2.0",
  "home_page": "https://requests.readthedocs.io",
  "download_url": "",
  "project_urls": {
    "Homepage": "https://requests.readthedocs.io",
    "Repository": "https://github.com/psf/requests"
  },
  "platform": null,
  "classifiers": [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3"
  ],
  "keywords": "http,requests,web",
  "requires_python": ">=3.7",
  "requires_dist": ["urllib3>=1.21.1,<3", "certifi>=2017.4.17"],
  "provides_extra": ["security", "socks"],
  "yanked": false,
  "yanked_reason": null,
  "package_url": "https://pypi.org/project/requests/",
  "project_url": "https://pypi.org/project/requests/",
  "release_url": "https://pypi.org/project/requests/2.31.0/",
  "files": [],
  "vulnerabilities": []
}
```

### PackageFile

Information about a package file (wheel or source distribution).

```python
class PackageFile:
    filename: str                       # File name
    url: str                           # Download URL
    size: int                          # File size in bytes
    md5_digest: str                    # MD5 hash
    sha256_digest: str                 # SHA256 hash
    upload_time: datetime              # Upload timestamp
    python_version: str                # Python version requirement
    packagetype: str                   # Package type (bdist_wheel, sdist, etc.)
    requires_python: str               # Python version requirement
    yanked: bool                       # Whether file is yanked
    yanked_reason: str                 # Reason for yanking
```

#### Package Types

| Type            | Description                          |
| --------------- | ------------------------------------ |
| `bdist_wheel`   | Binary wheel distribution            |
| `sdist`         | Source distribution                  |
| `bdist_egg`     | Binary egg distribution (deprecated) |
| `bdist_wininst` | Windows installer                    |
| `bdist_msi`     | Windows MSI installer                |
| `bdist_rpm`     | RPM package                          |
| `bdist_dumb`    | Binary distribution                  |

#### Example JSON

```json
{
  "filename": "requests-2.31.0-py3-none-any.whl",
  "url": "https://files.pythonhosted.org/packages/.../requests-2.31.0-py3-none-any.whl",
  "size": 62574,
  "md5_digest": "a8b2b8c1234567890abcdef",
  "sha256_digest": "58cd2187c01e70e6e26505bca751777aa9f2ee0b...",
  "upload_time": "2023-07-27T15:06:07",
  "python_version": "py3",
  "packagetype": "bdist_wheel",
  "requires_python": ">=3.7",
  "yanked": false,
  "yanked_reason": null
}
```

### Vulnerability

Security vulnerability information.

```python
class Vulnerability:
    id: str                            # Vulnerability ID
    source: str                        # Source (e.g., "GitHub Advisory Database")
    summary: str                       # Brief summary
    details: str                       # Detailed description
    aliases: List[str]                 # Alternative IDs (CVE, etc.)
    fixed_in: List[str]               # Versions that fix the vulnerability
    link: str                         # Reference URL
    withdrawn: datetime               # Withdrawal date (if applicable)
```

#### Example JSON

```json
{
  "id": "GHSA-2hrw-hx67-34x6",
  "source": "GitHub Advisory Database",
  "summary": "Django vulnerable to potential denial of service",
  "details": "An issue was discovered in Django 2.2 before 2.2.28...",
  "aliases": ["CVE-2023-31047"],
  "fixed_in": ["2.2.28", "3.2.19", "4.1.9", "4.2.1"],
  "link": "https://github.com/advisories/GHSA-2hrw-hx67-34x6",
  "withdrawn": null
}
```

### DependencyInfo

Parsed dependency information.

```python
class DependencyInfo:
    name: str                          # Dependency name
    version_spec: str                  # Version specification
    extras: List[str]                  # Optional extras
    environment_marker: str            # Environment marker
```

#### Version Specifications

Version specifications follow PEP 440:

| Operator | Meaning               | Example   |
| -------- | --------------------- | --------- |
| `==`     | Exactly equal         | `==1.0.0` |
| `>=`     | Greater than or equal | `>=1.0.0` |
| `>`      | Greater than          | `>1.0.0`  |
| `<=`     | Less than or equal    | `<=2.0.0` |
| `<`      | Less than             | `<2.0.0`  |
| `!=`     | Not equal             | `!=1.5.0` |
| `~=`     | Compatible release    | `~=1.4.2` |

#### Environment Markers

Environment markers specify conditions:

| Marker            | Description      | Example                        |
| ----------------- | ---------------- | ------------------------------ |
| `python_version`  | Python version   | `python_version >= "3.8"`      |
| `platform_system` | Operating system | `platform_system == "Windows"` |
| `extra`           | Optional extra   | `extra == "dev"`               |

#### Example JSON

```json
{
  "name": "urllib3",
  "version_spec": ">=1.21.1,<3",
  "extras": [],
  "environment_marker": null
}
```

## Response Models

### PackageVersions

List of package versions.

```python
class PackageVersions:
    package_name: str                  # Package name
    total_versions: int                # Total number of versions
    returned_versions: int             # Number of versions returned
    latest_version: str                # Latest version
    versions: List[VersionInfo]        # Version information
```

### VersionInfo

Information about a specific version.

```python
class VersionInfo:
    version: str                       # Version string
    type: str                         # Version type (stable, pre-release, development)
    is_latest: bool                   # Whether this is the latest version
```

#### Version Types

| Type          | Description         | Examples              |
| ------------- | ------------------- | --------------------- |
| `stable`      | Stable release      | `1.0.0`, `2.1.3`      |
| `pre-release` | Pre-release version | `1.0.0rc1`, `2.0.0b1` |
| `development` | Development version | `1.0.0.dev1`          |

### SearchResult

Package search result.

```python
class SearchResult:
    name: str                          # Package name
    version: str                       # Latest version
    summary: str                       # Package summary
    description: str                   # Package description
    author: str                        # Package author
    keywords: List[str]                # Package keywords
    classifiers: List[str]             # PyPI classifiers
    score: float                       # Relevance score (0.0-1.0)
```

### ComparisonResult

Package version comparison result.

```python
class ComparisonResult:
    package_name: str                  # Package name
    version1: VersionDetails           # First version details
    version2: VersionDetails           # Second version details
    comparison: ComparisonDetails      # Comparison results
```

### VersionDetails

Details about a version in comparison.

```python
class VersionDetails:
    version: str                       # Version string
    type: str                         # Version type
    upload_time: str                  # Upload timestamp (ISO format)
    dependencies_count: int           # Number of dependencies
    vulnerabilities_count: int        # Number of vulnerabilities
```

### ComparisonDetails

Comparison analysis between versions.

```python
class ComparisonDetails:
    result: int                        # Comparison result (-1, 0, 1)
    newer_version: str                # Which version is newer
    is_upgrade: bool                  # Whether version1 -> version2 is upgrade
    is_downgrade: bool                # Whether version1 -> version2 is downgrade
```

### CompatibilityResult

Python version compatibility result.

```python
class CompatibilityResult:
    package_name: str                  # Package name
    package_version: str               # Package version
    python_version: str                # Python version checked
    is_compatible: bool                # Whether compatible
    requires_python: str               # Python requirement from package
    compatibility_notes: List[str]     # Compatibility notes/warnings
    classifiers: List[str]             # Python-related classifiers
```

### DependencyAnalysis

Dependency analysis result.

```python
class DependencyAnalysis:
    package_name: str                  # Package name
    package_version: str               # Package version
    total_dependencies: int            # Total number of dependencies
    runtime_dependencies: List[DependencyInfo]     # Runtime dependencies
    development_dependencies: List[DependencyInfo] # Development dependencies
    available_extras: List[str]        # Available optional extras
    optional_dependencies: Dict[str, List[DependencyInfo]] # Optional dependencies by extra
```

### VulnerabilityReport

Security vulnerability report.

```python
class VulnerabilityReport:
    package_name: str                  # Package name
    package_version: str               # Package version
    vulnerability_count: int           # Number of vulnerabilities
    has_vulnerabilities: bool          # Whether vulnerabilities exist
    vulnerabilities: List[Vulnerability] # Vulnerability details
    security_status: str               # Security status (secure/vulnerable)
    recommendation: str                # Security recommendation
```

### HealthAssessment

Package health assessment.

```python
class HealthAssessment:
    package_name: str                  # Package name
    package_version: str               # Package version
    health_score: int                  # Health score (0-100)
    health_status: str                 # Health status
    health_notes: List[str]            # Health assessment notes
    total_versions: int                # Total number of versions
    is_latest: bool                    # Whether this is latest version
    has_vulnerabilities: bool          # Whether vulnerabilities exist
    is_yanked: bool                    # Whether version is yanked
    version_type: str                  # Version type
```

#### Health Status Values

| Status      | Score Range | Description                           |
| ----------- | ----------- | ------------------------------------- |
| `excellent` | 80-100      | Well-maintained, secure package       |
| `good`      | 60-79       | Generally good with minor issues      |
| `fair`      | 40-59       | Some concerns, use with caution       |
| `poor`      | 0-39        | Significant issues, avoid if possible |

### PyPIStats

PyPI-wide statistics.

```python
class PyPIStats:
    total_packages_size: int           # Total size of all packages (bytes)
    total_size_formatted: str          # Human-readable total size
    top_packages_count: int            # Number of top packages tracked
    top_packages: List[TopPackage]     # Top packages by size
    last_updated: str                  # Last update timestamp
```

### TopPackage

Information about a top package.

```python
class TopPackage:
    name: str                          # Package name
    size: int                         # Package size (bytes)
    size_formatted: str               # Human-readable size
```

### CacheInfo

Cache statistics and information.

```python
class CacheInfo:
    cache_stats: CacheStats           # Cache statistics
    cache_enabled: bool               # Whether caching is enabled
    cache_ttl_seconds: int            # Cache TTL in seconds
```

### CacheStats

Detailed cache statistics.

```python
class CacheStats:
    hits: int                         # Number of cache hits
    misses: int                       # Number of cache misses
    hit_rate: float                   # Cache hit rate (0.0-1.0)
    current_size: int                 # Current number of cached items
    max_size: int                     # Maximum cache capacity
```

## Validation Rules

### Package Names

Package names must follow PyPI naming conventions:

- Contain only letters, numbers, hyphens, underscores, and periods
- Start and end with alphanumeric characters
- Case-insensitive (normalized to lowercase)

**Valid Examples:**

- `requests`
- `django-rest-framework`
- `scikit-learn`
- `Pillow`

**Invalid Examples:**

- `-invalid` (starts with hyphen)
- `invalid-` (ends with hyphen)
- `in..valid` (consecutive periods)

### Version Strings

Version strings must follow PEP 440:

**Valid Examples:**

- `1.0.0`
- `2.1.3rc1`
- `1.0.0.dev1`
- `2.0.0b1`

**Invalid Examples:**

- `v1.0.0` (prefix not allowed)
- `1.0` (incomplete version)
- `1.0.0-rc1` (wrong separator)

### Version Specifications

Version specifications must use valid operators:

**Valid Examples:**

- `>=1.0.0`
- `>=1.0.0,<2.0.0`
- `~=1.4.2`
- `!=1.5.0`

**Invalid Examples:**

- `=> 1.0.0` (invalid operator)
- `>= 1.0.0` (space not allowed)
- `1.0.0+` (invalid syntax)

## Error Models

### ErrorResponse

Standard error response format.

```python
class ErrorResponse:
    code: int                         # Error code
    message: str                      # Error message
    data: Dict                        # Additional error data
```

### ValidationError

Parameter validation error.

```python
class ValidationError:
    parameter: str                    # Parameter name
    value: str                       # Invalid value
    details: str                     # Validation error details
```

## Next Steps

- [Tools Reference](tools.md) - See how these models are used in tools
- [Usage Examples](../user-guide/usage-examples.md) - Practical examples with these models
- [Integration Guide](../getting-started/integration.md) - Integrate with these data structures
