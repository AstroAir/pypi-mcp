#!/usr/bin/env python3
"""
Packaging utilities for pypi-mcp.

This script provides various utilities for package management including
version checking, metadata validation, and build automation.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any
import re


def get_version_from_init() -> str:
    """Extract version from __init__.py file."""
    init_file = Path("pypi_mcp") / "__init__.py"
    if not init_file.exists():
        raise FileNotFoundError("pypi_mcp/__init__.py not found")

    content = init_file.read_text()
    version_match = re.search(
        r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not version_match:
        raise ValueError("Version not found in __init__.py")

    return version_match.group(1)


def validate_version_consistency() -> Dict[str, Any]:
    """Check that version is consistent across files."""
    try:
        init_version = get_version_from_init()
    except (FileNotFoundError, ValueError) as e:
        return {"valid": False, "error": str(e)}

    # Check if pyproject.toml uses dynamic versioning
    pyproject_file = Path("pyproject.toml")
    if pyproject_file.exists():
        content = pyproject_file.read_text()
        if 'dynamic = ["version"]' in content or "dynamic = ['version']" in content:
            return {
                "valid": True,
                "version": init_version,
                "source": "dynamic from __init__.py"
            }
        else:
            # Check for hardcoded version in pyproject.toml
            version_match = re.search(
                r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                pyproject_version = version_match.group(1)
                if pyproject_version != init_version:
                    return {
                        "valid": False,
                        "error": f"Version mismatch: __init__.py={init_version}, pyproject.toml={pyproject_version}"
                    }

    return {
        "valid": True,
        "version": init_version,
        "source": "__init__.py"
    }


def check_required_files() -> Dict[str, Any]:
    """Check that all required packaging files exist."""
    required_files = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "pypi_mcp/__init__.py",
        "pypi_mcp/server.py",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    return {
        "valid": len(missing_files) == 0,
        "missing_files": missing_files,
        "required_files": required_files
    }


def validate_pyproject_toml() -> Dict[str, Any]:
    """Validate pyproject.toml structure and content."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        return {"valid": False, "error": "pyproject.toml not found"}

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore
        except ImportError:
            return {"valid": False, "error": "No TOML parser available"}

    try:
        with open(pyproject_file, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        return {"valid": False, "error": f"Failed to parse pyproject.toml: {e}"}

    # Check required sections
    required_sections = ["project", "build-system"]
    missing_sections = [
        section for section in required_sections if section not in data]

    if missing_sections:
        return {
            "valid": False,
            "error": f"Missing required sections: {missing_sections}"
        }

    # Check required project fields
    project = data["project"]
    required_fields = ["name", "description",
                       "readme", "requires-python", "dependencies"]
    missing_fields = [
        field for field in required_fields if field not in project]

    if missing_fields:
        return {
            "valid": False,
            "error": f"Missing required project fields: {missing_fields}"
        }

    return {
        "valid": True,
        "project_name": project.get("name"),
        "description": project.get("description"),
        "python_requires": project.get("requires-python"),
        "dependencies": project.get("dependencies", [])
    }


def check_entry_points() -> Dict[str, Any]:
    """Check that entry points are properly configured."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        return {"valid": False, "error": "pyproject.toml not found"}

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore
        except ImportError:
            return {"valid": False, "error": "No TOML parser available"}

    try:
        with open(pyproject_file, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        return {"valid": False, "error": f"Failed to parse pyproject.toml: {e}"}

    project = data.get("project", {})
    scripts = project.get("scripts", {})

    if not scripts:
        return {"valid": False, "error": "No entry points defined"}

    # Check that entry point modules exist
    entry_point_errors = []
    for script_name, module_path in scripts.items():
        if ":" in module_path:
            module_name, function_name = module_path.split(":", 1)
        else:
            module_name = module_path
            function_name = None

        # Convert module path to file path
        file_path = Path(module_name.replace(".", "/") + ".py")
        if not file_path.exists():
            entry_point_errors.append(
                f"Entry point {script_name} references non-existent module: {module_name}")

    return {
        "valid": len(entry_point_errors) == 0,
        "scripts": scripts,
        "errors": entry_point_errors
    }


def run_build_and_validate() -> Dict[str, Any]:
    """Run the build process and validate the results."""
    print("Running build process...")

    try:
        # Clean previous builds (cross-platform)
        import shutil
        dist_dir = Path("dist")
        if dist_dir.exists():
            shutil.rmtree(dist_dir)

        # Run build
        result = subprocess.run(
            ["uv", "build"],
            capture_output=True,
            text=True,
            check=True
        )

        print("Build completed successfully")

        # Check that files were created
        dist_dir = Path("dist")
        if not dist_dir.exists():
            return {"valid": False, "error": "No dist directory created"}

        wheel_files = list(dist_dir.glob("*.whl"))
        sdist_files = list(dist_dir.glob("*.tar.gz"))

        return {
            "valid": True,
            "wheel_files": [f.name for f in wheel_files],
            "sdist_files": [f.name for f in sdist_files],
            "build_output": result.stdout
        }

    except subprocess.CalledProcessError as e:
        return {
            "valid": False,
            "error": f"Build failed: {e}",
            "stderr": e.stderr
        }


def main() -> None:
    """Main function to run all packaging checks."""
    print("PyPI MCP Packaging Utilities")
    print("=" * 40)

    all_checks_passed = True

    # Check version consistency
    print("\n1. Checking version consistency...")
    version_result = validate_version_consistency()
    if version_result["valid"]:
        print(
            f"✅ Version: {version_result['version']} ({version_result['source']})")
    else:
        print(f"❌ Version check failed: {version_result['error']}")
        all_checks_passed = False

    # Check required files
    print("\n2. Checking required files...")
    files_result = check_required_files()
    if files_result["valid"]:
        print("✅ All required files present")
    else:
        print(f"❌ Missing files: {files_result['missing_files']}")
        all_checks_passed = False

    # Validate pyproject.toml
    print("\n3. Validating pyproject.toml...")
    pyproject_result = validate_pyproject_toml()
    if pyproject_result["valid"]:
        print(
            f"✅ pyproject.toml valid (project: {pyproject_result['project_name']})")
    else:
        print(
            f"❌ pyproject.toml validation failed: {pyproject_result['error']}")
        all_checks_passed = False

    # Check entry points
    print("\n4. Checking entry points...")
    entry_points_result = check_entry_points()
    if entry_points_result["valid"]:
        print(
            f"✅ Entry points valid: {list(entry_points_result['scripts'].keys())}")
    else:
        print(f"❌ Entry points check failed: {entry_points_result['error']}")
        if entry_points_result.get("errors"):
            for error in entry_points_result["errors"]:
                print(f"   {error}")
        all_checks_passed = False

    # Run build if all checks passed
    if all_checks_passed:
        print("\n5. Running build and validation...")
        build_result = run_build_and_validate()
        if build_result["valid"]:
            print("✅ Build completed successfully")
            print(f"   Wheel files: {build_result['wheel_files']}")
            print(f"   Source files: {build_result['sdist_files']}")
        else:
            print(f"❌ Build failed: {build_result['error']}")
            all_checks_passed = False

    if all_checks_passed:
        print("\n🎉 All packaging checks passed!")
        sys.exit(0)
    else:
        print("\n💥 Some packaging checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
