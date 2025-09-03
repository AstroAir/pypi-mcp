# Packaging Guide

This guide covers the packaging system for pypi-mcp, including building, validating, and distributing the package.

## Overview

The pypi-mcp project uses modern Python packaging standards with:

- **pyproject.toml** for project configuration
- **hatchling** as the build backend
- **Dynamic versioning** from `__init__.py`
- **MANIFEST.in** for explicit file inclusion control
- **Automated validation** scripts for package integrity

## Project Structure

```
pypi-mcp/
├── pyproject.toml          # Main project configuration
├── MANIFEST.in             # File inclusion rules
├── pypi_mcp/              # Main package
│   ├── __init__.py        # Version definition
│   └── ...                # Package modules
├── scripts/               # Packaging utilities
│   ├── packaging_utils.py # Build and validation tools
│   └── validate_package.py # Package content validation
├── tests/                 # Test suite
├── docs/                  # Documentation
└── dist/                  # Built packages (generated)
```

## Configuration Files

### pyproject.toml

The main configuration file defines:

- **Project metadata**: name, description, authors, keywords
- **Dependencies**: runtime and optional development dependencies
- **Build system**: hatchling configuration
- **Dynamic versioning**: reads version from `__init__.py`
- **Entry points**: CLI scripts and console commands
- **Tool configurations**: pytest, mypy, etc.

Key sections:
```toml
[project]
name = "pypi-mcp"
dynamic = ["version"]
description = "A comprehensive MCP server for PyPI package information"
readme = {file = "README.md", content-type = "text/markdown"}
license = {text = "MIT"}

[tool.hatch.version]
path = "pypi_mcp/__init__.py"
```

### MANIFEST.in

Controls which files are included in the source distribution:

```
# Include documentation
include README.md LICENSE CHANGELOG.md

# Include configuration
include pyproject.toml

# Include package data
recursive-include pypi_mcp *

# Exclude build artifacts
global-exclude *.pyc __pycache__
```

## Version Management

The project uses a single source of truth for versioning:

1. **Version definition**: Set in `pypi_mcp/__init__.py`
   ```python
   __version__ = "0.1.0"
   ```

2. **Dynamic reading**: pyproject.toml reads version automatically
   ```toml
   [project]
   dynamic = ["version"]
   
   [tool.hatch.version]
   path = "pypi_mcp/__init__.py"
   ```

3. **Validation**: Scripts ensure version consistency across files

## Building Packages

### Prerequisites

- Python 3.11 or higher
- uv package manager (recommended) or pip

### Build Commands

```bash
# Clean previous builds
rm -rf dist/

# Build both wheel and source distribution
uv build

# Or using pip/build
python -m build
```

This creates:
- `dist/pypi_mcp-{version}-py3-none-any.whl` (wheel)
- `dist/pypi_mcp-{version}.tar.gz` (source distribution)

### Build Validation

Use the provided scripts to validate builds:

```bash
# Check packaging configuration
python scripts/packaging_utils.py

# Validate built packages
python scripts/validate_package.py

# Complete workflow (if make is available)
make package
```

## Package Validation

The validation scripts check:

### packaging_utils.py

- ✅ Version consistency across files
- ✅ Required files presence
- ✅ pyproject.toml structure
- ✅ Entry points configuration
- ✅ Build process execution

### validate_package.py

- ✅ Wheel content validation
- ✅ Source distribution content
- ✅ Package installation testing
- ✅ Entry point functionality
- ✅ Import verification

## Distribution

### Local Testing

```bash
# Install from wheel
pip install dist/pypi_mcp-*.whl

# Install in development mode
pip install -e .

# Test installation
pypi-mcp --help
python -c "import pypi_mcp; print(pypi_mcp.__version__)"
```

### PyPI Upload

```bash
# Install upload tools
pip install twine

# Check package
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Troubleshooting

### Common Issues

1. **Version mismatch errors**
   - Ensure version is only defined in `__init__.py`
   - Check that pyproject.toml uses dynamic versioning

2. **Missing files in distribution**
   - Update MANIFEST.in to include required files
   - Verify with `python -m tarfile -l dist/*.tar.gz`

3. **Build failures**
   - Check pyproject.toml syntax
   - Ensure all dependencies are available
   - Verify Python version compatibility

4. **Entry point issues**
   - Check module paths in pyproject.toml
   - Ensure target modules exist
   - Test entry points after installation

### Validation Failures

If validation scripts fail:

1. **Check file paths**: Ensure all required files exist
2. **Verify metadata**: Check pyproject.toml completeness
3. **Test build**: Run `uv build` manually
4. **Check dependencies**: Ensure all imports work

## Best Practices

### Before Release

1. **Update version** in `__init__.py`
2. **Update CHANGELOG.md** with changes
3. **Run full test suite**: `pytest`
4. **Validate packaging**: `python scripts/packaging_utils.py`
5. **Test installation**: `python scripts/validate_package.py`
6. **Check metadata**: Ensure all fields are current

### Metadata Maintenance

- Keep **classifiers** up to date
- Update **Python version** support as needed
- Maintain **keywords** for discoverability
- Update **project URLs** if they change
- Review **dependencies** regularly

### Security Considerations

- **Pin dependencies** for reproducible builds
- **Scan for vulnerabilities** in dependencies
- **Sign packages** for distribution
- **Use secure upload** methods (API tokens)

## Automation

### CI/CD Integration

The packaging system integrates with CI/CD:

```yaml
# Example GitHub Actions
- name: Build package
  run: uv build

- name: Validate package
  run: python scripts/validate_package.py

- name: Upload to PyPI
  if: github.event_name == 'release'
  run: twine upload dist/*
```

### Make Targets

If make is available:

```bash
make clean          # Clean build artifacts
make build          # Build packages
make validate-package # Validate built packages
make check-packaging  # Check configuration
make package         # Complete build and validation
```

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Hatchling Documentation](https://hatch.pypa.io/latest/)
- [PyPI Upload Guide](https://packaging.python.org/tutorials/packaging-projects/)
