#!/usr/bin/env python3
"""
Copyright Header Checker and Enforcer

This script checks that all source files have proper copyright headers
and can optionally add them automatically.

Copyright (c) 2025 Stratoware LLC. All rights reserved.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class CopyrightChecker:
    """Checks and enforces copyright headers in source files."""

    COPYRIGHT_PATTERNS = {
        "python": {
            "extensions": [".py"],
            "copyright_format": (
                '"""\n{description}\n\n'
                "Copyright (c) {year} Stratoware LLC. All rights reserved.\n"
                '"""'
            ),
            "shebang_format": (
                "#!/usr/bin/env python3\n"
                '"""\n{description}\n\n'
                "Copyright (c) {year} Stratoware LLC. All rights reserved.\n"
                '"""'
            ),
            "regex": r"Copyright \(c\) \d{4} Stratoware LLC\. All rights reserved\.",
        },
        "html": {
            "extensions": [".html", ".htm"],
            "copyright_format": (
                "<!--\n{description}\n\n"
                "Copyright (c) {year} Stratoware LLC. All rights reserved.\n"
                "-->"
            ),
            "regex": r"Copyright \(c\) \d{4} Stratoware LLC\. All rights reserved\.",
        },
        "yaml": {
            "extensions": [".yml", ".yaml"],
            "copyright_format": (
                "# {description}\n"
                "# Copyright (c) {year} Stratoware LLC. All rights reserved."
            ),
            "regex": r"# Copyright \(c\) \d{4} Stratoware LLC\. All rights reserved\.",
        },
    }

    def __init__(self, fix_mode: bool = False, year: Optional[int] = None):
        """Initialize the copyright checker.

        Args:
            fix_mode: If True, automatically add missing copyright headers
            year: Copyright year to use (defaults to current year)
        """
        self.fix_mode = fix_mode
        self.year = year or datetime.now().year
        self.errors = []

    def get_file_type(self, file_path: Path) -> Optional[str]:
        """Determine the file type based on extension."""
        suffix = file_path.suffix.lower()
        for file_type, config in self.COPYRIGHT_PATTERNS.items():
            if suffix in config["extensions"]:
                return file_type
        return None

    def has_copyright(self, content: str, file_type: str) -> bool:
        """Check if content has a copyright header."""
        pattern = self.COPYRIGHT_PATTERNS[file_type]["regex"]
        return bool(re.search(pattern, content))

    def extract_description(self, content: str, file_type: str) -> str:
        """Extract a description from the file for the copyright header."""
        lines = content.split("\n")

        if file_type == "python":
            # Look for existing docstring or create from filename
            for i, line in enumerate(lines):
                if line.strip().startswith('"""') and "Copyright" not in line:
                    # Find the end of the docstring
                    for j in range(i + 1, len(lines)):
                        if '"""' in lines[j]:
                            # Extract the description part
                            desc_lines = lines[i + 1 : j]
                            desc_lines = [
                                line.strip() for line in desc_lines if line.strip()
                            ]
                            if desc_lines and not any(
                                "Copyright" in line for line in desc_lines
                            ):
                                return "\n".join(desc_lines)
                            break
            return "Python module"

        elif file_type == "html":
            # Look for title or create generic description
            title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
            if title_match:
                return title_match.group(1).strip()
            return "HTML document"

        elif file_type == "yaml":
            # Look for existing comments or create from content
            if "quiz:" in content:
                return "QMS Training Quiz"
            return "Configuration file"

        return "Source file"

    def add_copyright_header(
        self, file_path: Path, content: str, file_type: str
    ) -> str:
        """Add copyright header to file content."""
        config = self.COPYRIGHT_PATTERNS[file_type]
        description = self.extract_description(content, file_type)

        if file_type == "python":
            lines = content.split("\n")
            # Check if file starts with shebang
            if lines and lines[0].startswith("#!"):
                # Use shebang format
                copyright_header = config["shebang_format"].format(
                    description=description, year=self.year
                )
                # Replace the first line and any existing docstring
                new_content = copyright_header + "\n\n"
                # Skip shebang and any existing docstring
                skip_lines = 1
                in_docstring = False
                for i in range(1, len(lines)):
                    line = lines[i].strip()
                    if line.startswith('"""'):
                        if not in_docstring:
                            in_docstring = True
                            continue
                        else:
                            skip_lines = i + 1
                            break
                    elif in_docstring and '"""' in line:
                        skip_lines = i + 1
                        break
                    elif not in_docstring and line:
                        break

                # Add remaining content
                remaining_lines = lines[skip_lines:]
                if remaining_lines and remaining_lines[0].strip():
                    new_content += "\n".join(remaining_lines)
                else:
                    # Skip empty lines at the beginning
                    while remaining_lines and not remaining_lines[0].strip():
                        remaining_lines.pop(0)
                    if remaining_lines:
                        new_content += "\n".join(remaining_lines)

                return new_content
            else:
                # Regular Python file without shebang
                copyright_header = config["copyright_format"].format(
                    description=description, year=self.year
                )
                return copyright_header + "\n\n" + content

        elif file_type == "html":
            # Insert after DOCTYPE if present, otherwise at the beginning
            lines = content.split("\n")
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().lower().startswith("<!doctype"):
                    insert_pos = i + 1
                    break

            copyright_header = config["copyright_format"].format(
                description=description, year=self.year
            )

            lines.insert(insert_pos, copyright_header)
            return "\n".join(lines)

        elif file_type == "yaml":
            copyright_header = config["copyright_format"].format(
                description=description, year=self.year
            )
            return copyright_header + "\n\n" + content

        return content

    def check_file(self, file_path: Path) -> bool:
        """Check a single file for copyright header.

        Returns:
            True if file has proper copyright header or was fixed
            False if file is missing copyright header and not in fix mode
        """
        file_type = self.get_file_type(file_path)
        if not file_type:
            return True  # Skip unknown file types

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return False

        if self.has_copyright(content, file_type):
            return True

        if self.fix_mode:
            # Add copyright header
            new_content = self.add_copyright_header(file_path, content, file_type)
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ Added copyright header to {file_path}")
                return True
            except Exception as e:
                self.errors.append(f"Error writing {file_path}: {e}")
                return False
        else:
            self.errors.append(f"Missing copyright header: {file_path}")
            return False

    def check_files(self, file_paths: List[Path]) -> bool:
        """Check multiple files for copyright headers.

        Returns:
            True if all files have proper copyright headers
            False if any files are missing copyright headers
        """
        all_good = True
        for file_path in file_paths:
            if not self.check_file(file_path):
                all_good = False

        return all_good


