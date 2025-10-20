# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Unit tests for report generation functionality."""

from unittest.mock import MagicMock, mock_open, patch

import pytest

from app.routes import (
    generate_hardware_specifications_tables,
    generate_performance_summary,
    generate_product_requirements_tables,
    generate_report_content,
    generate_software_specifications_tables,
    generate_traceability_matrix,
    generate_user_needs_table,
    get_report_templates,
    process_auto_content,
)


class TestReportGeneration:
    """Test cases for report generation functionality."""

    @pytest.mark.unit
    def test_get_report_templates_success(self, app):
        """Test getting report templates successfully."""
        with app.app_context():
            with patch("os.path.exists", return_value=True), patch(
                "os.listdir",
                return_value=["specifications.md", "requirements_and_needs.md"],
            ), patch(
                "builtins.open",
                mock_open(read_data="# Test Report\n## Purpose\nTest purpose"),
            ):
                templates = get_report_templates()
                assert len(templates) == 2
                assert templates[0]["name"] == "specifications"
                assert templates[0]["title"] == "Test Report"
                # The actual implementation uses 'Report template' as default description
                assert templates[0]["description"] == "Report template"

    @pytest.mark.unit
    def test_get_report_templates_no_directory(self, app):
        """Test getting report templates when directory doesn't exist."""
        with app.app_context():
            with patch("os.path.exists", return_value=False):
                templates = get_report_templates()
                assert templates == []

    @pytest.mark.unit
    def test_generate_report_content_success(self, app, sample_dhf_data):
        """Test generating report content successfully."""
        with app.app_context():
            with patch("os.path.exists", return_value=True), patch(
                "builtins.open",
                mock_open(
                    read_data="# {{project_name}}\n## Purpose\nTest purpose\n<!-- AUTO_CONTENT: user_needs_table -->"
                ),
            ):
                with patch("app.routes.get_data_manager") as mock_get_data_manager:
                    mock_data_manager = MagicMock()
                    mock_data_manager.load_data.return_value = sample_dhf_data
                    mock_get_data_manager.return_value = mock_data_manager
                    content = generate_report_content("test_report")
                    assert content is not None
                    assert "Test Diabetes Monitor" in content["content"]
                    assert "Accurate Glucose Monitoring" in content["content"]

    @pytest.mark.unit
    def test_generate_report_content_file_not_found(self, app):
        """Test generating report content when file doesn't exist."""
        with app.app_context():
            with patch("os.path.exists", return_value=False):
                content = generate_report_content("nonexistent")
                assert content is None

    @pytest.mark.unit
    def test_process_auto_content_user_needs_table(self, sample_dhf_data):
        """Test processing auto content for user needs table."""
        content = "Test content <!-- AUTO_CONTENT: user_needs_table --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "UN001" in result
        assert "Accurate Glucose Monitoring" in result

    @pytest.mark.unit
    def test_process_auto_content_product_requirements_tables(self, sample_dhf_data):
        """Test processing auto content for product requirements tables."""
        content = "Test content <!-- AUTO_CONTENT: product_requirements_tables --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "PR001" in result
        assert "Glucose Measurement Accuracy" in result

    @pytest.mark.unit
    def test_process_auto_content_software_specifications_tables(self, sample_dhf_data):
        """Test processing auto content for software specifications tables."""
        content = "Test content <!-- AUTO_CONTENT: software_specifications_tables --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "SS001" in result
        assert "Glucose Algorithm" in result

    @pytest.mark.unit
    def test_process_auto_content_hardware_specifications_tables(self, sample_dhf_data):
        """Test processing auto content for hardware specifications tables."""
        content = "Test content <!-- AUTO_CONTENT: hardware_specifications_tables --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "HS001" in result
        assert "Glucose Sensor" in result

    @pytest.mark.unit
    def test_process_auto_content_traceability_matrix(self, sample_dhf_data):
        """Test processing auto content for traceability matrix."""
        content = "Test content <!-- AUTO_CONTENT: traceability_matrix --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "User Need" in result
        assert "Product Requirements" in result

    @pytest.mark.unit
    def test_process_auto_content_performance_summary(self, sample_dhf_data):
        """Test processing auto content for performance summary."""
        content = "Test content <!-- AUTO_CONTENT: performance_summary --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "Performance requirements" in result

    @pytest.mark.unit
    def test_process_auto_content_unknown_type(self, sample_dhf_data):
        """Test processing auto content for unknown type."""
        content = "Test content <!-- AUTO_CONTENT: unknown_type --> more content"
        result = process_auto_content(content, sample_dhf_data)

        assert "Test content" in result
        assert "more content" in result
        assert "[unknown_type content would be generated here]" in result

    @pytest.mark.unit
    def test_generate_user_needs_table(self, sample_dhf_data):
        """Test generating user needs table."""
        table = generate_user_needs_table(sample_dhf_data)

        assert "| ID | Title | Description |" in table
        assert "UN001" in table
        assert "Accurate Glucose Monitoring" in table
        assert "UN002" in table
        assert "Real-time Alerts" in table

    @pytest.mark.unit
    def test_generate_user_needs_table_empty(self):
        """Test generating user needs table with empty data."""
        table = generate_user_needs_table({})
        assert "*No user needs defined.*" in table

    @pytest.mark.unit
    def test_generate_product_requirements_tables(self, sample_dhf_data):
        """Test generating product requirements tables."""
        tables = generate_product_requirements_tables(sample_dhf_data)

        assert "### Functional Requirements" in tables
        assert "| ID | Title | Description | Linked User Needs |" in tables
        assert "PR001" in tables
        assert "Glucose Measurement Accuracy" in tables
        assert "UN001" in tables

    @pytest.mark.unit
    def test_generate_product_requirements_tables_empty(self):
        """Test generating product requirements tables with empty data."""
        tables = generate_product_requirements_tables({})
        assert "*No product requirements defined.*" in tables

    @pytest.mark.unit
    def test_generate_software_specifications_tables(self, sample_dhf_data):
        """Test generating software specifications tables."""
        tables = generate_software_specifications_tables(sample_dhf_data)

        assert "### Measurement" in tables
        assert "| ID | Title | Description | Linked Requirements |" in tables
        assert "SS001" in tables
        assert "Glucose Algorithm" in tables
        assert "PR001" in tables

    @pytest.mark.unit
    def test_generate_software_specifications_tables_empty(self):
        """Test generating software specifications tables with empty data."""
        tables = generate_software_specifications_tables({})
        assert "*No software specifications defined.*" in tables

    @pytest.mark.unit
    def test_generate_hardware_specifications_tables(self, sample_dhf_data):
        """Test generating hardware specifications tables."""
        tables = generate_hardware_specifications_tables(sample_dhf_data)

        assert "### Sensor" in tables
        assert "| ID | Title | Description | Linked Requirements |" in tables
        assert "HS001" in tables
        assert "Glucose Sensor" in tables
        assert "PR001" in tables

    @pytest.mark.unit
    def test_generate_hardware_specifications_tables_empty(self):
        """Test generating hardware specifications tables with empty data."""
        tables = generate_hardware_specifications_tables({})
        assert "*No hardware specifications defined.*" in tables

    @pytest.mark.unit
    def test_generate_traceability_matrix(self, sample_dhf_data):
        """Test generating traceability matrix."""
        matrix = generate_traceability_matrix(sample_dhf_data)

        assert (
            "| User Need | Product Requirements | Software Specs | Hardware Specs |"
            in matrix
        )
        assert "Accurate Glucose Monitoring" in matrix
        assert "PR001" in matrix

    @pytest.mark.unit
    def test_generate_performance_summary(self, sample_dhf_data):
        """Test generating performance summary."""
        summary = generate_performance_summary(sample_dhf_data)

        assert "Performance requirements" in summary
        assert "tabular format" in summary

    @pytest.mark.unit
    def test_generate_report_content_with_template_variables(
        self, app, sample_dhf_data
    ):
        """Test generating report content with template variables."""
        template_content = """
        # {{project_name}}
        Device Type: {{device_type}}
        Version: {{version}}
        Generated: {{generation_date}}
        Next Review: {{next_review_date}}
        """

        with app.app_context():
            with patch("os.path.exists", return_value=True), patch(
                "builtins.open", mock_open(read_data=template_content)
            ):
                with patch("app.routes.get_data_manager") as mock_get_data_manager:
                    mock_data_manager = MagicMock()
                    mock_data_manager.load_data.return_value = sample_dhf_data
                    mock_get_data_manager.return_value = mock_data_manager
                    content = generate_report_content("test_report")
                    assert content is not None
                    assert "Test Diabetes Monitor" in content["content"]
                    assert "Continuous Glucose Monitor" in content["content"]
                    assert "1.0.0" in content["content"]
                    assert "Generated:" in content["content"]
                    assert "Next Review:" in content["content"]
