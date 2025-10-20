# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Tests for traceability table UI functionality."""

import pytest


@pytest.mark.ui
class TestTraceabilityUI:
    """Test traceability table UI functionality."""

    def test_browse_page_contains_traceability_section(self, client, data_manager):
        """Test that browse page contains traceability tables section."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for traceability section in HTML
        assert b"Traceability Tables" in response.data
        assert b"User Needs to Product Requirements" in response.data
        assert b"Product Requirements to Specifications" in response.data
        assert b"Risks to Mitigations" in response.data

    def test_traceability_section_collapsible(self, client, data_manager):
        """Test that traceability section is collapsible."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for collapsible elements
        assert b'data-target="traceabilityItems"' in response.data
        assert b"collapsible-header" in response.data
        assert b"collapsible-content" in response.data

    def test_traceability_table_click_handlers(self, client, data_manager):
        """Test that traceability table items have click handlers."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for data attributes for click handling
        assert b'data-traceability-type="user-needs-to-requirements"' in response.data
        assert (
            b'data-traceability-type="requirements-to-specifications"' in response.data
        )
        assert b'data-traceability-type="risks-to-mitigations"' in response.data

    def test_traceability_content_panel(self, client, data_manager):
        """Test that traceability content panel exists."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for traceability content panel
        assert b'id="traceability-content"' in response.data
        assert b'id="traceability-title"' in response.data
        assert b'id="traceability-table-container"' in response.data

    def test_traceability_close_button(self, client, data_manager):
        """Test that traceability panel has close button."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for close button
        assert b'onclick="hideTraceabilityTable()"' in response.data
        assert b"Close" in response.data

    def test_traceability_javascript_functions(self, client, data_manager):
        """Test that traceability JavaScript functions are present."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for JavaScript functions
        assert b"function showTraceabilityTable(" in response.data
        assert b"function hideTraceabilityTable(" in response.data
        assert b"function generateUserNeedsToRequirementsTable(" in response.data
        assert b"function generateRequirementsToSpecificationsTable(" in response.data
        assert b"function generateRisksToMitigationsTable(" in response.data

    def test_traceability_api_calls(self, client, data_manager):
        """Test that traceability JavaScript makes API calls."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for API endpoint calls
        assert b"/api/traceability/user-needs-to-requirements" in response.data
        assert b"/api/traceability/requirements-to-specifications" in response.data
        assert b"/api/traceability/risks-to-mitigations" in response.data

    def test_traceability_table_styling(self, client, data_manager):
        """Test that traceability tables have proper styling."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for table styling classes
        assert b"table-responsive" in response.data
        assert b"table table-bordered table-hover" in response.data
        assert b"table-dark" in response.data

    def test_traceability_hyperlinks(self, client, data_manager):
        """Test that traceability tables have hyperlinks for navigation."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for hyperlink functionality
        assert b'onclick="loadItem(' in response.data
        assert b"text-decoration-none" in response.data

    def test_traceability_error_handling(self, client, data_manager):
        """Test that traceability tables handle errors gracefully."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for error handling in JavaScript
        assert b"Error loading data" in response.data
        assert b"console.error" in response.data

    def test_traceability_responsive_design(self, client, data_manager):
        """Test that traceability tables are responsive."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for responsive design elements (updated for new layout)
        assert b"table-responsive" in response.data
        assert b"container" in response.data

    def test_traceability_icon_usage(self, client, data_manager):
        """Test that traceability section uses appropriate icons."""
        response = client.get("/browse")
        assert response.status_code == 200

        # Check for icons
        assert b"fas fa-project-diagram" in response.data
        assert b"fas fa-link" in response.data
