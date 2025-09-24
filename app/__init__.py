# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Pocket DHF - A lightweight Device History File management system."""

from flask import Flask

from app.routes import main


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'dev-key-change-in-production'
    app.config['DEBUG'] = True

    # Register blueprints
    app.register_blueprint(main)

    return app
