# Release Process

Complete guide for releasing new versions of the PyPI MCP Server.

## Release Philosophy

The PyPI MCP Server follows a structured release process to ensure:

- **Quality**: Thorough testing before releases
- **Predictability**: Regular release schedule
- **Transparency**: Clear communication about changes
- **Stability**: Semantic versioning for compatibility

## Versioning Strategy

### Semantic Versioning

We follow [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes that require user action
- **MINOR**: New features that are backward compatible
- **PATCH**: Bug fixes that are backward compatible

### Version Examples

| Version           | Type  | Description                        |
| ----------------- | ----- | ---------------------------------- |
| `0.1.0` → `0.1.1` | Patch | Bug fixes only                     |
| `0.1.1` → `0.2.0` | Minor | New features, backward compatible  |
| `0.2.0` → `1.0.0` | Major | Breaking changes or stable release |

### Pre-release Versions

For testing and development:

- **Alpha**: `1.0.0a1` - Early development
- **Beta**: `1.0.0b1` - Feature complete, testing
- **Release Candidate**: `1.0.0rc1` - Final testing

## Release Types

### 1. Patch Releases

**When**: Critical bug fixes, security patches

**Frequency**: As needed

**Process**: Fast-track for critical issues

```bash
# Example: 0.1.0 → 0.1.1
git checkout main
git pull origin main
# Apply fix
# Update version
# Create release
```

### 2. Minor Releases

**When**: New features, improvements

**Frequency**: Monthly or when features are ready

**Process**: Full release process

```bash
# Example: 0.1.1 → 0.2.0
git checkout main
git pull origin main
# Merge feature branches
# Update version
# Update changelog
# Create release
```

### 3. Major Releases

**When**: Breaking changes, major milestones

**Frequency**: When necessary

**Process**: Extended testing and communication

```bash
# Example: 0.9.0 → 1.0.0
# Extensive testing
# Migration guide
# Communication plan
# Full release process
```

## Release Schedule

### Regular Schedule

- **Patch releases**: As needed for critical issues
- **Minor releases**: First Monday of each month (if changes available)
- **Major releases**: When breaking changes are necessary

### Release Calendar

| Month    | Target | Type  | Focus                  |
| -------- | ------ | ----- | ---------------------- |
| January  | 0.2.0  | Minor | New tools, performance |
| February | 0.2.1  | Patch | Bug fixes              |
| March    | 0.3.0  | Minor | Security features      |
| April    | 0.3.1  | Patch | Stability              |
| May      | 0.4.0  | Minor | API improvements       |
| June     | 0.4.1  | Patch | Bug fixes              |

## Pre-Release Checklist

### 1. Code Quality

- [ ] All tests pass (unit, integration, performance)
- [ ] Code coverage ≥90%
- [ ] No critical security vulnerabilities
- [ ] Code review completed
- [ ] Documentation updated

### 2. Version Management

- [ ] Version number updated in `__init__.py` (single source of truth)
- [ ] CHANGELOG.md updated with new version
- [ ] Migration guide written (if needed)
- [ ] Version consistency validated: `python scripts/packaging_utils.py`

### 3. Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Performance tests pass
- [ ] Manual testing completed
- [ ] Compatibility testing (Python versions)

### 4. Documentation

- [ ] API documentation updated
- [ ] User guide updated
- [ ] Examples updated
- [ ] README updated
- [ ] Migration guide (for breaking changes)

### 5. Packaging Validation

- [ ] Package configuration validated: `python scripts/packaging_utils.py`
- [ ] Package contents validated: `python scripts/validate_package.py`
- [ ] Build process tested: `uv build`
- [ ] Installation tested in clean environment
- [ ] Entry points verified: `pypi-mcp --help`
- [ ] Package metadata complete and accurate

## Release Process

### 1. Preparation Phase

#### Update Version Numbers

```bash
# Update pyproject.toml
[project]
version = "0.2.0"

# Update __init__.py
__version__ = "0.2.0"

# Verify version consistency
python -c "import pypi_mcp; print(pypi_mcp.__version__)"
```

#### Update Changelog

```markdown
# Changelog

## [0.2.0] - 2025-01-15

### Added

- New package health assessment tool
- Enhanced vulnerability checking
- Performance improvements

### Changed

- Improved error handling
- Updated dependencies

### Fixed

- Cache invalidation bug
- Rate limiting edge case

### Deprecated

- Old API endpoints (will be removed in 0.3.0)

### Security

- Fixed potential XSS vulnerability
```

#### Create Release Branch

```bash
# Create release branch
git checkout -b release/0.2.0

# Commit version updates
git add .
git commit -m "chore: prepare release 0.2.0"

# Push release branch
git push origin release/0.2.0
```

### 2. Testing Phase

#### Automated Testing

```bash
# Run full test suite
pytest

# Run performance tests
pytest -m performance

# Run integration tests
pytest -m integration

# Check code quality
black --check pypi_mcp/
mypy pypi_mcp/
ruff check pypi_mcp/
```

#### Manual Testing

```bash
# Test installation
pip install -e .

# Test basic functionality
pypi-mcp --help
pypi-mcp --log-level DEBUG

# Test with real data
# ... manual testing scenarios ...
```

#### Compatibility Testing

```bash
# Test with different Python versions
tox

# Test with different dependency versions
# ... compatibility matrix testing ...
```

### 3. Release Phase

#### Create Release PR

```bash
# Create pull request from release branch to main
# Title: "Release 0.2.0"
# Include changelog in description
```

#### Review and Merge

1. **Code Review**: At least one maintainer review
2. **CI/CD**: All automated checks pass
3. **Approval**: Release approved by maintainers
4. **Merge**: Merge to main branch

#### Tag Release

```bash
# Checkout main and pull latest
git checkout main
git pull origin main

# Create and push tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

#### GitHub Release

Create GitHub release:

1. Go to GitHub releases page
2. Click "Create a new release"
3. Select tag `v0.2.0`
4. Title: "PyPI MCP Server v0.2.0"
5. Description: Copy from CHANGELOG.md
6. Attach any release artifacts
7. Publish release

### 4. Distribution Phase

#### PyPI Release

```bash
# Build distribution packages
python -m build

# Check packages
twine check dist/*

# Upload to PyPI (test first)
twine upload --repository testpypi dist/*

# Test installation from test PyPI
pip install --index-url https://test.pypi.org/simple/ pypi-mcp

# Upload to production PyPI
twine upload dist/*
```

#### Docker Release

```bash
# Build Docker image
docker build -t pypi-mcp:0.2.0 .
docker build -t pypi-mcp:latest .

# Push to registry
docker push pypi-mcp:0.2.0
docker push pypi-mcp:latest
```

#### Documentation Release

```bash
# Update documentation site
mkdocs gh-deploy

# Update version in documentation
# ... update version references ...
```

## Post-Release Activities

### 1. Communication

#### Release Announcement

````markdown
# PyPI MCP Server v0.2.0 Released

We're excited to announce the release of PyPI MCP Server v0.2.0!

## What's New

- **Package Health Assessment**: New tool to assess package health
- **Enhanced Security**: Improved vulnerability checking
- **Performance**: 30% faster response times

## Breaking Changes

None in this release.

## Upgrade Instructions

```bash
pip install --upgrade pypi-mcp
```
````

## Full Changelog

See [CHANGELOG.md](link) for complete details.

````

#### Update Documentation

- [ ] Update version in documentation
- [ ] Update installation instructions
- [ ] Update examples with new features
- [ ] Update API documentation

### 2. Monitoring

#### Release Health

Monitor for issues after release:

- [ ] Error rates in logs
- [ ] User feedback and issues
- [ ] Performance metrics
- [ ] Download statistics

#### Issue Tracking

Track post-release issues:

```bash
# Label issues with release version
# Monitor for regressions
# Plan hotfixes if needed
````

### 3. Cleanup

#### Branch Cleanup

```bash
# Delete release branch
git branch -d release/0.2.0
git push origin --delete release/0.2.0

# Clean up local tags
git tag -l | grep -v v0.2.0 | head -5 | xargs git tag -d
```

#### Prepare for Next Release

```bash
# Create development branch for next version
git checkout -b develop/0.3.0

# Update version to next development version
# Update in pyproject.toml: version = "0.3.0.dev0"
```

## Hotfix Process

### When to Hotfix

Hotfixes are for critical issues:

- Security vulnerabilities
- Data corruption bugs
- Service-breaking issues
- Critical performance problems

### Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout main
git checkout -b hotfix/0.2.1

# 2. Apply fix
# ... make necessary changes ...

# 3. Test fix
pytest
# ... manual testing ...

# 4. Update version (patch increment)
# Update to 0.2.1

# 5. Create PR and merge
# 6. Tag and release
git tag -a v0.2.1 -m "Hotfix release 0.2.1"

# 7. Distribute
# ... PyPI, Docker, etc. ...
```

## Release Automation

### GitHub Actions

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
```

### Release Scripts

```bash
#!/bin/bash
# scripts/release.sh

set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

echo "Preparing release $VERSION"

# Update version
sed -i "s/version = .*/version = \"$VERSION\"/" pyproject.toml

# Run tests
pytest

# Build and check
python -m build
twine check dist/*

# Create tag
git add .
git commit -m "chore: release $VERSION"
git tag -a "v$VERSION" -m "Release $VERSION"

echo "Release $VERSION prepared. Push with:"
echo "git push origin main --tags"
```

## Release Metrics

### Success Metrics

Track release success:

- **Time to Release**: From code freeze to distribution
- **Issue Rate**: Post-release issues per release
- **Adoption Rate**: Download/usage statistics
- **Feedback**: User satisfaction and feedback

### Quality Metrics

Monitor release quality:

- **Test Coverage**: Maintain >90% coverage
- **Bug Escape Rate**: Bugs found after release
- **Performance**: Response time improvements
- **Security**: Vulnerability count and response time

## Rollback Procedures

### When to Rollback

Consider rollback for:

- Critical security vulnerabilities
- Data corruption issues
- Widespread functionality breakage
- Performance degradation >50%

### Rollback Process

```bash
# 1. Assess impact and decide on rollback
# 2. Communicate to users
# 3. Revert PyPI package (if possible)
# 4. Revert Docker images
# 5. Update documentation
# 6. Plan fix and re-release
```

## Next Steps

- [Development Setup](development-setup.md) - Set up development environment
- [Contributing Guidelines](contributing.md) - Learn how to contribute
- [Testing Guide](testing.md) - Comprehensive testing information
