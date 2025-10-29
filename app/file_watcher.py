# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""File watcher for monitoring YAML data file changes."""

import os
import queue
import threading
import time
from typing import Optional

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class YAMLFileChangeHandler(FileSystemEventHandler):
    """Handler for YAML file change events."""

    def __init__(self, file_path: str, change_queue: queue.Queue):
        """Initialize the file change handler.

        Args:
            file_path: Path to the file to monitor
            change_queue: Queue to put change notifications
        """
        super().__init__()
        self.file_path = os.path.abspath(file_path)
        self.change_queue = change_queue
        self.last_modified = 0
        # Debounce time to avoid multiple events for single save
        self.debounce_seconds = 0.5

    def on_modified(self, event: FileSystemEvent) -> None:
        """Called when a file is modified."""
        if event.is_directory:
            return

        # Check if this is our target file
        event_path = os.path.abspath(event.src_path)
        if event_path == self.file_path:
            # Debounce: ignore events that happen too quickly
            current_time = time.time()
            if current_time - self.last_modified > self.debounce_seconds:
                self.last_modified = current_time
                print(f"Detected change in {self.file_path}")
                self.change_queue.put({"type": "file_changed", "path": self.file_path})


class FileWatcher:
    """Watches a file for changes and notifies subscribers."""

    def __init__(self, file_path: str):
        """Initialize the file watcher.

        Args:
            file_path: Path to the file to monitor
        """
        self.file_path = os.path.abspath(file_path)
        self.watch_dir = os.path.dirname(self.file_path)
        self.change_queue: queue.Queue = queue.Queue()
        self.observer: Optional[Observer] = None
        self.is_running = False
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start watching the file."""
        with self._lock:
            if self.is_running:
                return

            print(f"Starting file watcher for: {self.file_path}")
            event_handler = YAMLFileChangeHandler(self.file_path, self.change_queue)
            self.observer = Observer()
            self.observer.schedule(event_handler, self.watch_dir, recursive=False)
            self.observer.start()
            self.is_running = True

    def stop(self) -> None:
        """Stop watching the file."""
        with self._lock:
            if not self.is_running or self.observer is None:
                return

            print(f"Stopping file watcher for: {self.file_path}")
            self.observer.stop()
            self.observer.join(timeout=5)
            self.is_running = False

    def get_changes(self, timeout: Optional[float] = None) -> Optional[dict]:
        """Get the next change event from the queue.

        Args:
            timeout: Maximum time to wait for a change (None = wait forever)

        Returns:
            Change event dict or None if timeout
        """
        try:
            return self.change_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def has_changes(self) -> bool:
        """Check if there are any pending changes."""
        return not self.change_queue.empty()
