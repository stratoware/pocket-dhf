# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Pocket DHF - A lightweight Device History File management system."""

import os
from flask import Flask

from app.routes import main


def create_app(data_file_path: str = None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = (
        "dev-key-change-in-production"  # pragma: allowlist secret
    )
    app.config["DEBUG"] = True

    # Store data file path in app config for access by routes
    if data_file_path is None:
        data_file_path = os.getenv("DHF_DATA_FILE")
    
    app.config["DHF_DATA_FILE"] = data_file_path

    # Register blueprints
    app.register_blueprint(main)

    return app
