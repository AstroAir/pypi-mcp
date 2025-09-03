# Contributing to PyPI MCP Server

Thank you for your interest in contributing to PyPI MCP Server! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pypi-mcp.git
   cd pypi-mcp
   ```

2. **Install dependencies**
   ```bash
   uv sync --dev
   ```

3. **Verify the setup**
   ```bash
   uv run pytest
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run the development checks**
   ```bash
   # Format code
   uv run black pypi_mcp/
   uv run isort pypi_mcp/
   
   # Lint code
   uv run ruff check pypi_mcp/
   uv run ruff format pypi_mcp/
   
   # Type checking
   uv run mypy pypi_mcp/
   
   # Run tests
   uv run pytest
   ```

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking

All code must pass these checks before being merged.

### Testing

- Write tests for all new functionality
- Ensure existing tests continue to pass
- Aim for high test coverage
- Use appropriate test markers:
  - `@pytest.mark.unit` for fast unit tests
  - `@pytest.mark.integration` for integration tests
  - `@pytest.mark.network` for tests requiring network access

### Documentation

- Update the README.md if you add new features
- Add docstrings to new functions and classes
- Update type hints for all new code
- Consider adding examples for new functionality

## Submitting Changes

### Pull Request Process

1. **Ensure your branch is up to date**
   ```bash
   git fetch origin
   git rebase origin/master
   ```

2. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Use a clear, descriptive title
   - Provide a detailed description of your changes
   - Reference any related issues
   - Include screenshots or examples if applicable

4. **Address review feedback**
   - Respond to comments promptly
   - Make requested changes
   - Push updates to your branch

### Pull Request Guidelines

- **One feature per PR**: Keep pull requests focused on a single feature or bug fix
- **Clear commit messages**: Use descriptive commit messages
- **Tests required**: All new code must include appropriate tests
- **Documentation**: Update documentation for user-facing changes
- **Breaking changes**: Clearly mark and document any breaking changes

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Python version and operating system
- Steps to reproduce the issue
- Expected vs. actual behavior
- Error messages or logs
- Minimal code example if applicable

### Feature Requests

For new features:
- Describe the use case and motivation
- Provide examples of how it would be used
- Consider backward compatibility
- Discuss implementation approach if you have ideas

### Code Contributions

We welcome contributions including:
- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

## Development Tips

### Running Specific Tests

```bash
# Run unit tests only
uv run pytest -m unit

# Run integration tests
uv run pytest -m integration

# Run tests with coverage
uv run pytest --cov=pypi_mcp
```

### Debugging

- Use the `--pdb` flag with pytest to drop into debugger on failures
- Add logging statements for debugging (use the `logging` module)
- Test your changes with real PyPI packages

### Performance Considerations

- Be mindful of API rate limits
- Use caching appropriately
- Consider async/await patterns for I/O operations
- Profile performance-critical code

## Release Process

Releases are handled by maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a GitHub release
4. Automated CI will publish to PyPI

## Getting Help

- **Issues**: Check existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Refer to the README and code documentation

## Recognition

Contributors will be recognized in:
- The project's README
- Release notes for significant contributions
- GitHub's contributor statistics

Thank you for contributing to PyPI MCP Server!
