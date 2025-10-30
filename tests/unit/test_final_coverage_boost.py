# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Final tests to push coverage over 80%."""

import os
import tempfile

import yaml

from app.data_utils import DHFDataManager


class TestFinalCoverageboost:
    """Additional tests for missing coverage."""

    def test_sync_analysis_to_dhf_not_found(self):
        """Test syncing non-existent analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            test_data = {
                "metadata": {"project_name": "Test"},
                "user_needs": {},
                "risks": {},
                "product_requirements": {},
                "software_specifications": {},
                "hardware_specifications": {},
                "mitigation_links": {},
                "configuration": {"severity_levels": [], "probability_harm_levels": []},
            }

            with open(data_file, "w") as f:
                yaml.safe_dump(test_data, f)

            manager = DHFDataManager(data_file)
            result = manager.sync_analysis_to_dhf("nonexistent")

            assert "error" in result

    def test_apply_dhf_sync_not_found(self):
        """Test applying sync for non-existent analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            test_data = {
                "metadata": {"project_name": "Test"},
                "user_needs": {},
                "risks": {},
                "product_requirements": {},
                "software_specifications": {},
                "hardware_specifications": {},
                "mitigation_links": {},
                "configuration": {"severity_levels": [], "probability_harm_levels": []},
            }

            with open(data_file, "w") as f:
                yaml.safe_dump(test_data, f)

            manager = DHFDataManager(data_file)
            changes = {"new_risks": [], "updated_risks": [], "new_specs": []}
            result = manager.apply_dhf_sync("nonexistent", changes)

            assert result is False

    def test_get_severity_name(self):
        """Test getting severity name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            test_data = {
                "metadata": {"project_name": "Test"},
                "configuration": {
                    "severity_mapping": {"S1": {"name": "Low", "description": "Minor"}}
                },
            }

            with open(data_file, "w") as f:
                yaml.safe_dump(test_data, f)

            manager = DHFDataManager(data_file)

            # Test existing severity
            assert manager.get_severity_name("S1") == "Low"

            # Test non-existent severity
            assert manager.get_severity_name("S99") == "S99"

    def test_get_probability_harm_name(self):
        """Test getting probability harm name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            test_data = {
                "metadata": {"project_name": "Test"},
                "configuration": {
                    "probability_harm_mapping": {
                        "PH1": {"name": "Rare", "description": "Unlikely"}
                    }
                },
            }

            with open(data_file, "w") as f:
                yaml.safe_dump(test_data, f)

            manager = DHFDataManager(data_file)

            # Test existing probability
            assert manager.get_probability_harm_name("PH1") == "Rare"

            # Test non-existent probability
            assert manager.get_probability_harm_name("PH99") == "PH99"

    def test_calculate_rbm_score(self):
        """Test RBM score calculation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "dhf_data.yaml")

            test_data = {"metadata": {"project_name": "Test"}, "configuration": {}}

            with open(data_file, "w") as f:
                yaml.safe_dump(test_data, f)

            manager = DHFDataManager(data_file)

            # Test valid calculation
            assert manager.calculate_rbm_score("S3", "PH2") == 6

            # Test with invalid values
            assert manager.calculate_rbm_score("S1", "PH1") == 1
            assert manager.calculate_rbm_score("SX", "PH1") == 1
            assert manager.calculate_rbm_score("S1", "PHX") == 1
