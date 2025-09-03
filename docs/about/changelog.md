# Changelog

All notable changes to the PyPI MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive MkDocs documentation structure
- Performance monitoring and optimization guides
- Advanced debugging tools and techniques
- Detailed troubleshooting guides

### Changed

- Improved documentation organization and navigation
- Enhanced code examples and usage patterns

## [0.1.0] - 2025-01-15

### Added

- Initial release of PyPI MCP Server
- FastMCP-based server implementation
- 10 comprehensive tools for PyPI package management:
  - `get_package_info` - Detailed package metadata retrieval
  - `get_package_versions` - Package version listing
  - `search_packages` - Package search functionality
  - `compare_versions` - Version comparison analysis
  - `check_compatibility` - Python version compatibility checking
  - `get_dependencies` - Dependency analysis with extras support
  - `check_vulnerabilities` - Security vulnerability scanning
  - `get_package_health` - Package health assessment
  - `get_pypi_stats` - PyPI-wide statistics
  - `get_cache_info` - Cache performance monitoring
- 2 resource endpoints:
  - `pypi://stats/overview` - PyPI statistics overview
  - `pypi://package/{name}` - Package metadata resource
- 3 AI analysis prompts:
  - `analyze_package` - Comprehensive package analysis
  - `compare_packages` - Package comparison template
  - `security_review` - Security-focused review template
- Intelligent caching system with TTL and LRU eviction
- Rate limiting with configurable limits
- Support for both STDIO and HTTP transports
- Comprehensive configuration via environment variables
- Async/await architecture for high performance
- Type safety with Pydantic models
- Extensive error handling and validation
- Claude Desktop integration support

### Technical Features

- **Caching**: TTL-based cache with LRU eviction policy
- **Rate Limiting**: Configurable client-side rate limiting
- **Transport Protocols**: STDIO and HTTP transport support
- **Data Validation**: Pydantic models for type safety
- **Error Handling**: Comprehensive error handling with specific error codes
- **Logging**: Configurable logging with multiple levels
- **Performance**: Async/await architecture for non-blocking operations
- **Security**: Input validation and sanitized error responses

### Configuration Options

- `PYPI_MCP_PYPI_BASE_URL` - PyPI API base URL
- `PYPI_MCP_USER_AGENT` - Custom User-Agent header
- `PYPI_MCP_TIMEOUT` - HTTP request timeout
- `PYPI_MCP_RATE_LIMIT` - Maximum requests per second
- `PYPI_MCP_CACHE_TTL` - Cache time-to-live in seconds
- `PYPI_MCP_CACHE_MAX_SIZE` - Maximum cache entries
- `PYPI_MCP_LOG_LEVEL` - Logging verbosity level
- `PYPI_MCP_ENABLE_VULNERABILITY_CHECK` - Enable/disable vulnerability checking
- `PYPI_MCP_ENABLE_STATS` - Enable/disable statistics endpoints
- `PYPI_MCP_ENABLE_SEARCH` - Enable/disable search functionality

### Dependencies

- `fastmcp` (>=2.12.0) - MCP framework
- `httpx` (>=0.27.0) - Async HTTP client
- `packaging` (>=23.0) - Python package version handling
- `cachetools` (>=5.3.0) - Caching utilities
- `pydantic` (>=2.0.0) - Data validation and serialization

### Development Tools

- `pytest` - Testing framework with async support
- `black` - Code formatting
- `isort` - Import sorting
- `mypy` - Type checking
- `ruff` - Fast Python linter
- `pytest-cov` - Coverage reporting

### Documentation

- Comprehensive README with quick start guide
- API documentation for all tools, resources, and prompts
- Configuration guide with examples
- Integration guide for Claude Desktop and custom clients
- Troubleshooting guide for common issues
- Development setup instructions
- Contributing guidelines

### Examples

- Basic usage examples for all tools
- Claude Desktop configuration examples
- HTTP transport integration examples
- Python client implementation examples
- Performance optimization examples

## Version History

### Pre-release Development

#### [0.1.0-rc1] - 2025-01-10

