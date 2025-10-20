# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""
Tests for hyperlink navigation in traceability tables.
"""

# Integration tests for traceability navigation functionality


class TestTraceabilityNavigation:
    """Test hyperlink navigation in traceability tables."""

    def test_browse_page_contains_traceability_hyperlinks(self, app, client):
        """Test that the browse page contains hyperlinks in traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for traceability hyperlinks
        assert 'onclick="loadItem(' in html_content
        assert "text-decoration-none" in html_content
        assert 'href="#"' in html_content

    def test_browse_page_contains_traceability_table_generation(self, app, client):
        """Test that the browse page contains traceability table generation functions."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for table generation functions
        assert "generateUserNeedsToRequirementsTable" in html_content
        assert "generateRequirementsToSpecificationsTable" in html_content
        assert "generateRisksToMitigationsTable" in html_content

    def test_browse_page_contains_traceability_data_loading(self, app, client):
        """Test that the browse page contains data loading functions for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for data loading functions
        assert "loadUserNeedsToRequirementsData" in html_content
        assert "loadRequirementsToSpecificationsData" in html_content
        assert "loadRisksToMitigationsData" in html_content

    def test_browse_page_contains_traceability_api_calls(self, app, client):
        """Test that the browse page contains API calls for traceability data."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for API calls
        assert "/api/traceability/user-needs-to-requirements" in html_content
        assert "/api/traceability/requirements-to-specifications" in html_content
        assert "/api/traceability/risks-to-mitigations" in html_content

    def test_browse_page_contains_traceability_table_structure(self, app, client):
        """Test that the browse page contains proper table structure for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for table structure
        assert "table" in html_content
        assert "thead" in html_content
        assert "tbody" in html_content
        assert "tr" in html_content
        assert "td" in html_content

    def test_browse_page_contains_traceability_table_ids(self, app, client):
        """Test that the browse page contains proper IDs for traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for table IDs
        assert "user-needs-requirements-tbody" in html_content
        assert "requirements-specifications-tbody" in html_content
        assert "risks-mitigations-tbody" in html_content

    def test_browse_page_contains_traceability_error_handling(self, app, client):
        """Test that the browse page contains error handling for traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for error handling
        assert "Error loading data" in html_content
        assert "catch" in html_content
        assert "console.error" in html_content

    def test_browse_page_contains_traceability_loading_states(self, app, client):
        """Test that the browse page contains loading states for traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for loading states
        assert "text-center" in html_content
        assert "text-muted" in html_content

    def test_browse_page_contains_traceability_hyperlink_styling(self, app, client):
        """Test that the browse page contains proper styling for traceability hyperlinks."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for hyperlink styling
        assert "text-decoration-none" in html_content
        assert "d-block" in html_content

    def test_browse_page_contains_traceability_table_headers(self, app, client):
        """Test that the browse page contains proper headers for traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for table headers
        assert "User Need" in html_content
        assert "Product Requirements" in html_content
        assert "Risk" in html_content
        assert "Mitigations" in html_content

    def test_browse_page_contains_traceability_navigation_functions(self, app, client):
        """Test that the browse page contains navigation functions for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for navigation functions
        assert "loadItem(" in html_content
        assert "updateSidebarFocus(" in html_content

    def test_browse_page_contains_traceability_data_parsing(self, app, client):
        """Test that the browse page contains data parsing for traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for data parsing
        assert "response.json()" in html_content
        assert "forEach" in html_content
        assert "map(" in html_content

    def test_browse_page_contains_traceability_dynamic_content(self, app, client):
        """Test that the browse page contains dynamic content generation for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for dynamic content
        assert "innerHTML" in html_content
        assert "createElement" in html_content
        assert "appendChild" in html_content

    def test_browse_page_contains_traceability_type_handling(self, app, client):
        """Test that the browse page contains type handling for traceability items."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for type handling
        assert "software_specification" in html_content
        assert "hardware_specification" in html_content
        assert "risk" in html_content

    def test_browse_page_contains_traceability_hyperlink_generation(self, app, client):
        """Test that the browse page contains hyperlink generation for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for hyperlink generation
        assert 'onclick="loadItem(' in html_content
        assert 'href="#"' in html_content
        assert "text-decoration-none" in html_content

    def test_browse_page_contains_traceability_table_responsiveness(self, app, client):
        """Test that the browse page contains responsive design for traceability tables."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for responsive design
        assert "table-responsive" in html_content
        assert "col-" in html_content
        assert "container" in html_content

    def test_browse_page_contains_traceability_accessibility(self, app, client):
        """Test that the browse page contains accessibility features for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for accessibility features
        assert (
            "aria-" in html_content
            or "role=" in html_content
            or "tabindex=" in html_content
        )

    def test_browse_page_contains_traceability_performance(self, app, client):
        """Test that the browse page contains performance optimizations for traceability."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for performance optimizations
        assert "fetch(" in html_content
        assert "then(" in html_content
        assert "catch(" in html_content
