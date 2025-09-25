# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Pytest configuration and fixtures for Pocket DHF tests."""

import os
import tempfile

import pytest

from app import create_app
from app.data_utils import DHFDataManager


@pytest.fixture
def app(sample_dhf_data):
    """Create and configure a new app instance for each test."""
    # Create a temporary file for testing
    db_fd, db_path = tempfile.mkstemp()

    # Write sample data to the temporary file
    import yaml

    with open(db_path, "w") as f:
        yaml.dump(sample_dhf_data, f)

    app = create_app(data_file_path=db_path)
    app.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DEBUG": False,
        }
    )

    # Override the data file path for testing
    app.config["DHF_DATA_FILE"] = db_path

    yield app

    # Clean up
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_dhf_data():
    """Sample DHF data for testing."""
    return {
        "metadata": {
            "project_name": "Test Diabetes Monitor",
            "device_type": "Continuous Glucose Monitor",
            "version": "1.0.0",
            "created_date": "2025-01-01",
            "last_modified": "2025-01-01 12:00:00",
        },
        "user_needs": {
            "Athlete Performance": {
                "group_name": "Athlete Performance",
                "needs": {
                    "UN001": {
                        "title": "Accurate Glucose Monitoring",
                        "description": "The device must accurately measure blood glucose levels",
                    },
                    "UN002": {
                        "title": "Real-time Alerts",
                        "description": "The device must provide real-time alerts for dangerous glucose levels",
                    },
                },
            }
        },
        "risks": {
            "Patient Safety": {
                "group_name": "Patient Safety",
                "risks": {
                    "R001": {
                        "title": "Inaccurate Glucose Reading",
                        "harm": "Incorrect treatment decisions",
                        "sequence_of_events": "Sensor malfunction leads to false reading",
                        "hazardous_situation": "Patient receives incorrect insulin dose",
                        "probability_occurrence": "PO2",
                        "probability_harm": "PH3",
                        "severity": "S3",
                        "cannot_be_reduced_further": False,
                        "benefits_outweigh_risk": True,
                        "justification": "Risk is acceptable with proper calibration",
                    }
                },
            }
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
                                "title": "Glucose Measurement Accuracy",
                                "description": "The device must measure glucose with ±15% accuracy",
                                "linked_user_needs": ["UN001"],
                            }
                        },
                    }
                },
            }
        },
        "software_specifications": {
            "Measurement": {
                "group_name": "Measurement",
                "specifications": {
                    "SS001": {
                        "title": "Glucose Algorithm",
                        "description": "Algorithm for converting sensor data to glucose readings",
                        "linked_product_requirements": ["PR001"],
                    }
                },
            }
        },
        "hardware_specifications": {
            "Sensor": {
                "group_name": "Sensor",
                "specifications": {
                    "HS001": {
                        "title": "Glucose Sensor",
                        "description": "Electrochemical sensor for glucose detection",
                        "linked_product_requirements": ["PR001"],
                    }
                },
            }
        },
        "mitigation_links": {
            "ML001": {
                "specification_id": "SS001",
                "risk_id": "R001",
                "effect": "Reduces probability of occurrence by 1",
            }
        },
        "configuration": {
            "severity_mapping": {
                "S1": {"name": "Low", "description": "Minor impact"},
                "S2": {"name": "Medium", "description": "Moderate impact"},
                "S3": {"name": "High", "description": "Significant impact"},
            },
            "probability_occurrence_mapping": {
                "PO1": {"name": "Low", "description": "Unlikely to occur"},
                "PO2": {"name": "Medium", "description": "May occur occasionally"},
                "PO3": {"name": "High", "description": "Likely to occur frequently"},
            },
            "probability_harm_mapping": {
                "PH1": {"name": "Low", "description": "Unlikely to cause harm"},
                "PH2": {"name": "Medium", "description": "May cause harm"},
                "PH3": {"name": "High", "description": "Likely to cause harm"},
            },
        },
    }


@pytest.fixture
def data_manager(sample_dhf_data, tmp_path):
    """Create a data manager with sample data."""
    data_file = tmp_path / "test_dhf_data.yaml"

    # Write sample data to temporary file
    import yaml

    with open(data_file, "w") as f:
        yaml.dump(sample_dhf_data, f)

    return DHFDataManager(str(data_file))


@pytest.fixture
def mock_git_config():
    """Mock git configuration for testing."""
    return {"name": "Test User", "email": "test@example.com"}