def main():
    """Main entry point for the copyright checker."""
    parser = argparse.ArgumentParser(
        description="Check and enforce copyright headers in source files"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to check (if none provided, checks all source files)",
    )
    parser.add_argument(
        "--fix", action="store_true", help="Automatically add missing copyright headers"
    )
    parser.add_argument(
        "--year", type=int, help="Copyright year to use (defaults to current year)"
    )

    args = parser.parse_args()

    # Get files to check
    if args.files:
        file_paths = [Path(f) for f in args.files if Path(f).exists()]
    else:
        # Find all source files in the project
        project_root = Path(__file__).parent.parent
        file_paths = []
        for pattern in ["**/*.py", "**/*.html", "**/*.yml", "**/*.yaml"]:
            file_paths.extend(project_root.glob(pattern))

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
            ".coverage",
        ]

        file_paths = [
            f
            for f in file_paths
            if not any(exclude in str(f) for exclude in exclude_patterns)
        ]

    if not file_paths:
        print("No files to check")
        return 0

    # Check files
    checker = CopyrightChecker(fix_mode=args.fix, year=args.year)
    success = checker.check_files(file_paths)

    # Report results
    if checker.errors:
        for error in checker.errors:
            print(f"❌ {error}")

    if success:
        print(f"✅ All {len(file_paths)} files have proper copyright headers")
        return 0
    else:
        print(
            f"\n❌ Found {len(checker.errors)} files with missing or incorrect copyright headers"
        )
        if not args.fix:
            print("Run with --fix to automatically add copyright headers")
        return 1


if __name__ == "__main__":
    sys.exit(main())
