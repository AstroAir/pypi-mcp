# Contributing Guidelines

Welcome to the PyPI MCP Server project! This guide will help you contribute effectively to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our Code of Conduct:

- **Be respectful**: Treat all community members with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be collaborative**: Work together to improve the project
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning and growing

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/pypi-mcp.git
cd pypi-mcp

# Add upstream remote
git remote add upstream https://github.com/AstroAir/pypi-mcp.git
```

### 2. Set Up Development Environment

Follow the [Development Setup Guide](development-setup.md) to set up your local environment.

### 3. Create a Branch

```bash
# Create a new branch for your contribution
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

## Types of Contributions

### 🐛 Bug Reports

Help us improve by reporting bugs:

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating issues
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Error messages and logs

#### Bug Report Template

```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**

1. Step one
2. Step two
3. Step three

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**

- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- PyPI MCP Version: [e.g., 0.1.0]

**Additional Context**
Any other relevant information.
```

### 💡 Feature Requests

Suggest new features or improvements:

1. **Check existing issues** for similar requests
2. **Use the feature request template**
3. **Explain the use case** and benefits
4. **Consider implementation complexity**

#### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Explain why this feature would be useful.

**Proposed Solution**
Describe how you envision this feature working.

**Alternatives Considered**
Any alternative solutions you've considered.

**Additional Context**
Any other relevant information.
```

### 🔧 Code Contributions

Contribute code improvements:

1. **Start with an issue** - discuss before implementing
2. **Follow coding standards** - see below
3. **Write tests** - ensure good test coverage
4. **Update documentation** - keep docs current
5. **Submit a pull request** - follow the PR template

## Coding Standards

### Code Style

We use automated tools to maintain consistent code style:

```bash
# Format code with black
black pypi_mcp/ tests/

# Sort imports with isort
isort pypi_mcp/ tests/

# Type check with mypy
mypy pypi_mcp/

# Lint with ruff
ruff check pypi_mcp/ tests/
```

### Code Quality Guidelines

#### 1. Type Hints

Always use type hints for function parameters and return values:

```python
# Good
async def get_package_info(package_name: str, version: Optional[str] = None) -> PackageInfo:
    """Get package information."""

# Bad
async def get_package_info(package_name, version=None):
    """Get package information."""
```

#### 2. Docstrings

Write clear docstrings for all public functions and classes:

```python
def validate_package_name(name: str) -> bool:
    """
    Validate package name according to PyPI rules.

    Args:
        name: The package name to validate

    Returns:
        True if the name is valid, False otherwise

    Examples:
        >>> validate_package_name("requests")
        True
        >>> validate_package_name("-invalid")
        False
    """
```

#### 3. Error Handling

Use specific exception types and provide helpful error messages:

```python
# Good
if not validate_package_name(package_name):
    raise ValidationError(
        "package_name",
        package_name,
        "Invalid package name format"
    )

# Bad
if not validate_package_name(package_name):
    raise Exception("Invalid name")
```

#### 4. Async Best Practices

Follow async/await best practices:

```python
# Good - use async context manager
async with client:
    result = await client.get_package_info(package_name)

# Good - handle exceptions in async code
try:
    result = await async_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise

# Bad - blocking call in async function
def blocking_operation():
    time.sleep(1)  # Don't do this in async code
```

### Testing Requirements

#### 1. Test Coverage

- Aim for >90% test coverage
- Write tests for all new functionality
- Include both positive and negative test cases

#### 2. Test Categories

Use appropriate test markers:

```python
@pytest.mark.unit
async def test_validation_logic():
    """Unit test for validation logic."""

@pytest.mark.integration
@pytest.mark.network
async def test_real_api_call():
    """Integration test with real API."""
```

#### 3. Test Structure

Follow the Arrange-Act-Assert pattern:

```python
async def test_get_package_info():
    # Arrange
    package_name = "requests"
    expected_name = "requests"

    # Act
    result = await get_package_info(package_name)

    # Assert
    assert result.name == expected_name
    assert result.version is not None
```

## Pull Request Process

### 1. Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### 2. Pull Request Template

```markdown
## Description

Brief description of the changes.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] New tests added for new functionality

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### 3. Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers review the code
3. **Feedback**: Address any feedback or requested changes
4. **Approval**: Once approved, the PR will be merged

### 4. Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```
feat(tools): add package health assessment tool

Add new tool to assess package health based on various metrics
including vulnerabilities, maintenance status, and version type.

Closes #123
```

```
fix(client): handle rate limiting in PyPI client

Add exponential backoff retry logic when PyPI rate limits are hit.
This prevents the client from failing immediately on rate limit errors.

Fixes #456
```

## Documentation Contributions

### 1. Documentation Types

- **API Documentation**: Tool, resource, and prompt references
- **User Guides**: Configuration, usage examples, troubleshooting
- **Developer Guides**: Architecture, contributing, testing
- **Examples**: Code examples and tutorials

### 2. Documentation Standards

- Use clear, concise language
- Include code examples where appropriate
- Add cross-references to related sections
- Follow MkDocs formatting conventions
- Test all code examples

### 3. Building Documentation

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

## Release Process

### 1. Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### 2. Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version number is bumped
- [ ] Release notes are prepared

### 3. Release Timeline

- **Patch releases**: As needed for critical bugs
- **Minor releases**: Monthly or when significant features are ready
- **Major releases**: When breaking changes are necessary

## Community Guidelines

### 1. Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions and reviews

### 2. Getting Help

If you need help:

1. **Check the documentation** first
2. **Search existing issues** for similar problems
3. **Ask in GitHub Discussions** for general questions
4. **Create an issue** for bugs or specific problems

### 3. Helping Others

Ways to help the community:

- Answer questions in discussions
- Review pull requests
- Improve documentation
- Report bugs
- Suggest improvements

## Recognition

We value all contributions and recognize contributors in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Acknowledgment of significant contributions
- **GitHub**: Contributor badges and statistics

## Development Workflow

### 1. Typical Workflow

```bash
# 1. Sync with upstream
git checkout main
git pull upstream main

# 2. Create feature branch
git checkout -b feature/new-tool

# 3. Make changes
# ... edit files ...

# 4. Run tests and quality checks
pytest
black pypi_mcp/ tests/
mypy pypi_mcp/

# 5. Commit changes
git add .
git commit -m "feat(tools): add new analysis tool"

# 6. Push to your fork
git push origin feature/new-tool

# 7. Create pull request on GitHub
```

### 2. Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream changes
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

### 3. Handling Merge Conflicts

```bash
# If conflicts occur during merge
git status  # See conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "resolve merge conflicts"
```

## Advanced Contributing

### 1. Adding New Tools

To add a new tool:

1. Define the tool function in `server.py`
2. Add appropriate type hints and validation
3. Write comprehensive tests
4. Update API documentation
5. Add usage examples

### 2. Extending Data Models

To add new data models:

1. Define Pydantic models in `models.py`
2. Add validation logic
3. Update serialization/deserialization
4. Write model tests
5. Update documentation

### 3. Performance Improvements

For performance contributions:

1. Profile the current implementation
2. Identify bottlenecks
3. Implement optimizations
4. Add performance tests
5. Document performance characteristics

## Questions?

If you have questions about contributing:

- Check the [FAQ](../troubleshooting/faq.md)
- Ask in [GitHub Discussions](https://github.com/AstroAir/pypi-mcp/discussions)
- Review existing [issues](https://github.com/AstroAir/pypi-mcp/issues)

Thank you for contributing to PyPI MCP Server! 🎉
