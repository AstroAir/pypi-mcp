#!/usr/bin/env python3
"""
Package validation script for pypi-mcp.

This script validates that the built package contains all necessary files
and metadata, and that it can be installed and imported correctly.
"""

import os
import sys
import subprocess
import tempfile
import zipfile
import tarfile
from pathlib import Path
from typing import List, Set, Dict, Any, Optional
import json


def run_command(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess[str]:
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise


def validate_wheel_contents(wheel_path: Path) -> Dict[str, Any]:
    """Validate the contents of a wheel file."""
    print(f"Validating wheel: {wheel_path}")

    required_files = {
        "pypi_mcp/__init__.py",
        "pypi_mcp/server.py",
        "pypi_mcp/client.py",
        "pypi_mcp/models.py",
        "pypi_mcp/config.py",
        "pypi_mcp/cache.py",
        "pypi_mcp/utils.py",
        "pypi_mcp/exceptions.py",
    }

    found_files = set()
    metadata_files = []

    with zipfile.ZipFile(wheel_path, 'r') as zf:
        for file_info in zf.filelist:
            found_files.add(file_info.filename)
            if file_info.filename.endswith('.dist-info/METADATA'):
                metadata_files.append(file_info.filename)

    # Check required files
    missing_files = required_files - found_files
    if missing_files:
        return {
            "valid": False,
            "errors": [f"Missing required files: {missing_files}"]
        }

    # Check metadata
    if not metadata_files:
        return {
            "valid": False,
            "errors": ["No METADATA file found in wheel"]
        }

    return {
        "valid": True,
        "files": list(found_files),
        "metadata_files": metadata_files
    }


def validate_sdist_contents(sdist_path: Path) -> Dict[str, Any]:
    """Validate the contents of a source distribution."""
    print(f"Validating source distribution: {sdist_path}")

    required_files = {
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "pypi_mcp/__init__.py",
        "pypi_mcp/server.py",
    }

    found_files = set()

    with tarfile.open(sdist_path, 'r:gz') as tf:
        for member in tf.getmembers():
            if member.isfile():
                # Remove the top-level directory from the path
                path_parts = Path(member.name).parts
                if len(path_parts) > 1:
                    relative_path = str(Path(*path_parts[1:]))
                    # Normalize path separators for cross-platform compatibility
                    normalized_path = relative_path.replace('\\', '/')
                    found_files.add(normalized_path)

    # Check required files
    missing_files = required_files - found_files
    if missing_files:
        return {
            "valid": False,
            "errors": [f"Missing required files: {missing_files}"]
        }

    return {
        "valid": True,
        "files": list(found_files)
    }


def test_package_installation(wheel_path: Path) -> Dict[str, Any]:
    """Test that the package can be installed and imported."""
    print("Testing package installation...")

    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = Path(temp_dir) / "test_venv"

        # Create virtual environment
        try:
            run_command([sys.executable, "-m", "venv", str(venv_dir)])
        except subprocess.CalledProcessError:
            return {
                "valid": False,
                "errors": ["Failed to create virtual environment"]
            }

        # Determine python executable in venv
        if os.name == 'nt':  # Windows
            python_exe = venv_dir / "Scripts" / "python.exe"
        else:  # Unix-like
            python_exe = venv_dir / "bin" / "python"

        try:
            # Install the wheel
            run_command([str(python_exe), "-m", "pip",
                        "install", str(wheel_path)])

            # Test import
            result = run_command([
                str(python_exe), "-c",
                "import pypi_mcp; print(f'Version: {pypi_mcp.__version__}')"
            ])

            # Test entry point
            entry_result = run_command(
                [str(python_exe), "-m", "pypi_mcp.server", "--help"])

            return {
                "valid": True,
                "import_output": result.stdout.strip(),
                "entry_point_works": "--help" in entry_result.stdout or "usage:" in entry_result.stdout.lower()
            }

        except subprocess.CalledProcessError as e:
            return {
                "valid": False,
                "errors": [f"Installation or import failed: {e}"]
            }


def main() -> None:
    """Main validation function."""
    print("PyPI MCP Package Validation")
    print("=" * 40)

    # Find distribution files
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ No dist directory found. Run 'uv build' first.")
        sys.exit(1)

    wheel_files = list(dist_dir.glob("*.whl"))
    sdist_files = list(dist_dir.glob("*.tar.gz"))

    if not wheel_files:
        print("❌ No wheel files found in dist/")
        sys.exit(1)

    if not sdist_files:
        print("❌ No source distribution files found in dist/")
        sys.exit(1)

    all_valid = True

    # Validate wheel
    for wheel_file in wheel_files:
        wheel_result = validate_wheel_contents(wheel_file)
        if wheel_result["valid"]:
            print(f"✅ Wheel validation passed: {wheel_file.name}")
        else:
            print(f"❌ Wheel validation failed: {wheel_file.name}")
            for error in wheel_result["errors"]:
                print(f"   {error}")
            all_valid = False

    # Validate source distribution
    for sdist_file in sdist_files:
        sdist_result = validate_sdist_contents(sdist_file)
        if sdist_result["valid"]:
            print(
                f"✅ Source distribution validation passed: {sdist_file.name}")
        else:
            print(
                f"❌ Source distribution validation failed: {sdist_file.name}")
            for error in sdist_result["errors"]:
                print(f"   {error}")
            all_valid = False

    # Test installation
    if wheel_files and all_valid:
        install_result = test_package_installation(wheel_files[0])
        if install_result["valid"]:
            print("✅ Package installation test passed")
            print(f"   {install_result['import_output']}")
            if install_result.get("entry_point_works"):
                print("✅ Entry point test passed")
            else:
                print("⚠️  Entry point test inconclusive")
        else:
            print("❌ Package installation test failed")
            for error in install_result["errors"]:
                print(f"   {error}")
            all_valid = False

    if all_valid:
        print("\n🎉 All package validations passed!")
        sys.exit(0)
    else:
        print("\n💥 Some package validations failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
