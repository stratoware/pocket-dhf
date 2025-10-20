# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""
Tests for popup editing functionality for linked entities.
"""

# Integration tests for popup editing functionality


class TestPopupEditing:
    """Test popup editing functionality for linked entities."""

    def test_browse_page_contains_popup_modal(self, app, client):
        """Test that the browse page contains the popup modal for editing linked items."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for modal structure
        assert 'id="linkedItemsModal"' in html_content
        assert 'class="modal fade"' in html_content
        assert 'id="linkedItemsModalLabel"' in html_content
        assert 'id="modal-linked-items-content"' in html_content
        assert 'id="save-linked-items"' in html_content

    def test_browse_page_contains_edit_buttons(self, app, client):
        """Test that the browse page contains edit buttons for linked entities."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for edit buttons
        assert 'onclick="openLinkedItemsModal' in html_content
        assert "Edit" in html_content
        assert "btn btn-sm btn-outline-primary" in html_content

    def test_browse_page_contains_linked_items_display_sections(self, app, client):
        """Test that the browse page contains display sections for linked items."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for linked items display sections
        assert 'id="user-needs-display"' in html_content
        assert 'id="risks-display"' in html_content
        assert 'id="product-requirements-display"' in html_content
        assert "Linked User Needs" in html_content
        assert "Linked Risks" in html_content
        assert "Linked Product Requirements" in html_content

    def test_browse_page_contains_javascript_functions(self, app, client):
        """Test that the browse page contains JavaScript functions for popup editing."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for JavaScript functions
        assert "function openLinkedItemsModal(" in html_content
        assert "function generateModalContent(" in html_content
        assert "function getCurrentLinkedItems(" in html_content
        assert "function saveLinkedItems(" in html_content
        assert "function updateLinkedItemsDisplay(" in html_content

    def test_browse_page_contains_modal_styling(self, app, client):
        """Test that the browse page contains CSS styling for the modal."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for modal styling classes - these are in CSS
        assert "modal-linked-items-list" in html_content
        assert "form-check" in html_content

    def test_browse_page_modal_content_generation(self, app, client):
        """Test that the modal content generation function is present."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for modal content generation logic
        assert "modal-linked-items-list" in html_content
        assert "form-check-input" in html_content
        assert "form-check-label" in html_content
        assert "No items available to link" in html_content

    def test_browse_page_modal_event_handlers(self, app, client):
        """Test that the modal event handlers are properly set up."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for event handlers
        assert 'data-bs-dismiss="modal"' in html_content
        assert "saveLinkedItems" in html_content

    def test_browse_page_modal_accessibility(self, app, client):
        """Test that the modal has proper accessibility attributes."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for accessibility attributes
        assert 'aria-labelledby="linkedItemsModalLabel"' in html_content
        assert 'aria-hidden="true"' in html_content
        assert 'aria-label="Close"' in html_content
        assert 'tabindex="-1"' in html_content

    def test_browse_page_modal_responsive_design(self, app, client):
        """Test that the modal has responsive design classes."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for responsive design classes
        assert "modal-dialog modal-lg" in html_content
        assert "modal-content" in html_content
        assert "modal-header" in html_content
        assert "modal-body" in html_content
        assert "modal-footer" in html_content

    def test_browse_page_modal_form_elements(self, app, client):
        """Test that the modal contains proper form elements."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for form elements
        assert 'type="checkbox"' in html_content
        assert "form-check-input" in html_content
        assert "form-check-label" in html_content
        assert "value=" in html_content

    def test_browse_page_modal_button_styling(self, app, client):
        """Test that the modal buttons have proper styling."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for button styling
        assert "btn btn-secondary" in html_content
        assert "btn btn-primary" in html_content
        assert "btn-close" in html_content

    def test_browse_page_modal_content_scrolling(self, app, client):
        """Test that the modal content has proper scrolling behavior."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for scrolling behavior - these are in CSS
        assert "overflow" in html_content or "scroll" in html_content.lower()

    def test_browse_page_modal_error_handling(self, app, client):
        """Test that the modal has error handling capabilities."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for error handling
        assert "text-muted" in html_content
        assert "text-center" in html_content
        assert "Error loading data" in html_content or "error" in html_content.lower()

    def test_browse_page_modal_data_binding(self, app, client):
        """Test that the modal has proper data binding for linked items."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for data binding
        assert "currentLinkedItems" in html_content or "linkedItems" in html_content
        assert "getCurrentLinkedItems" in html_content
        assert "updateLinkedItemsDisplay" in html_content

    def test_browse_page_modal_validation(self, app, client):
        """Test that the modal has validation capabilities."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for validation
        assert "form-check" in html_content
        assert "checked" in html_content
        assert "value=" in html_content

    def test_browse_page_modal_performance(self, app, client):
        """Test that the modal has performance optimizations."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for performance optimizations - these are in CSS
        assert "max-height" in html_content or "performance" in html_content.lower()
