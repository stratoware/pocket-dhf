# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Pocket DHF - A lightweight Device History File management system."""

import atexit
import os

from flask import Flask

from app.file_watcher import FileWatcher
from app.routes import main, set_file_watcher


def create_app(data_file_path: str = None, reports_dir: str = None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config[
        "SECRET_KEY"
    ] = "dev-key-change-in-production"  # pragma: allowlist secret
    app.config["DEBUG"] = True

    # Store data file path in app config for access by routes
    if data_file_path is None:
        data_file_path = os.getenv("DHF_DATA_FILE")

    app.config["DHF_DATA_FILE"] = data_file_path

    # Set up reports directory path
    if reports_dir is None:
        reports_dir = os.getenv("DHF_REPORTS_DIR")
    if not reports_dir:
        reports_dir = "sample-data/report-templates"
    app.config["DHF_REPORTS_DIR"] = reports_dir

    # Register blueprints
    app.register_blueprint(main)

    # Initialize file watcher if we have a data file
    if data_file_path and os.path.exists(data_file_path):
        watcher = FileWatcher(data_file_path)
        watcher.start()
        set_file_watcher(watcher)

        # Ensure watcher stops on app shutdown
        atexit.register(watcher.stop)
        print(f"File watcher enabled for: {data_file_path}")

    return app
