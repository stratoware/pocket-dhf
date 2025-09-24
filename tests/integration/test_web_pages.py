# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Integration tests for web pages."""

from unittest.mock import patch

import pytest


class TestWebPages:
    """Test cases for web pages."""

    @pytest.mark.ui
    def test_index_page(self, client, data_manager):
        """Test index page loads successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Pocket DHF" in response.data
        # Check for any project name in the response
        assert b"Monitor" in response.data or b"Project" in response.data

    @pytest.mark.ui
    def test_browse_page(self, client, data_manager):
        """Test browse page loads successfully."""
        response = client.get("/browse")
        assert response.status_code == 200
        assert b"Browse DHF Data" in response.data
        assert b"DHF Navigation" in response.data

    @pytest.mark.ui
    def test_configuration_page(self, client, data_manager):
        """Test configuration page loads successfully."""
        response = client.get("/configuration")
        assert response.status_code == 200
        assert b"Configuration" in response.data
        assert b"Severity Options" in response.data

    @pytest.mark.ui
    def test_reports_page(self, client, data_manager):
        """Test reports page loads successfully."""
        response = client.get("/reports")
        assert response.status_code == 200
        assert b"Reports" in response.data
        assert b"Report Templates" in response.data

    @pytest.mark.ui
    def test_index_page_with_error(self, client):
        """Test index page handles data loading errors gracefully."""
        with patch(
            "app.routes.data_manager.load_data", side_effect=Exception("Test error")
        ):
            response = client.get("/")
            assert response.status_code == 200
            # Check for error message or fallback content
            assert b"Error" in response.data or b"Unknown" in response.data

    @pytest.mark.ui
    def test_browse_page_with_error(self, client):
        """Test browse page handles data loading errors gracefully."""
        with patch(
            "app.routes.data_manager.load_data", side_effect=Exception("Test error")
        ):
            response = client.get("/browse")
            assert response.status_code == 302  # Redirect to index

    @pytest.mark.ui
    def test_configuration_page_with_error(self, client):
        """Test configuration page handles data loading errors gracefully."""
        with patch(
            "app.routes.data_manager.get_configuration",
            side_effect=Exception("Test error"),
        ):
            response = client.get("/configuration")
            assert response.status_code == 302  # Redirect to index

    @pytest.mark.ui
    def test_reports_page_with_error(self, client):
        """Test reports page handles data loading errors gracefully."""
        with patch(
            "app.routes.get_report_templates", side_effect=Exception("Test error")
        ):
            response = client.get("/reports")
            assert response.status_code == 302  # Redirect to index

    @pytest.mark.ui
    def test_static_files(self, client):
        """Test static files are served correctly."""
        response = client.get("/static/css/style.css")
        assert response.status_code == 200
        assert response.content_type == "text/css; charset=utf-8"

    @pytest.mark.ui
    def test_favicon(self, client):
        """Test favicon is handled (should return 404 if not present)."""
        response = client.get("/favicon.ico")
        # This might return 404 if no favicon is present, which is fine
        assert response.status_code in [200, 404]

    @pytest.mark.ui
    def test_nonexistent_page(self, client):
        """Test non-existent page returns 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    @pytest.mark.ui
    def test_browse_page_with_item_id_param(self, client, data_manager):
        """Test browse page with item ID parameter."""
        response = client.get("/browse?item_id=UN001")
        assert response.status_code == 200
        assert b"Browse DHF Data" in response.data

    @pytest.mark.ui
    def test_reports_page_generate_specifications(self, client, data_manager):
        """Test generating specifications report."""
        response = client.get("/api/report/specifications")
        assert response.status_code == 200

        data = response.get_json()
        assert "title" in data
        assert "content" in data
        # Check for any project name in the content
        assert "Monitor" in data["content"] or "Project" in data["content"]

    @pytest.mark.ui
    def test_reports_page_generate_requirements_and_needs(self, client, data_manager):
        """Test generating requirements and needs report."""
        response = client.get("/api/report/requirements_and_needs")
        assert response.status_code == 200

        data = response.get_json()
        assert "title" in data
        assert "content" in data
        # Check for any project name in the content
        assert "Monitor" in data["content"] or "Project" in data["content"]

    @pytest.mark.ui
    def test_browse_page_displays_counts(self, client, data_manager):
        """Test browse page displays correct item counts."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check that counts are displayed in the HTML
        assert b"User Needs" in response.data
        assert b"Risks" in response.data
        assert b"Product Requirements" in response.data
        assert b"Software Specifications" in response.data
        assert b"Hardware Specifications" in response.data

    @pytest.mark.ui
    def test_configuration_page_displays_options(self, client, data_manager):
        """Test configuration page displays configuration options."""
        response = client.get("/configuration")
        assert response.status_code == 200

        # Check that configuration options are displayed
        assert b"Severity" in response.data or b"Options" in response.data

    @pytest.mark.ui
    def test_reports_page_displays_templates(self, client, data_manager):
        """Test reports page displays available templates."""
        response = client.get("/reports")
        assert response.status_code == 200

        # Check that report templates are displayed
        assert b"Report Templates" in response.data
        assert b"specifications" in response.data
        assert b"requirements_and_needs" in response.data
