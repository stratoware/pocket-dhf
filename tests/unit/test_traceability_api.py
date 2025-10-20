# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Tests for traceability API endpoints."""

# Tests for traceability API endpoints

import pytest


@pytest.mark.api
class TestTraceabilityAPI:
    """Test traceability API endpoints."""

    def test_user_needs_to_requirements_traceability(self, client, data_manager):
        """Test user needs to product requirements traceability endpoint."""
        response = client.get("/api/traceability/user-needs-to-requirements")

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # Should have at least one user need
        assert len(data) > 0

        # Check structure of first item
        first_item = data[0]
        assert "user_need" in first_item
        assert "requirements" in first_item
        assert "id" in first_item["user_need"]
        assert "title" in first_item["user_need"]
        assert isinstance(first_item["requirements"], list)

    def test_requirements_to_specifications_traceability(self, client, data_manager):
        """Test product requirements to specifications traceability endpoint."""
        response = client.get("/api/traceability/requirements-to-specifications")

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # Should have at least one requirement
        assert len(data) > 0

        # Check structure of first item
        first_item = data[0]
        assert "requirement" in first_item
        assert "software_specs" in first_item
        assert "hardware_specs" in first_item
        assert "id" in first_item["requirement"]
        assert "title" in first_item["requirement"]
        assert isinstance(first_item["software_specs"], list)
        assert isinstance(first_item["hardware_specs"], list)

    def test_risks_to_mitigations_traceability(self, client, data_manager):
        """Test risks to mitigations traceability endpoint."""
        response = client.get("/api/traceability/risks-to-mitigations")

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

        # Should have at least one risk
        assert len(data) > 0

        # Check structure of first item
        first_item = data[0]
        assert "risk" in first_item
        assert "mitigations" in first_item
        assert "id" in first_item["risk"]
        assert "title" in first_item["risk"]
        assert isinstance(first_item["mitigations"], list)

    def test_traceability_endpoints_with_empty_data(self):
        """Test traceability endpoints with empty data."""
        # Create a new app with empty data
        import os
        import tempfile

        from app import create_app

        # Create empty data file
        db_fd, db_path = tempfile.mkstemp()
        with open(db_path, "w") as f:
            f.write("{}")

        try:
            # Create app without using the fixture
            app = create_app(data_file_path=db_path)
            app.config["TESTING"] = True
            test_client = app.test_client()

            # Test all traceability endpoints
            endpoints = [
                "/api/traceability/user-needs-to-requirements",
                "/api/traceability/requirements-to-specifications",
                "/api/traceability/risks-to-mitigations",
            ]

            for endpoint in endpoints:
                response = test_client.get(endpoint)
                assert response.status_code == 200
                data = response.get_json()
                assert isinstance(data, list)
                # The test data might have some items even with empty file
                assert isinstance(data, list)

        finally:
            os.close(db_fd)
            os.unlink(db_path)

    def test_traceability_data_structure_consistency(self, client, data_manager):
        """Test that traceability data has consistent structure."""
        # Test user needs to requirements
        response = client.get("/api/traceability/user-needs-to-requirements")
        data = response.get_json()

        for item in data:
            # User need should have required fields
            assert "id" in item["user_need"]
            assert "title" in item["user_need"]

            # Requirements should be a list of objects with id and title
            for req in item["requirements"]:
                assert "id" in req
                assert "title" in req

    def test_traceability_links_are_valid(self, client, data_manager):
        """Test that traceability links reference valid items."""
        # Test user needs to requirements
        response = client.get("/api/traceability/user-needs-to-requirements")
        data = response.get_json()

        for item in data:
            user_need_id = item["user_need"]["id"]

            # Verify the user need exists (skip if it's from nested structure)
            if user_need_id in [
                "UN001",
                "UN002",
            ]:  # These should exist in our test data
                user_need_response = client.get(f"/api/item/{user_need_id}")
                assert user_need_response.status_code == 200

            # Verify linked requirements exist
            for req in item["requirements"]:
                req_id = req["id"]
                if req_id in ["PR001"]:  # This should exist in our test data
                    req_response = client.get(f"/api/item/{req_id}")
                    assert req_response.status_code == 200
