# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Pocket DHF - A lightweight Device History File management system."""

import atexit
import os

from flask import Flask

from app.file_watcher import FileWatcher
from app.routes import main, set_file_watcher


def create_app(data_file_path: str = None, reports_dir: str = None, application_root: str = None):
    """Create and configure the Flask application.
    
    Args:
        data_file_path: Path to DHF data file
        reports_dir: Path to reports templates directory
        application_root: URL prefix where the app is mounted (e.g., '/dhf-api' or '/')
    """
    app = Flask(__name__)

    # Configuration
    app.config[
        "SECRET_KEY"
    ] = "dev-key-change-in-production"  # pragma: allowlist secret
    app.config["DEBUG"] = True

    # Set application root (URL prefix for when app is mounted under a subpath)
    if application_root is None:
        application_root = os.getenv("APPLICATION_ROOT", "")
    
    # Normalize: empty string for root mount, or path with leading slash and no trailing slash
    if application_root and application_root != "/":
        application_root = "/" + application_root.strip("/")
    else:
        application_root = ""
    
    # Store for use in templates and context
    app.config["APPLICATION_ROOT"] = application_root if application_root else "/"
    
    # Log the mount point for debugging
    mount_display = application_root if application_root else "/"
    print(f"Pocket DHF mounted at: {mount_display}")

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

    # Register blueprints without url_prefix
    # The APPLICATION_ROOT config tells Flask how to generate URLs (via url_for)
    # but the actual routing is handled at root level (nginx strips the prefix)
    app.register_blueprint(main)

    # Register error handlers and context processors
    register_error_handlers(app)

    # Initialize file watcher if we have a data file
    if data_file_path and os.path.exists(data_file_path):
        watcher = FileWatcher(data_file_path)
        watcher.start()
        set_file_watcher(watcher)

        # Ensure watcher stops on app shutdown
        atexit.register(watcher.stop)
        print(f"File watcher enabled for: {data_file_path}")

    return app


def register_error_handlers(app):
    """Register global error handlers and context processors."""
    from flask import render_template, request

    @app.context_processor
    def inject_integration_mode():
        """Make integration mode available to all templates."""
        header_value = request.headers.get('X-Integrated-Mode')
        is_integrated = header_value == 'true'
        
        # Debug logging
        app.logger.debug(f"Path: {request.path}, X-Integrated-Mode: {header_value}, is_integrated: {is_integrated}")
        
        # Get the application root prefix (e.g., "/dhf-api")
        app_root = app.config.get('APPLICATION_ROOT', '/')
        prefix = '' if app_root == '/' else app_root
        
        # Create a custom url_for that adds the prefix
        def url_for_with_prefix(endpoint, **values):
            from flask import url_for as flask_url_for
            url = flask_url_for(endpoint, **values)
            # Add prefix if we have one and URL is relative
            if prefix and url.startswith('/'):
                url = prefix + url
            return url
        
        return {
            'is_integrated': is_integrated,
            'url_for': url_for_with_prefix,  # Override url_for in templates
        }

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return render_template(
            'error.html',
            error_code=404,
            error_title="Page Not Found",
            error_message="The requested page could not be found.",
            show_home_link=True
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(f'Internal error: {error}')
        return render_template(
            'error.html',
            error_code=500,
            error_title="Internal Server Error",
            error_message="Pocket DHF encountered an unexpected error. Please try again or contact support if the problem persists.",
            show_home_link=True
        ), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Catch-all handler for unhandled exceptions."""
        app.logger.error(f'Unhandled exception: {error}', exc_info=True)

        # Return 500 error page
        return render_template(
            'error.html',
            error_code=500,
            error_title="Unexpected Error",
            error_message="Pocket DHF encountered an unexpected error. The issue has been logged.",
            show_home_link=True
        ), 500
