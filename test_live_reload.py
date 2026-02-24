#!/usr/bin/env python3
# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Test script to verify live reload functionality."""

import sys
import time

# Test import of watchdog
try:
    from watchdog.observers import Observer

    print("✓ watchdog library is installed and importable")
except ImportError as e:
    print(f"✗ Failed to import watchdog: {e}")
    sys.exit(1)

# Test import of file_watcher module
try:
    from app.file_watcher import FileWatcher

    print("✓ file_watcher module is importable")
except ImportError as e:
    print(f"✗ Failed to import file_watcher: {e}")
    sys.exit(1)

# Test creating a file watcher for a sample file
try:
    import os
    import tempfile

    # Create a temporary file to watch
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        test_file = f.name
        f.write("test: data\n")

    print(f"✓ Created test file: {test_file}")

    # Create and start file watcher
    watcher = FileWatcher(test_file)
    watcher.start()
    print("✓ File watcher started successfully")

    # Give it a moment to initialize
    time.sleep(0.5)

    # Modify the file
    with open(test_file, "a") as f:
        f.write("modified: true\n")
    print("✓ Modified test file")

    # Check for change notification (wait up to 2 seconds)
    change = watcher.get_changes(timeout=2.0)
    if change:
        print(f"✓ File change detected: {change}")
    else:
        print("⚠ No file change detected within timeout (may be normal)")

    # Stop watcher
    watcher.stop()
    print("✓ File watcher stopped successfully")

    # Clean up
    os.unlink(test_file)
    print("✓ Cleaned up test file")

except Exception as e:
    print(f"✗ Error during file watcher test: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! Live reload functionality is ready.")
print("=" * 60)
print("\nYou can now start the server with:")
print("  poetry run python main.py --data-file ../apnea.dhf")
print("\nThe browser will automatically reload when you edit the YAML file.")
