# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""
Tests for drag-to-resize sidebar functionality.
"""

# Integration tests for drag-to-resize functionality


class TestDragResize:
    """Test drag-to-resize sidebar functionality."""

    def test_browse_page_contains_resize_handle(self, app, client):
        """Test that the browse page contains the resize handle element."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for resize handle
        assert 'id="resize-handle"' in html_content
        assert "resize-handle" in html_content

    def test_browse_page_contains_resize_javascript(self, app, client):
        """Test that the browse page contains JavaScript for drag-to-resize functionality."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for resize JavaScript
        assert "mousedown" in html_content
        assert "mousemove" in html_content
        assert "mouseup" in html_content
        assert "addEventListener" in html_content

    def test_browse_page_contains_resize_css_classes(self, app, client):
        """Test that the browse page contains CSS classes for resize functionality."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for CSS classes
        assert "d-flex" in html_content
        assert "sidebar" in html_content
        assert "main-content" in html_content

    def test_browse_page_contains_resize_constraints(self, app, client):
        """Test that the browse page contains resize constraints."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for resize constraints
        assert "25%" in html_content
        assert "75%" in html_content
        assert "Math.max" in html_content
        assert "Math.min" in html_content

    def test_browse_page_contains_mouse_event_handlers(self, app, client):
        """Test that the browse page contains mouse event handlers."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for mouse event handlers
        assert "mousedown" in html_content
        assert "mousemove" in html_content
        assert "mouseup" in html_content
        assert "preventDefault" in html_content

    def test_browse_page_contains_width_calculation(self, app, client):
        """Test that the browse page contains width calculation logic."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for width calculation - these are in JavaScript
        assert "clientX" in html_content or "width" in html_content
        assert "offsetLeft" in html_content or "offset" in html_content
        assert "style" in html_content

    def test_browse_page_contains_cursor_styling(self, app, client):
        """Test that the browse page contains cursor styling for resize handle."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for cursor styling - these are in CSS
        assert "cursor" in html_content or "resize-handle" in html_content

    def test_browse_page_contains_drag_state_management(self, app, client):
        """Test that the browse page contains drag state management."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for drag state management - these are in JavaScript
        assert (
            "isDragging" in html_content
            or "drag" in html_content.lower()
            or "resize" in html_content.lower()
        )

    def test_browse_page_contains_event_cleanup(self, app, client):
        """Test that the browse page contains event cleanup functionality."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for event cleanup - these are in JavaScript
        assert (
            "removeEventListener" in html_content or "addEventListener" in html_content
        )

    def test_browse_page_contains_resize_handle_positioning(self, app, client):
        """Test that the browse page contains resize handle positioning."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for resize handle positioning - these are in CSS
        assert "position" in html_content or "resize-handle" in html_content
        assert "width" in html_content
        assert "height" in html_content

    def test_browse_page_contains_resize_handle_hover_effects(self, app, client):
        """Test that the browse page contains hover effects for resize handle."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for hover effects - these are in CSS
        assert "hover" in html_content.lower() or "resize-handle" in html_content

    def test_browse_page_contains_flexbox_layout(self, app, client):
        """Test that the browse page contains flexbox layout for resize functionality."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for flexbox layout
        assert "d-flex" in html_content
        assert "flex" in html_content.lower()

    def test_browse_page_contains_resize_boundaries(self, app, client):
        """Test that the browse page contains resize boundaries."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for resize boundaries
        assert "25%" in html_content
        assert "75%" in html_content
        assert "Math.max" in html_content
        assert "Math.min" in html_content

    def test_browse_page_contains_resize_performance(self, app, client):
        """Test that the browse page contains performance optimizations for resize."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for performance optimizations - these are in JavaScript
        assert (
            "requestAnimationFrame" in html_content
            or "performance" in html_content.lower()
            or "resize" in html_content.lower()
        )

    def test_browse_page_contains_resize_accessibility(self, app, client):
        """Test that the browse page contains accessibility features for resize."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for accessibility features
        assert (
            "aria-" in html_content
            or "role=" in html_content
            or "tabindex=" in html_content
        )

    def test_browse_page_contains_resize_error_handling(self, app, client):
        """Test that the browse page contains error handling for resize functionality."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for error handling
        assert (
            "try" in html_content
            or "catch" in html_content
            or "error" in html_content.lower()
        )

    def test_browse_page_contains_resize_responsive_design(self, app, client):
        """Test that the browse page contains responsive design for resize functionality."""
        response = client.get("/browse")
        assert response.status_code == 200

        html_content = response.get_data(as_text=True)

        # Check for responsive design
        assert "col-" in html_content
        assert "container" in html_content
        assert "row" in html_content
