"""
Tests for dynamic linked_risks functionality in /api/item endpoint.
"""

import pytest
from unittest.mock import patch, MagicMock
from app import create_app


class TestDynamicLinkedRisks:
    """Test dynamic linked_risks functionality."""

    def test_api_item_with_linked_risks_software_spec(self, app, client):
        """Test that software specifications get linked_risks dynamically added."""
        # Mock the data manager to return a software spec without linked_risks
        mock_data = {
            "software_specifications": {
                "sensor_processing": {
                    "specifications": {
                        "SS001": {
                            "id": "SS001",
                            "title": "Motion Sensor Fusion",
                            "description": "Multi-sensor fusion algorithm",
                            "linked_product_requirements": ["PR004", "PR005"]
                        }
                    }
                }
            },
            "mitigation_links": {
                "ML001": {
                    "specification_id": "SS001",
                    "risk_id": "R001",
                    "specification_type": "software"
                }
            },
            "risks": {
                "safety": {
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "title": "Sensor Malfunction",
                            "description": "Risk of sensor failure"
                        }
                    }
                }
            }
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["software_specifications"]["sensor_processing"]["specifications"]["SS001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/SS001')
            
            assert response.status_code == 200
            data = response.get_json()
            assert "linked_risks" in data
            assert data["linked_risks"] == ["R001"]
            assert data["id"] == "SS001"
            assert data["title"] == "Motion Sensor Fusion"

    def test_api_item_with_linked_risks_hardware_spec(self, app, client):
        """Test that hardware specifications get linked_risks dynamically added."""
        mock_data = {
            "hardware_specifications": {
                "sensors": {
                    "specifications": {
                        "HS001": {
                            "id": "HS001",
                            "title": "9-Axis IMU Sensor",
                            "description": "Integrated 9-axis inertial measurement unit",
                            "linked_product_requirements": ["PR004", "PR005"]
                        }
                    }
                }
            },
            "mitigation_links": {
                "ML001": {
                    "specification_id": "HS001",
                    "risk_id": "R001",
                    "specification_type": "hardware"
                }
            },
            "risks": {
                "safety": {
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "title": "Sensor Malfunction",
                            "description": "Risk of sensor failure"
                        }
                    }
                }
            }
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["hardware_specifications"]["sensors"]["specifications"]["HS001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/HS001')
            
            assert response.status_code == 200
            data = response.get_json()
            assert "linked_risks" in data
            assert data["linked_risks"] == ["R001"]
            assert data["id"] == "HS001"
            assert data["title"] == "9-Axis IMU Sensor"

    def test_api_item_with_multiple_linked_risks(self, app, client):
        """Test that specifications with multiple linked risks work correctly."""
        mock_data = {
            "software_specifications": {
                "sensor_processing": {
                    "specifications": {
                        "SS001": {
                            "id": "SS001",
                            "title": "Motion Sensor Fusion",
                            "description": "Multi-sensor fusion algorithm",
                            "linked_product_requirements": ["PR004", "PR005"]
                        }
                    }
                }
            },
            "mitigation_links": {
                "ML001": {
                    "specification_id": "SS001",
                    "risk_id": "R001",
                    "specification_type": "software"
                },
                "ML002": {
                    "specification_id": "SS001",
                    "risk_id": "R002",
                    "specification_type": "software"
                }
            },
            "risks": {
                "safety": {
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "title": "Sensor Malfunction",
                            "description": "Risk of sensor failure"
                        },
                        "R002": {
                            "id": "R002",
                            "title": "Data Loss",
                            "description": "Risk of data loss"
                        }
                    }
                }
            }
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["software_specifications"]["sensor_processing"]["specifications"]["SS001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/SS001')
            
            assert response.status_code == 200
            data = response.get_json()
            assert "linked_risks" in data
            assert set(data["linked_risks"]) == {"R001", "R002"}
            assert len(data["linked_risks"]) == 2

    def test_api_item_without_linked_risks(self, app, client):
        """Test that specifications without linked risks don't get the field added."""
        mock_data = {
            "software_specifications": {
                "sensor_processing": {
                    "specifications": {
                        "SS001": {
                            "id": "SS001",
                            "title": "Motion Sensor Fusion",
                            "description": "Multi-sensor fusion algorithm",
                            "linked_product_requirements": ["PR004", "PR005"]
                        }
                    }
                }
            },
            "mitigation_links": {},
            "risks": {}
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["software_specifications"]["sensor_processing"]["specifications"]["SS001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/SS001')
            
            assert response.status_code == 200
            data = response.get_json()
            assert "linked_risks" not in data
            assert data["id"] == "SS001"

    def test_api_item_non_specification_item(self, app, client):
        """Test that non-specification items (user needs, risks, etc.) don't get linked_risks."""
        mock_data = {
            "user_needs": {
                "performance": {
                    "needs": {
                        "UN001": {
                            "id": "UN001",
                            "title": "Quantitative and trustworthy metrics",
                            "description": "Athletes need quantitative and trustworthy metrics"
                        }
                    }
                }
            }
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["user_needs"]["performance"]["needs"]["UN001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/UN001')
            
            assert response.status_code == 200
            data = response.get_json()
            assert "linked_risks" not in data
            assert data["id"] == "UN001"

    def test_api_item_with_invalid_risk_id(self, app, client):
        """Test that invalid risk IDs in mitigation links are handled gracefully."""
        mock_data = {
            "software_specifications": {
                "sensor_processing": {
                    "specifications": {
                        "SS001": {
                            "id": "SS001",
                            "title": "Motion Sensor Fusion",
                            "description": "Multi-sensor fusion algorithm"
                        }
                    }
                }
            },
            "mitigation_links": {
                "ML001": {
                    "specification_id": "SS001",
                    "risk_id": "INVALID_RISK",
                    "specification_type": "software"
                }
            },
            "risks": {
                "safety": {
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "title": "Valid Risk",
                            "description": "A valid risk"
                        }
                    }
                }
            }
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["software_specifications"]["sensor_processing"]["specifications"]["SS001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/SS001')
            
            assert response.status_code == 200
            data = response.get_json()
            # Should not have linked_risks since the risk ID is invalid
            assert "linked_risks" not in data

    def test_api_item_with_missing_risk_data(self, app, client):
        """Test that missing risk data is handled gracefully."""
        mock_data = {
            "software_specifications": {
                "sensor_processing": {
                    "specifications": {
                        "SS001": {
                            "id": "SS001",
                            "title": "Motion Sensor Fusion",
                            "description": "Multi-sensor fusion algorithm"
                        }
                    }
                }
            },
            "mitigation_links": {
                "ML001": {
                    "specification_id": "SS001",
                    "risk_id": "R001",
                    "specification_type": "software"
                }
            },
            "risks": {}  # Empty risks section
        }
        
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = mock_data["software_specifications"]["sensor_processing"]["specifications"]["SS001"]
            mock_dm.load_data.return_value = mock_data
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/SS001')
            
            assert response.status_code == 200
            data = response.get_json()
            # Should not have linked_risks since the risk data is missing
            assert "linked_risks" not in data

    def test_api_item_error_handling(self, app, client):
        """Test error handling in the linked_risks functionality."""
        with patch('app.routes.get_data_manager') as mock_get_dm:
            mock_dm = MagicMock()
            mock_dm.get_item_by_id.return_value = {
                "id": "SS001",
                "title": "Test Spec"
            }
            mock_dm.load_data.side_effect = Exception("Database error")
            mock_get_dm.return_value = mock_dm
            
            response = client.get('/api/item/SS001')
            
            assert response.status_code == 500
            data = response.get_json()
            assert "error" in data