- Release candidate with core functionality
- Initial tool implementations
- Basic caching and rate limiting
- STDIO transport support

#### [0.1.0-beta1] - 2025-01-05

- Beta release for testing
- Core MCP server implementation
- Basic package information tools
- Initial documentation

#### [0.1.0-alpha1] - 2025-01-01

- Initial alpha release
- Proof of concept implementation
- Basic PyPI API integration
- FastMCP framework integration

## Upgrade Guide

### From Pre-release to 0.1.0

This is the first stable release. If you were using pre-release versions:

1. **Update installation**:

   ```bash
   pip install --upgrade pypi-mcp
   ```

2. **Review configuration**: Check environment variables for any changes

3. **Update integrations**: Verify Claude Desktop configuration is current

4. **Test functionality**: Run basic tests to ensure everything works

## Breaking Changes

### 0.1.0

- First stable release - no breaking changes from pre-release versions
- Established stable API contract for tools, resources, and prompts

## Migration Notes

### Future Breaking Changes

We follow semantic versioning:

- **Patch releases** (0.1.x): Bug fixes, no breaking changes
- **Minor releases** (0.x.0): New features, backward compatible
- **Major releases** (x.0.0): Breaking changes, migration required

When breaking changes are introduced, we will provide:

- Advance notice in release notes
- Migration guides with step-by-step instructions
- Deprecation warnings in the release before removal
- Support for both old and new APIs during transition periods

## Release Notes Format

Each release includes:

### Added

- New features and capabilities
- New tools, resources, or prompts
- New configuration options
- New integrations or examples

### Changed

- Improvements to existing features
- Performance enhancements
- Updated dependencies
- Documentation improvements

### Deprecated

- Features marked for removal in future versions
- Alternative approaches recommended
- Timeline for removal

### Removed

- Features removed in this version
- Breaking changes from previous versions
- Discontinued support for older versions

### Fixed

- Bug fixes and issue resolutions
- Security vulnerability patches
- Performance issue fixes
- Documentation corrections

### Security

- Security-related changes and fixes
- Vulnerability disclosures and patches
- Security best practice updates

## Contributing to Changelog

When contributing to the project:

1. **Add entries** to the "Unreleased" section
2. **Use appropriate categories** (Added, Changed, Fixed, etc.)
3. **Write clear descriptions** of changes
4. **Include issue/PR references** where applicable
5. **Follow the format** established in existing entries

Example entry:

```markdown
### Added

- New `analyze_dependencies` tool for deep dependency analysis (#123)
- Support for private PyPI repositories via configuration (#145)

### Fixed

- Cache invalidation bug when package versions are yanked (#134)
- Memory leak in HTTP transport under high load (#156)
```

## Release Process

Releases follow this process:

1. **Update version** in `pyproject.toml` and `__init__.py`
2. **Move unreleased changes** to new version section
3. **Add release date** to version header
4. **Create release tag** following `v{version}` format
5. **Publish to PyPI** and update documentation
6. **Create GitHub release** with changelog excerpt

## Versioning Policy

- **Semantic Versioning**: MAJOR.MINOR.PATCH format
- **Backward Compatibility**: Maintained within major versions
- **Deprecation Policy**: Features deprecated for at least one minor version before removal
- **Security Updates**: Provided for current and previous major versions
- **LTS Support**: Long-term support versions may be designated for enterprise use

## Support Timeline

| Version | Release Date | End of Support | Notes          |
| ------- | ------------ | -------------- | -------------- |
| 0.1.x   | 2025-01-15   | TBD            | Current stable |

Support includes:

- Security updates
- Critical bug fixes
- Documentation updates
- Community support

## Links

- [GitHub Repository](https://github.com/AstroAir/pypi-mcp)
- [PyPI Package](https://pypi.org/project/pypi-mcp/)
- [Documentation](https://astroair.github.io/pypi-mcp/)
- [Issue Tracker](https://github.com/AstroAir/pypi-mcp/issues)
- [Discussions](https://github.com/AstroAir/pypi-mcp/discussions)
