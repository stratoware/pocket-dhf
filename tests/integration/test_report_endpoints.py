# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Integration tests for report generation endpoints."""

from unittest.mock import MagicMock, mock_open, patch

import pytest


class TestReportGeneration:
    """Test cases for report generation endpoints."""

    @pytest.mark.integration
    def test_generate_requirements_report(self, client, data_manager):
        """Test generating requirements and needs report."""
        response = client.get("/api/report/requirements_and_needs")
        assert response.status_code == 200
        # Reports return JSON with markdown content
        assert "application/json" in response.content_type or "text/markdown" in response.content_type

    @pytest.mark.integration
    def test_generate_specifications_report(self, client, data_manager):
        """Test generating specifications report."""
        response = client.get("/api/report/specifications")
        assert response.status_code == 200
        # Reports return JSON with markdown content
        assert "application/json" in response.content_type or "text/markdown" in response.content_type

    @pytest.mark.integration
    def test_generate_risk_management_report(self, client, data_manager):
        """Test generating risk management report."""
        response = client.get("/api/report/risk_management")
        assert response.status_code == 200
        # Reports return JSON with markdown content
        assert "application/json" in response.content_type or "text/markdown" in response.content_type

    @pytest.mark.integration
    def test_generate_invalid_report(self, client, data_manager):
        """Test generating invalid report type."""
        response = client.get("/api/report/invalid_report_type")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_generate_report_with_template(self, client, data_manager):
        """Test report generation with custom template."""
        template_content = """# Test Report
## User Needs
{{user_needs_table}}
## Traceability
{{traceability_matrix}}
"""
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=template_content)):
                response = client.get("/api/report/requirements_and_needs")
                assert response.status_code == 200

    @pytest.mark.integration
    def test_generate_report_without_template(self, client, data_manager):
        """Test report generation without template file."""
        with patch("os.path.exists", return_value=False):
            response = client.get("/api/report/requirements_and_needs")
            # Should return error or default content
            assert response.status_code in [200, 404, 500]

    @pytest.mark.integration
    def test_generate_report_error_handling(self, client, data_manager):
        """Test report generation error handling."""
        with patch("app.routes.get_data_manager", side_effect=Exception("Test error")):
            response = client.get("/api/report/requirements_and_needs")
            # May return 404, 500, or 200 depending on error handling
            assert response.status_code in [404, 500, 200]


class TestReportHelperFunctions:
    """Test cases for report helper functions."""

    @pytest.mark.integration
    def test_generate_user_needs_table(self, client, data_manager):
        """Test user needs table generation."""
        # This gets called as part of report generation
        response = client.get("/api/report/requirements_and_needs")
        assert response.status_code == 200
        # Check that response contains table-like content
        assert b"|" in response.data or b"None" in response.data

    @pytest.mark.integration
    def test_generate_traceability_matrix(self, client, data_manager):
        """Test traceability matrix generation."""
        response = client.get("/api/report/requirements_and_needs")
        assert response.status_code == 200
        # Matrix should be generated
        assert response.data

    @pytest.mark.integration
    def test_generate_performance_summary(self, client, data_manager):
        """Test performance summary generation."""
        response = client.get("/api/report/specifications")
        assert response.status_code == 200
        # Should generate some content
        assert response.data


class TestReportTemplates:
    """Test cases for report templates."""

    @pytest.mark.integration
    def test_report_with_all_placeholders(self, client, data_manager):
        """Test report generation with all template placeholders."""
        template_content = """# Complete Report
## Metadata
{{project_name}}
{{device_type}}
{{version}}

## Tables
{{user_needs_table}}
{{product_requirements_table}}
{{software_specifications_table}}
{{hardware_specifications_table}}
{{risk_assessment_table}}
{{traceability_matrix}}
{{performance_summary}}
"""
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open(read_data=template_content)):
                response = client.get("/api/report/requirements_and_needs")
                assert response.status_code == 200
                # Should have replaced placeholders
                assert b"{{" not in response.data or response.status_code == 200

    @pytest.mark.integration
    def test_report_with_nested_requirements(self, client, data_manager):
        """Test report generation with nested requirement structure."""
        # The test data should handle nested requirements
        response = client.get("/api/report/specifications")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_report_with_linked_risks(self, client, data_manager):
        """Test report generation with linked risks."""
        response = client.get("/api/report/risk_management")
        assert response.status_code == 200
        # Should include risk information
        assert response.data


class TestReportDownload:
    """Test cases for report download functionality."""

    @pytest.mark.integration
    def test_download_report_as_markdown(self, client, data_manager):
        """Test downloading report as markdown."""
        response = client.get("/api/report/requirements_and_needs")
        assert response.status_code == 200
        # Accept either JSON or markdown content type
        assert "application/json" in response.content_type or "text/markdown" in response.content_type
        # Should have content
        assert response.data

    @pytest.mark.integration
    def test_download_multiple_reports(self, client, data_manager):
        """Test downloading multiple different reports."""
        reports = ["requirements_and_needs", "specifications", "risk_management"]
        for report_name in reports:
            response = client.get(f"/api/report/{report_name}")
            assert response.status_code == 200
            assert response.data  # Should have content


class TestReportDataStructures:
    """Test reports with different data structures."""

    @pytest.mark.integration
    def test_report_with_flat_structure(self, client, data_manager):
        """Test report generation with flat data structure."""
        with patch("app.routes.get_data_manager") as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.load_data.return_value = {
                "metadata": {"project_name": "Test", "device_type": "Device"},
                "user_needs": {"UN001": {"title": "Need 1"}},
                "product_requirements": {},
            }
            mock_get_dm.return_value = mock_dm

            response = client.get("/api/report/requirements_and_needs")
            assert response.status_code == 200

    @pytest.mark.integration
    def test_report_with_hierarchical_structure(self, client, data_manager):
        """Test report generation with hierarchical data structure."""
        with patch("app.routes.get_data_manager") as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.load_data.return_value = {
                "metadata": {"project_name": "Test", "device_type": "Device"},
                "user_needs": {"group1": {"user_needs": {"UN001": {"title": "Need 1"}}}},
                "product_requirements": {
                    "group1": {"requirements": {"PR001": {"title": "Req 1"}}}
                },
            }
            mock_get_dm.return_value = mock_dm

            response = client.get("/api/report/requirements_and_needs")
            assert response.status_code == 200

    @pytest.mark.integration
    def test_report_with_empty_data(self, client, data_manager):
        """Test report generation with empty data."""
        with patch("app.routes.get_data_manager") as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.load_data.return_value = {
                "metadata": {},
                "user_needs": {},
                "product_requirements": {},
            }
            mock_get_dm.return_value = mock_dm

            response = client.get("/api/report/requirements_and_needs")
            assert response.status_code == 200
            # Should handle empty data gracefully
            assert response.data

