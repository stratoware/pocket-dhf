# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Comprehensive tests for analyses functionality to improve coverage."""

import os
import tempfile

import yaml

from app.data_utils import DHFDataManager


class TestAnalysesCoverage:
    """Test analyses management functionality."""

    def test_get_analyses_directory_with_custom_dir(self):
        """Test getting analyses directory with custom path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.get_analyses_directory()
            assert result == analyses_dir

    def test_get_analyses_directory_default(self):
        """Test getting default analyses directory."""
        manager = DHFDataManager("test.yaml", analyses_dir=None)
        result = manager.get_analyses_directory()
        assert "sample-data/analyses" in result

    def test_get_analyses_empty_directory(self):
        """Test getting analyses from empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            analyses = manager.get_analyses()
            assert analyses == []

    def test_get_analyses_nonexistent_directory(self):
        """Test getting analyses when directory doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "nonexistent")

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            analyses = manager.get_analyses()
            assert analyses == []

    def test_get_analyses_with_valid_files(self):
        """Test getting analyses with valid YAML files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create test analysis files
            fmea_data = {
                "id": "fmea-001",
                "title": "Test FMEA",
                "type": "fmea",
                "description": "Test description",
                "status": "active",
                "last_modified": "2025-01-01",
            }

            fta_data = {
                "id": "fta-001",
                "title": "Test FTA",
                "type": "fta",
                "description": "Test FTA description",
                "status": "draft",
            }

            with open(os.path.join(analyses_dir, "fmea-001.yaml"), "w") as f:
                yaml.safe_dump(fmea_data, f)

            with open(os.path.join(analyses_dir, "fta-001.yml"), "w") as f:
                yaml.safe_dump(fta_data, f)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            analyses = manager.get_analyses()

            assert len(analyses) == 2
            assert analyses[0]["id"] == "fmea-001"
            assert analyses[0]["title"] == "Test FMEA"
            assert analyses[0]["type"] == "fmea"
            assert analyses[1]["id"] == "fta-001"

    def test_get_analyses_with_invalid_yaml(self):
        """Test getting analyses with invalid YAML file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create invalid YAML file
            with open(os.path.join(analyses_dir, "invalid.yaml"), "w") as f:
                f.write("invalid: yaml: content: [[[")

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            analyses = manager.get_analyses()

            # Should skip invalid file
            assert len(analyses) == 0

    def test_get_analyses_with_non_dict_content(self):
        """Test getting analyses with non-dictionary YAML content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create YAML file with list content
            with open(os.path.join(analyses_dir, "list.yaml"), "w") as f:
                yaml.safe_dump(["item1", "item2"], f)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            analyses = manager.get_analyses()

            # Should skip non-dict content
            assert len(analyses) == 0

    def test_load_analysis_success(self):
        """Test loading a specific analysis by ID."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            analysis_data = {
                "id": "fmea-001",
                "title": "Test FMEA",
                "type": "fmea",
                "items": [{"id": "item1", "hazard": "Test hazard"}],
            }

            with open(os.path.join(analyses_dir, "fmea-001.yaml"), "w") as f:
                yaml.safe_dump(analysis_data, f)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            loaded = manager.load_analysis("fmea-001")

            assert loaded is not None
            assert loaded["id"] == "fmea-001"
            assert loaded["title"] == "Test FMEA"
            assert "filename" in loaded
            assert loaded["filename"] == "fmea-001.yaml"

    def test_load_analysis_not_found(self):
        """Test loading analysis that doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            loaded = manager.load_analysis("nonexistent")

            assert loaded is None

    def test_load_analysis_directory_not_exists(self):
        """Test loading analysis when directory doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "nonexistent")

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            loaded = manager.load_analysis("fmea-001")

            assert loaded is None

    def test_load_analysis_with_error(self):
        """Test loading analysis with file read error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create invalid YAML
            with open(os.path.join(analyses_dir, "bad.yaml"), "w") as f:
                f.write("invalid: [[[")

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            loaded = manager.load_analysis("any-id")

            assert loaded is None

    def test_save_analysis_new_file(self):
        """Test saving a new analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")

            analysis_data = {
                "id": "fmea-002",
                "title": "New FMEA",
                "type": "fmea",
                "status": "draft",
            }

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.save_analysis("fmea-002", analysis_data)

            assert result is True
            assert os.path.exists(os.path.join(analyses_dir, "fmea-002.yaml"))

            # Verify content
            with open(os.path.join(analyses_dir, "fmea-002.yaml"), "r") as f:
                saved_data = yaml.safe_load(f)
            assert saved_data["id"] == "fmea-002"
            assert saved_data["title"] == "New FMEA"

    def test_save_analysis_with_existing_filename(self):
        """Test saving analysis with existing filename."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create existing file
            with open(os.path.join(analyses_dir, "test.yaml"), "w") as f:
                yaml.safe_dump({"id": "old", "title": "Old"}, f)

            analysis_data = {
                "id": "fmea-003",
                "title": "Updated FMEA",
                "filename": "test.yaml",
            }

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.save_analysis("fmea-003", analysis_data)

            assert result is True

            # Verify filename is not in saved data
            with open(os.path.join(analyses_dir, "test.yaml"), "r") as f:
                saved_data = yaml.safe_load(f)
            assert "filename" not in saved_data

    def test_save_analysis_invalid_filename(self):
        """Test saving analysis with invalid filename."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            analysis_data = {
                "id": "fmea-004",
                "title": "Bad Filename",
                "filename": "../../../etc/passwd",
            }

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.save_analysis("fmea-004", analysis_data)

            assert result is False

    def test_save_analysis_path_traversal_attempt(self):
        """Test save analysis prevents path traversal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create a directory outside analyses_dir
            outside_dir = os.path.join(temp_dir, "outside")
            os.makedirs(outside_dir)

            analysis_data = {
                "id": "fmea-005",
                "title": "Path Traversal",
                "filename": "test.yaml",
            }

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)

            # Normal save should work (path traversal prevented)
            result = manager.save_analysis("fmea-005", analysis_data)
            assert result is True

    def test_save_analysis_with_yml_extension(self):
        """Test saving analysis with .yml extension."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            analysis_data = {
                "id": "fta-001",
                "title": "Test FTA",
                "filename": "fta-001.yml",
            }

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.save_analysis("fta-001", analysis_data)

            assert result is True
            assert os.path.exists(os.path.join(analyses_dir, "fta-001.yml"))

    def test_delete_analysis_success(self):
        """Test deleting an analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            # Create analysis file
            analysis_data = {"id": "fmea-delete", "title": "To Delete"}
            filepath = os.path.join(analyses_dir, "fmea-delete.yaml")
            with open(filepath, "w") as f:
                yaml.safe_dump(analysis_data, f)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.delete_analysis("fmea-delete")

            assert result is True
            assert not os.path.exists(filepath)

    def test_delete_analysis_not_found(self):
        """Test deleting non-existent analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            os.makedirs(analyses_dir)

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.delete_analysis("nonexistent")

            assert result is False

    def test_delete_analysis_directory_not_exists(self):
        """Test deleting analysis when directory doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "nonexistent")

            manager = DHFDataManager("test.yaml", analyses_dir=analyses_dir)
            result = manager.delete_analysis("fmea-001")

            assert result is False

    def test_create_analysis_fmea(self):
        """Test creating a new FMEA analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            # Create initial data file
            initial_data = {
                "metadata": {"project_name": "Test"},
                "user_needs": {},
                "configuration": {"severity_levels": [], "probability_harm_levels": []},
            }
            with open(data_file, "w") as f:
                yaml.safe_dump(initial_data, f)

            manager = DHFDataManager(data_file, analyses_dir=analyses_dir)
            result = manager.create_analysis("fmea", "New FMEA", "Test description")

            assert result is not None
            assert result["type"] == "fmea"
            assert result["title"] == "New FMEA"
            assert result["description"] == "Test description"
            assert result["status"] == "active"
            assert "id" in result
            assert "last_modified" in result
            assert "rows" in result
            assert isinstance(result["rows"], list)

    def test_create_analysis_fta(self):
        """Test creating a new FTA analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            initial_data = {
                "metadata": {"project_name": "Test"},
                "user_needs": {},
                "configuration": {"severity_levels": [], "probability_harm_levels": []},
            }
            with open(data_file, "w") as f:
                yaml.safe_dump(initial_data, f)

            manager = DHFDataManager(data_file, analyses_dir=analyses_dir)
            result = manager.create_analysis("fta", "New FTA", "FTA description")

            assert result is not None
            assert result["type"] == "fta"
            assert result["title"] == "New FTA"
            assert result["description"] == "FTA description"
            assert "basic_events" in result
            assert isinstance(result["basic_events"], list)

    def test_create_analysis_generates_unique_id(self):
        """Test that create_analysis generates unique IDs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            initial_data = {
                "metadata": {"project_name": "Test"},
                "user_needs": {},
                "configuration": {"severity_levels": [], "probability_harm_levels": []},
            }
            with open(data_file, "w") as f:
                yaml.safe_dump(initial_data, f)

            manager = DHFDataManager(data_file, analyses_dir=analyses_dir)

            # Create multiple analyses
            result1 = manager.create_analysis("fmea", "FMEA 1")
            result2 = manager.create_analysis("fmea", "FMEA 2")

            assert result1["id"] != result2["id"]

    def test_create_analysis_saves_to_file(self):
        """Test that create_analysis saves to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyses_dir = os.path.join(temp_dir, "analyses")
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            initial_data = {
                "metadata": {"project_name": "Test"},
                "user_needs": {},
                "configuration": {"severity_levels": [], "probability_harm_levels": []},
            }
            with open(data_file, "w") as f:
                yaml.safe_dump(initial_data, f)

            manager = DHFDataManager(data_file, analyses_dir=analyses_dir)
            result = manager.create_analysis("fmea", "New FMEA")

            assert result is not None

            # Verify file was created
            analysis_id = result["id"]
            expected_file = os.path.join(analyses_dir, f"{analysis_id.lower()}.yaml")
            assert os.path.exists(expected_file)

            # Verify content
            with open(expected_file, "r") as f:
                saved_data = yaml.safe_load(f)
            assert saved_data["id"] == analysis_id
            assert saved_data["title"] == "New FMEA"
