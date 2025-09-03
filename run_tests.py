#!/usr/bin/env python3
"""
Comprehensive test runner for the PyPI MCP server.

This script provides different test execution modes following FastMCP testing best practices:
- Unit tests (fast, mocked dependencies)
- Integration tests (real API calls)
- Performance tests (caching, concurrency)
- All tests with coverage reporting
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def run_unit_tests():
    """Run unit tests (fast, mocked dependencies)."""
    cmd = [
        "uv", "run", "pytest",
        "tests/test_server.py",
        "tests/test_error_handling.py",
        "tests/test_config.py",
        "-m", "not integration and not performance",
        "-v"
    ]
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests (may hit real APIs)."""
    cmd = [
        "uv", "run", "pytest",
        "tests/test_integration.py",
        "-m", "integration",
        "-v",
        "--tb=long"
    ]
    return run_command(cmd, "Integration Tests")


def run_performance_tests():
    """Run performance and caching tests."""
    cmd = [
        "uv", "run", "pytest",
        "tests/test_performance.py",
        "-v",
        "--tb=long"
    ]
    return run_command(cmd, "Performance Tests")


def run_all_tests():
    """Run all tests."""
    cmd = [
        "uv", "run", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "All Tests")


def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    cmd = [
        "uv", "run", "pytest",
        "tests/",
        "--cov=pypi_mcp",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "-v"
    ]
    return run_command(cmd, "All Tests with Coverage")


def run_specific_test(test_path):
    """Run a specific test file or test function."""
    cmd = [
        "uv", "run", "pytest",
        test_path,
        "-v",
        "--tb=long"
    ]
    return run_command(cmd, f"Specific Test: {test_path}")


def run_linting():
    """Run code linting and formatting checks."""
    commands = [
        (["uv", "run", "black", "--check", "pypi_mcp/", "tests/"], "Black formatting check"),
        (["uv", "run", "isort", "--check-only", "pypi_mcp/", "tests/"], "Import sorting check"),
        (["uv", "run", "ruff", "check", "pypi_mcp/", "tests/"], "Ruff linting"),
        (["uv", "run", "mypy", "pypi_mcp/"], "Type checking"),
    ]
    
    all_passed = True
    for cmd, description in commands:
        if not run_command(cmd, description):
            all_passed = False
    
    return all_passed


def run_security_checks():
    """Run security checks on dependencies."""
    # Note: This would require additional security tools
    print("\n🔒 Security checks would go here (e.g., safety, bandit)")
    return True


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="PyPI MCP Server Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --unit                    # Run unit tests only
  python run_tests.py --integration             # Run integration tests
  python run_tests.py --performance             # Run performance tests
  python run_tests.py --all                     # Run all tests
  python run_tests.py --coverage                # Run all tests with coverage
  python run_tests.py --lint                    # Run linting checks
  python run_tests.py --ci                      # Run CI pipeline (unit + lint)
  python run_tests.py --test tests/test_server.py::TestMCPToolsIntegration::test_get_package_info_tool
        """
    )
    
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--security", action="store_true", help="Run security checks")
    parser.add_argument("--ci", action="store_true", help="Run CI pipeline (unit tests + linting)")
    parser.add_argument("--test", type=str, help="Run specific test file or function")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # If no specific test type is specified, run unit tests by default
    if not any([args.unit, args.integration, args.performance, args.all, 
                args.coverage, args.lint, args.security, args.ci, args.test]):
        args.unit = True
    
    success = True
    
    print("🧪 PyPI MCP Server Test Runner")
    print(f"📁 Working directory: {Path.cwd()}")
    
    if args.test:
        success &= run_specific_test(args.test)
    
    if args.unit:
        success &= run_unit_tests()
    
    if args.integration:
        success &= run_integration_tests()
    
    if args.performance:
        success &= run_performance_tests()
    
    if args.all:
        success &= run_all_tests()
    
    if args.coverage:
        success &= run_tests_with_coverage()
    
    if args.lint:
        success &= run_linting()
    
    if args.security:
        success &= run_security_checks()
    
    if args.ci:
        print("\n🚀 Running CI Pipeline")
        success &= run_unit_tests()
        success &= run_linting()
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests passed successfully!")
        print("\nNext steps:")
        print("- Run integration tests: python run_tests.py --integration")
        print("- Run with coverage: python run_tests.py --coverage")
        print("- Run performance tests: python run_tests.py --performance")
    else:
        print("❌ Some tests failed. Please check the output above.")
        print("\nTroubleshooting:")
        print("- Check test output for specific failures")
        print("- Run individual test files to isolate issues")
        print("- Ensure all dependencies are installed: uv sync --dev")
    print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
