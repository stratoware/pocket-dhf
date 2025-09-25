# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Tests for 3-level nested product requirements structure."""

import pytest
import yaml
import tempfile
import os

from app.data_utils import DHFDataManager


@pytest.mark.unit
class TestNestedRequirements:
    """Test 3-level nested product requirements functionality."""

    @pytest.fixture
    def nested_requirements_data(self):
        """Sample data with 3-level nested product requirements."""
        return {
            "metadata": {
                "project_name": "Test Project",
                "version": "1.0.0"
            },
            "product_requirements": {
                "functional_requirements": {
                    "group_name": "Functional Requirements",
                    "description": "Core functionality that the system must provide",
                    "requirements": {
                        "muscle_contraction_measurement": {
                            "group_name": "Muscle Contraction Measurement",
                            "description": "Requirements for measuring muscle contraction percentages",
                            "requirements": {
                                "PR001": {
                                    "id": "PR001",
                                    "title": "Quadricep Contraction Measurement",
                                    "description": "The sleeve shall measure quadricep contraction in percent with an accuracy of +/- 1%",
                                    "linked_user_needs": ["UN001"]
                                },
                                "PR002": {
                                    "id": "PR002", 
                                    "title": "Hamstring Contraction Measurement",
                                    "description": "The sleeve shall measure hamstring contraction in percent with an accuracy of +/- 1%",
                                    "linked_user_needs": ["UN002"]
                                }
                            }
                        },
                        "flexion_extension_measurement": {
                            "group_name": "Flexion/Extension Measurement",
                            "description": "Requirements for measuring joint angles",
                            "requirements": {
                                "PR003": {
                                    "id": "PR003",
                                    "title": "Quadricep Flexion Measurement",
                                    "description": "The sleeve shall measure quadricep flexion in degrees with an accuracy of +/- 1 degree",
                                    "linked_user_needs": ["UN003"]
                                }
                            }
                        }
                    }
                },
                "performance_requirements": {
                    "group_name": "Performance Requirements",
                    "description": "Quantitative performance criteria the system must meet",
                    "requirements": {
                        "measurement_accuracy": {
                            "group_name": "Measurement Accuracy",
                            "description": "Accuracy requirements for all measurement functions",
                            "requirements": {
                                "PR015": {
                                    "id": "PR015",
                                    "title": "Muscle Contraction Accuracy",
                                    "description": "The system shall measure muscle contraction percentages with an accuracy of +/- 1% across the full measurement range",
                                    "linked_user_needs": ["UN001"]
                                }
                            }
                        }
                    }
                }
            },
            "user_needs": {
                "Athlete Performance": {
                    "group_name": "Athlete Performance",
                    "needs": {
                        "UN001": {
                            "id": "UN001",
                            "title": "Quantitative and trustworthy metrics",
                            "description": "Athletes need reliable data to track performance"
                        },
                        "UN002": {
                            "id": "UN002",
                            "title": "Real-time biofeedback during training",
                            "description": "Athletes need immediate feedback during workouts"
                        },
                        "UN003": {
                            "id": "UN003",
                            "title": "Information easily consumable or summarized",
                            "description": "Athletes need clear, actionable information"
                        }
                    }
                }
            }
        }

    @pytest.fixture
    def nested_data_manager(self, nested_requirements_data, tmp_path):
        """Create a data manager with nested requirements data."""
        data_file = tmp_path / "nested_dhf_data.yaml"
        
        with open(data_file, "w") as f:
            yaml.dump(nested_requirements_data, f)
            
        return DHFDataManager(str(data_file))

    def test_get_item_by_id_nested_structure(self, nested_data_manager):
        """Test getting items by ID in 3-level nested structure."""
        # Test getting a requirement from nested structure
        item = nested_data_manager.get_item_by_id("PR001")
        assert item is not None
        assert item["title"] == "Quadricep Contraction Measurement"
        assert item["id"] == "PR001"
        
        # Test getting another requirement
        item = nested_data_manager.get_item_by_id("PR015")
        assert item is not None
        assert item["title"] == "Muscle Contraction Accuracy"
        assert item["id"] == "PR015"

    def test_update_item_nested_structure(self, nested_data_manager):
        """Test updating items in 3-level nested structure."""
        # Update a requirement in nested structure
        updated_data = {
            "title": "Updated Quadricep Contraction Measurement",
            "description": "Updated description"
        }
        
        success = nested_data_manager.update_item("PR001", updated_data)
        assert success is True
        
        # Verify the update
        item = nested_data_manager.get_item_by_id("PR001")
        assert item["title"] == "Updated Quadricep Contraction Measurement"
        assert item["description"] == "Updated description"

    def test_get_linkable_items_nested_structure(self, nested_data_manager):
        """Test getting linkable items from nested structure."""
        linkable_items = nested_data_manager.get_linkable_items()
        
        # Should include product requirements from nested structure
        assert "product_requirements" in linkable_items
        pr_items = linkable_items["product_requirements"]
        
        # Should have all requirements from nested structure
        pr_ids = [item["id"] for item in pr_items]
        assert "PR001" in pr_ids
        assert "PR002" in pr_ids
        assert "PR003" in pr_ids
        assert "PR015" in pr_ids
        
        # Check titles are correct
        pr_titles = {item["id"]: item["title"] for item in pr_items}
        assert pr_titles["PR001"] == "Quadricep Contraction Measurement"
        assert pr_titles["PR015"] == "Muscle Contraction Accuracy"

    def test_traceability_with_nested_structure(self, nested_data_manager):
        """Test traceability functionality with nested structure."""
        # Test user needs to requirements traceability
        data = nested_data_manager.load_data()
        
        # Find linked requirements for UN001
        linked_requirements = []
        for pr_group in data.get("product_requirements", {}).values():
            if "requirements" in pr_group:
                # Handle 3-level structure
                if any(isinstance(req, dict) and "requirements" in req for req in pr_group["requirements"].values()):
                    for sub_group in pr_group["requirements"].values():
                        if "requirements" in sub_group:
                            for req_id, req in sub_group["requirements"].items():
                                if "UN001" in req.get("linked_user_needs", []):
                                    linked_requirements.append(req_id)
        
        # Should find PR001 and PR015 linked to UN001
        assert "PR001" in linked_requirements
        assert "PR015" in linked_requirements

    def test_nested_structure_counting(self, nested_data_manager):
        """Test counting requirements in nested structure."""
        data = nested_data_manager.load_data()
        
        # Count all requirements in nested structure
        total_count = 0
        for pr_group in data.get("product_requirements", {}).values():
            if "requirements" in pr_group:
                # Handle 3-level structure
                if any(isinstance(req, dict) and "requirements" in req for req in pr_group["requirements"].values()):
                    for sub_group in pr_group["requirements"].values():
                        if "requirements" in sub_group:
                            total_count += len(sub_group["requirements"])
        
        # Should have 4 requirements total
        assert total_count == 4

    def test_mixed_structure_support(self, tmp_path):
        """Test support for both 2-level and 3-level structures."""
        # Create data with mixed structures
        mixed_data = {
            "metadata": {"project_name": "Test Project"},
            "product_requirements": {
                "functional_requirements": {
                    "group_name": "Functional Requirements",
                    "requirements": {
                        "PR001": {
                            "id": "PR001",
                            "title": "Direct Requirement",
                            "description": "A requirement in 2-level structure"
                        }
                    }
                },
                "performance_requirements": {
                    "group_name": "Performance Requirements", 
                    "requirements": {
                        "measurement_accuracy": {
                            "group_name": "Measurement Accuracy",
                            "requirements": {
                                "PR002": {
                                    "id": "PR002",
                                    "title": "Nested Requirement",
                                    "description": "A requirement in 3-level structure"
                                }
                            }
                        }
                    }
                }
            }
        }
        
        data_file = tmp_path / "mixed_dhf_data.yaml"
        with open(data_file, "w") as f:
            yaml.dump(mixed_data, f)
            
        data_manager = DHFDataManager(str(data_file))
        
        # Should be able to get both types of requirements
        pr001 = data_manager.get_item_by_id("PR001")
        assert pr001 is not None
        assert pr001["title"] == "Direct Requirement"
        
        pr002 = data_manager.get_item_by_id("PR002")
        assert pr002 is not None
        assert pr002["title"] == "Nested Requirement"
        
        # Should be able to update both types
        data_manager.update_item("PR001", {"title": "Updated Direct"})
        data_manager.update_item("PR002", {"title": "Updated Nested"})
        
        pr001 = data_manager.get_item_by_id("PR001")
        assert pr001["title"] == "Updated Direct"
        
        pr002 = data_manager.get_item_by_id("PR002")
        assert pr002["title"] == "Updated Nested"

