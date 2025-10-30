# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Tests for analyses API routes to improve coverage."""

import os

import yaml


class TestAnalysesRoutes:
    """Test analyses-related routes."""

    def test_api_get_analyses_empty(self, client):
        """Test getting empty analyses list."""
        response = client.get("/api/analyses")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_api_get_analysis_not_found(self, client):
        """Test getting non-existent analysis."""
        response = client.get("/api/analyses/nonexistent")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_api_update_analysis(self, app, client):
        """Test updating an analysis."""
        analyses_dir = app.config["DHF_ANALYSES_DIR"]

        analysis_data = {
            "id": "fmea-update-001",
            "title": "Original Title",
            "type": "fmea",
            "items": [],
        }

        with open(os.path.join(analyses_dir, "fmea-update-001.yaml"), "w") as f:
            yaml.safe_dump(analysis_data, f)

        updated_data = {
            "id": "fmea-update-001",
            "title": "Updated Title",
            "type": "fmea",
            "items": [],
            "filename": "fmea-update-001.yaml",
        }

        response = client.put(
            "/api/analyses/fmea-update-001",
            json=updated_data,
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_api_delete_analysis_not_found(self, client):
        """Test deleting non-existent analysis."""
        response = client.delete("/api/analyses/nonexistent")
        assert response.status_code == 404

    def test_api_create_analysis_fmea(self, client):
        """Test creating a new FMEA analysis."""
        data = {
            "type": "fmea",
            "title": "New FMEA via API",
            "description": "Created via API",
        }

        response = client.post(
            "/api/analyses", json=data, content_type="application/json"
        )
        assert response.status_code == 200
        result = response.get_json()
        assert result["success"] is True
        assert "analysis" in result
        assert result["analysis"]["type"] == "fmea"
        assert result["analysis"]["title"] == "New FMEA via API"

    def test_api_create_analysis_fta(self, client):
        """Test creating a new FTA analysis."""
        data = {
            "type": "fta",
            "title": "New FTA via API",
            "description": "FTA description",
        }

        response = client.post(
            "/api/analyses", json=data, content_type="application/json"
        )
        assert response.status_code == 200
        result = response.get_json()
        assert result["success"] is True
        assert result["analysis"]["type"] == "fta"

    def test_api_create_analysis_missing_type(self, client):
        """Test creating analysis without type."""
        data = {"title": "Missing Type"}

        response = client.post(
            "/api/analyses", json=data, content_type="application/json"
        )
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result

    def test_api_create_analysis_missing_title(self, client):
        """Test creating analysis without title."""
        data = {"type": "fmea"}

        response = client.post(
            "/api/analyses", json=data, content_type="application/json"
        )
        assert response.status_code == 400

    def test_api_create_analysis_invalid_type(self, client):
        """Test creating analysis with invalid type."""
        data = {"type": "invalid", "title": "Invalid Type"}

        response = client.post(
            "/api/analyses", json=data, content_type="application/json"
        )
        assert response.status_code == 400

    def test_analyses_page(self, app, client):
        """Test analyses page rendering."""
        response = client.get("/analyses")
        assert response.status_code == 200
        assert b"Analyses" in response.data
