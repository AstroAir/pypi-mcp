# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup and documentation

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 2025-01-03

### Added
- Initial release of PyPI MCP Server
- Package discovery and search functionality
- Detailed package metadata retrieval
- Version management and comparison tools
- Dependency analysis capabilities
- Security vulnerability checking
- PyPI statistics and analytics
- Async/await support for high performance
- Intelligent caching with TTL
- Rate limiting and error handling
- Support for both HTTP and STDIO transports
- Comprehensive logging and monitoring
- FastMCP framework integration
- Pydantic data models for type safety
- Complete test suite with pytest
- Documentation with MkDocs
- Examples and usage guides

### Tools Available
- `get_package_info` - Get detailed package metadata
- `get_package_versions` - List package versions
- `search_packages` - Search for packages
- `compare_versions` - Compare two package versions
- `check_compatibility` - Check Python compatibility
- `get_dependencies` - Analyze package dependencies
- `check_vulnerabilities` - Check for security vulnerabilities
- `get_package_health` - Assess package health and maintenance
- `get_pypi_stats` - Get PyPI-wide statistics
- `get_cache_info` - Get server cache information

### Resources Available
- `pypi://stats/overview` - PyPI statistics overview
- `pypi://package/{package_name}` - Package metadata resource

### Prompts Available
- `analyze_package` - Generate comprehensive package analysis
- `compare_packages` - Generate package comparison analysis
- `security_review` - Generate security review prompt

### Technical Features
- Built with FastMCP framework
- Async HTTP client with httpx
- Pydantic data validation and serialization
- Python packaging utilities integration
- Intelligent caching with cachetools
- Comprehensive error handling
- Type hints throughout codebase
- Modern Python packaging with pyproject.toml
- UV package manager support
- GitHub Actions CI/CD pipeline
- Code quality tools (Black, isort, Ruff, MyPy)
- Test coverage reporting
- Security scanning integration

[Unreleased]: https://github.com/AstroAir/pypi-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AstroAir/pypi-mcp/releases/tag/v0.1.0
