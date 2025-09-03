# Packaging Troubleshooting

This guide helps resolve common packaging issues with pypi-mcp.

## Common Issues

### Build Failures

#### Issue: "No module named 'hatchling'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'hatchling'
```

**Solution:**
```bash
# Install build dependencies
pip install build hatchling

# Or use uv
uv add --dev build hatchling
```

#### Issue: "Version not found in __init__.py"

**Symptoms:**
```
ValueError: Version not found in __init__.py
```

**Solution:**
1. Check that `__init__.py` contains:
   ```python
   __version__ = "x.y.z"
   ```

2. Verify pyproject.toml configuration:
   ```toml
   [tool.hatch.version]
   path = "pypi_mcp/__init__.py"
   ```

#### Issue: "Build backend not found"

**Symptoms:**
```
ERROR: Could not build wheels for pypi-mcp
```

**Solution:**
```bash
# Update build tools
pip install --upgrade build setuptools wheel

# Clean and rebuild
rm -rf dist/ build/ *.egg-info/
uv build
```

### Validation Failures

#### Issue: "Missing required files"

**Symptoms:**
```
❌ Missing required files: {'pypi_mcp/__init__.py'}
```

**Solution:**
1. Check file exists: `ls pypi_mcp/__init__.py`
2. Update MANIFEST.in if needed:
   ```
   recursive-include pypi_mcp *.py
   ```
3. Rebuild: `uv build`

#### Issue: "Entry points not working"

**Symptoms:**
```
❌ Entry points check failed
```

**Solution:**
1. Verify pyproject.toml entry points:
   ```toml
   [project.scripts]
   pypi-mcp = "pypi_mcp.server:main"
   ```

2. Check target module exists:
   ```bash
   python -c "from pypi_mcp.server import main"
   ```

3. Test after installation:
   ```bash
   pip install -e .
   pypi-mcp --help
   ```

### Installation Issues

#### Issue: "Package not found after installation"

**Symptoms:**
```
ModuleNotFoundError: No module named 'pypi_mcp'
```

**Solution:**
1. Check installation location:
   ```bash
   pip show pypi-mcp
   ```

2. Verify Python path:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. Reinstall in development mode:
   ```bash
   pip install -e .
   ```

#### Issue: "Entry point command not found"

**Symptoms:**
```
bash: pypi-mcp: command not found
```

**Solution:**
1. Check if scripts directory is in PATH:
   ```bash
   python -m site --user-base
   ```

2. Add to PATH or use full path:
   ```bash
   python -m pypi_mcp.server
   ```

3. Reinstall with --force-reinstall:
   ```bash
   pip install --force-reinstall .
   ```

### Metadata Issues

#### Issue: "Invalid classifier"

**Symptoms:**
```
WARNING: Invalid classifier: 'Topic :: Invalid'
```

**Solution:**
1. Check valid classifiers at: https://pypi.org/classifiers/
2. Update pyproject.toml with valid classifiers
3. Validate with: `python scripts/packaging_utils.py`

#### Issue: "README not found"

**Symptoms:**
```
FileNotFoundError: README.md not found
```

**Solution:**
1. Ensure README.md exists in project root
2. Check pyproject.toml configuration:
   ```toml
   readme = {file = "README.md", content-type = "text/markdown"}
   ```

## Diagnostic Commands

### Check Package Configuration

```bash
# Validate packaging setup
python scripts/packaging_utils.py

# Check specific issues
python -c "
import tomllib
with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
    print('Project name:', data['project']['name'])
    print('Version source:', data.get('project', {}).get('dynamic', []))
"
```

### Inspect Built Packages

```bash
# List wheel contents
python -m zipfile -l dist/*.whl

# List source distribution contents
python -m tarfile -l dist/*.tar.gz

# Check metadata
python -c "
import zipfile
with zipfile.ZipFile('dist/pypi_mcp-*.whl') as z:
    print(z.read('pypi_mcp-*/METADATA').decode())
"
```

### Test Installation

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install and test
pip install dist/*.whl
python -c "import pypi_mcp; print(pypi_mcp.__version__)"
pypi-mcp --help

# Cleanup
deactivate
rm -rf test_env
```

## Environment Issues

### Python Version Compatibility

**Issue:** Package fails on different Python versions

**Solution:**
1. Check supported versions in pyproject.toml:
   ```toml
   requires-python = ">=3.11"
   ```

2. Test with multiple Python versions:
   ```bash
   python3.11 -m pip install .
   python3.12 -m pip install .
   ```

### Virtual Environment Issues

**Issue:** Package works in one environment but not another

**Solution:**
1. Check Python version: `python --version`
2. Check installed packages: `pip list`
3. Compare environments: `pip freeze > requirements.txt`
4. Create clean environment and test

### Path Issues

**Issue:** Import errors or command not found

**Solution:**
1. Check PYTHONPATH: `echo $PYTHONPATH`
2. Check PATH: `echo $PATH`
3. Use absolute imports in code
4. Install in development mode: `pip install -e .`

## Advanced Debugging

### Enable Verbose Output

```bash
# Verbose build
uv build --verbose

# Verbose pip install
pip install -v .

# Debug import issues
python -v -c "import pypi_mcp"
```

### Check Dependencies

```bash
# List all dependencies
pip show pypi-mcp

# Check for conflicts
pip check

# Verify specific imports
python -c "
try:
    import fastmcp
    import httpx
    import pydantic
    print('All dependencies available')
except ImportError as e:
    print(f'Missing dependency: {e}')
"
```

### Platform-Specific Issues

#### Windows

- Use PowerShell or Command Prompt
- Check for path separator issues (`\` vs `/`)
- Verify file permissions

#### macOS/Linux

- Check file permissions: `ls -la`
- Verify shell configuration
- Check for case sensitivity issues

## Getting Help

If issues persist:

1. **Check logs**: Look for detailed error messages
2. **Search issues**: Check GitHub issues for similar problems
3. **Create minimal reproduction**: Isolate the problem
4. **Report bug**: Include full error messages and environment details

### Information to Include

When reporting packaging issues:

- Python version: `python --version`
- Operating system and version
- Package manager: `pip --version` or `uv --version`
- Full error message and traceback
- Steps to reproduce
- Contents of pyproject.toml (relevant sections)
- Output of `python scripts/packaging_utils.py`
