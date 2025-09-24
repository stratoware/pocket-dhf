# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Test runner script for Pocket DHF."""

import os
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run the test suite with coverage reporting."""
    # Ensure we're in the project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Run pytest with coverage
    cmd = [
        "poetry",
        "run",
        "pytest",
        "--cov=app",
        "--cov-report=html:reports/coverage-html",
        "--cov-report=xml:reports/coverage.xml",
        "--cov-report=term-missing",
        "--html=reports/test-report.html",
        "--self-contained-html",
        "--junitxml=reports/junit.xml",
        "--cov-fail-under=80",
        "-v",
        "tests/",
    ]

    print("Running test suite...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report: reports/coverage-html/index.html")
        print("📋 Test report: reports/test-report.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())
