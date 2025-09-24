#!/usr/bin/env python3
"""
Python Docstring Checker

This script checks that all Python classes have proper docstrings.

Copyright (c) 2025 Stratoware LLC. All rights reserved.
"""

import argparse
import ast
import sys
from pathlib import Path
from typing import List, Optional, Tuple


class DocstringChecker:
    """Checks for missing docstrings in Python classes."""

    def __init__(self, fix_mode: bool = False):
        """Initialize the docstring checker.

        Args:
            fix_mode: If True, automatically add missing docstrings
        """
        self.fix_mode = fix_mode
        self.errors = []

    def get_class_info(
        self, node: ast.ClassDef, source_lines: List[str]
    ) -> Tuple[str, int, Optional[str]]:
        """Extract information about a class definition.

        Args:
            node: AST node representing the class
            source_lines: Source code lines

        Returns:
            Tuple of (class_name, line_number, existing_docstring)
        """
        class_name = node.name
        line_number = node.lineno

        # Check if class has a docstring
        docstring = None
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            docstring = node.body[0].value.value

        return class_name, line_number, docstring

    def generate_default_docstring(self, class_name: str) -> str:
        """Generate a default docstring for a class.

        Args:
            class_name: Name of the class

        Returns:
            Default docstring text
        """
        return f'"""{class_name} class."""'

    def add_docstring_to_class(
        self, file_path: Path, class_name: str, line_number: int
    ) -> bool:
        """Add a docstring to a class that's missing one.

        Args:
            file_path: Path to the Python file
            class_name: Name of the class
            line_number: Line number where the class is defined

        Returns:
            True if docstring was added successfully
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Find the class definition line
            class_line_idx = line_number - 1  # Convert to 0-based index

            # Find the next line after the class definition that contains code
            insert_idx = class_line_idx + 1

            # Skip any decorators or comments immediately after class definition
            while insert_idx < len(lines):
                line = lines[insert_idx].strip()
                if line and not line.startswith("#"):
                    break
                insert_idx += 1

            # Determine the indentation level
            class_line = lines[class_line_idx]
            class_indent = len(class_line) - len(class_line.lstrip())
            docstring_indent = " " * (class_indent + 4)  # Add 4 spaces for class body

            # Create the docstring
            docstring = self.generate_default_docstring(class_name)
            docstring_lines = [
                f"{docstring_indent}{docstring}\n",
                f"{docstring_indent}\n",  # Add blank line after docstring
            ]

            # Insert the docstring
            for i, docstring_line in enumerate(docstring_lines):
                lines.insert(insert_idx + i, docstring_line)

            # Write the file back
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return True

        except Exception as e:
            self.errors.append(
                f"Error adding docstring to {file_path}:{line_number}: {e}"
            )
            return False

    def check_file(self, file_path: Path) -> bool:
        """Check a single Python file for class docstrings.

        Args:
            file_path: Path to the Python file to check

        Returns:
            True if all classes have docstrings or were fixed
            False if classes are missing docstrings and not in fix mode
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                source_lines = content.splitlines()
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return False

        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False

        # Find all class definitions
        classes_without_docstrings = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name, line_number, docstring = self.get_class_info(
                    node, source_lines
                )

                if not docstring or not docstring.strip():
                    classes_without_docstrings.append((class_name, line_number))

        if not classes_without_docstrings:
            return True

        if self.fix_mode:
            # Try to add docstrings
            success = True
            for class_name, line_number in classes_without_docstrings:
                if self.add_docstring_to_class(file_path, class_name, line_number):
                    print(
                        f"✅ Added docstring to class {class_name} in {file_path}:{line_number}"
                    )
                else:
                    success = False
            return success
        else:
            # Report missing docstrings
            for class_name, line_number in classes_without_docstrings:
                self.errors.append(
                    f"Missing docstring in class {class_name} at {file_path}:{line_number}"
                )
            return False

    def check_files(self, file_paths: List[Path]) -> bool:
        """Check multiple files for class docstrings.

        Args:
            file_paths: List of Python files to check

        Returns:
            True if all classes have docstrings
            False if any classes are missing docstrings
        """
        all_good = True
        for file_path in file_paths:
            if file_path.suffix == ".py":
                if not self.check_file(file_path):
                    all_good = False

        return all_good


def main():
    """Main entry point for the docstring checker."""
    parser = argparse.ArgumentParser(
        description="Check that all Python classes have docstrings"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Python files to check (if none provided, checks all .py files)",
    )
    parser.add_argument(
        "--fix", action="store_true", help="Automatically add missing docstrings"
    )

    args = parser.parse_args()

    # Get files to check
    if args.files:
        file_paths = [
            Path(f) for f in args.files if Path(f).exists() and Path(f).suffix == ".py"
        ]
    else:
        # Find all Python files in the project
        project_root = Path(__file__).parent.parent
        file_paths = list(project_root.glob("**/*.py"))

        # Filter out unwanted directories
        exclude_patterns = [
            "__pycache__",
            ".git",
            ".pytest_cache",
            "build",
            "dist",
            ".venv",
            "venv",
            "node_modules",
            "htmlcov",
        ]

        file_paths = [
            f
            for f in file_paths
            if not any(exclude in str(f) for exclude in exclude_patterns)
        ]

    if not file_paths:
        print("No Python files to check")
        return 0

    # Check files
    checker = DocstringChecker(fix_mode=args.fix)
    success = checker.check_files(file_paths)

    # Report results
    if checker.errors:
        for error in checker.errors:
            print(f"❌ {error}")

    if success:
        print(f"✅ All classes in {len(file_paths)} Python files have docstrings")
        return 0
    else:
        print(f"\n❌ Found {len(checker.errors)} classes with missing docstrings")
        if not args.fix:
            print("Run with --fix to automatically add basic docstrings")
        return 1


if __name__ == "__main__":
    sys.exit(main())
