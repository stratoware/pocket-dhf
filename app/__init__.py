# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Pocket DHF - A lightweight Device History File management system."""

import atexit
import os

from flask import Flask

from app.file_watcher import FileWatcher
from app.routes import main, set_file_watcher


def create_app(data_dir: str = None):
    """Create and configure the Flask application.
    
    Args:
        data_dir: Path to the data directory containing:
                  - dhf_data.yaml (DHF data file)
                  - analyses/ (FMEA and FTA files)
                  - report-templates/ (markdown report templates)
                  Defaults to "sample-data"
    """
    app = Flask(__name__)

    # Configuration
    app.config[
        "SECRET_KEY"
    ] = "dev-key-change-in-production"  # pragma: allowlist secret
    app.config["DEBUG"] = True

    # Determine data directory
    if data_dir is None:
        data_dir = os.getenv("DHF_DATA_DIR", "sample-data")
    
    # Construct paths from data directory
    # Look for dhf_data.yaml or any .dhf file
    data_file_path = None
    if data_dir:
        default_path = os.path.join(data_dir, "dhf_data.yaml")
        if os.path.exists(default_path):
            data_file_path = default_path
        else:
            # Look for any .dhf file
            import glob
            dhf_files = glob.glob(os.path.join(data_dir, "*.dhf"))
            if dhf_files:
                data_file_path = dhf_files[0]  # Use first .dhf file found
    
    reports_dir = os.path.join(data_dir, "report-templates") if data_dir else None
    analyses_dir = os.path.join(data_dir, "analyses") if data_dir else None

    app.config["DHF_DATA_FILE"] = data_file_path
    app.config["DHF_REPORTS_DIR"] = reports_dir
    app.config["DHF_ANALYSES_DIR"] = analyses_dir

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
