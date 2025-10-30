# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Tests for schema migration system."""

import pytest
import yaml

from app.schema_migrations import (
    CURRENT_SCHEMA_VERSION,
    SCHEMA_VERSION_1_0,
    SCHEMA_VERSION_2_0,
    get_schema_version,
    migrate_to_latest,
    migrate_v1_to_v2,
    needs_migration,
)


class TestSchemaVersionDetection:
    """Tests for schema version detection."""

    def test_get_schema_version_with_explicit_version(self):
        """Test getting schema version when explicitly set in metadata."""
        data = {
            "metadata": {"schema_version": "2.0"},
            "configuration": {},
            "risks": {},
        }
        assert get_schema_version(data) == "2.0"

    def test_get_schema_version_v1_0_indicator(self):
        """Test detecting v1.0 from presence of probability_occurrence_mapping."""
        data = {
            "configuration": {
                "probability_occurrence_mapping": {
                    "PO1": {"name": "Low", "description": "Unlikely"}
                }
            },
            "risks": {},
        }
        assert get_schema_version(data) == SCHEMA_VERSION_1_0

    def test_get_schema_version_defaults_to_current(self):
        """Test that version defaults to current when no indicators present."""
        data = {"configuration": {}, "risks": {}}
        assert get_schema_version(data) == CURRENT_SCHEMA_VERSION

    def test_needs_migration_true_for_v1_0(self):
        """Test that v1.0 data needs migration."""
        data = {
            "configuration": {
                "probability_occurrence_mapping": {"PO1": {"name": "Low"}}
            }
        }
        assert needs_migration(data) is True

    def test_needs_migration_false_for_current(self):
        """Test that current version data doesn't need migration."""
        data = {"metadata": {"schema_version": CURRENT_SCHEMA_VERSION}}
        assert needs_migration(data) is False


class TestMigrationV1ToV2:
    """Tests for v1.0 to v2.0 migration."""

    def test_migrate_v1_to_v2_removes_probability_occurrence_mapping(self):
        """Test that migration removes probability_occurrence_mapping."""
        data = {
            "metadata": {},
            "configuration": {
                "severity_mapping": {"S1": {"name": "Low"}},
                "probability_occurrence_mapping": {
                    "PO1": {"name": "Low"},
                    "PO2": {"name": "Medium"},
                    "PO3": {"name": "High"},
                },
                "probability_harm_mapping": {"PH1": {"name": "Low"}},
            },
            "risks": {},
        }

        result = migrate_v1_to_v2(data)

        assert "probability_occurrence_mapping" not in result["configuration"]
        assert "severity_mapping" in result["configuration"]
        assert "probability_harm_mapping" in result["configuration"]

    def test_migrate_v1_to_v2_removes_probability_occurrence_from_risks(self):
        """Test that migration removes probability_occurrence from all risks."""
        data = {
            "metadata": {},
            "configuration": {},
            "risks": {
                "patient_safety": {
                    "group_name": "Patient Safety",
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "title": "Test Risk",
                            "severity": "S3",
                            "probability_occurrence": "PO2",
                            "probability_harm": "PH3",
                        },
                        "R002": {
                            "id": "R002",
                            "title": "Another Risk",
                            "severity": "S2",
                            "probability_occurrence": "PO1",
                            "probability_harm": "PH2",
                        },
                    },
                }
            },
        }

        result = migrate_v1_to_v2(data)

        for group in result["risks"].values():
            for risk in group["risks"].values():
                assert "probability_occurrence" not in risk
                assert "probability_harm" in risk
                assert "severity" in risk

    def test_migrate_v1_to_v2_preserves_other_risk_fields(self):
        """Test that migration preserves all other risk fields."""
        data = {
            "metadata": {},
            "configuration": {},
            "risks": {
                "patient_safety": {
                    "group_name": "Patient Safety",
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "title": "Test Risk",
                            "hazard": "Test Hazard",
                            "harm": "Test Harm",
                            "severity": "S3",
                            "probability_occurrence": "PO2",
                            "probability_harm": "PH3",
                            "justification": "Test justification",
                            "benefits_outweigh_risk": True,
                        }
                    },
                }
            },
        }

        result = migrate_v1_to_v2(data)

        risk = result["risks"]["patient_safety"]["risks"]["R001"]
        assert risk["id"] == "R001"
        assert risk["title"] == "Test Risk"
        assert risk["hazard"] == "Test Hazard"
        assert risk["harm"] == "Test Harm"
        assert risk["severity"] == "S3"
        assert risk["probability_harm"] == "PH3"
        assert risk["justification"] == "Test justification"
        assert risk["benefits_outweigh_risk"] is True

    def test_migrate_v1_to_v2_sets_schema_version(self):
        """Test that migration sets schema_version in metadata."""
        data = {"metadata": {}, "configuration": {}, "risks": {}}

        result = migrate_v1_to_v2(data)

        assert "schema_version" in result["metadata"]
        assert result["metadata"]["schema_version"] == SCHEMA_VERSION_2_0

    def test_migrate_v1_to_v2_handles_legacy_flat_risk_structure(self):
        """Test migration handles legacy flat risk structure."""
        data = {
            "metadata": {},
            "configuration": {},
            "risks": {
                "R001": {
                    "id": "R001",
                    "title": "Flat Structure Risk",
                    "severity": "S2",
                    "probability_occurrence": "PO1",
                    "probability_harm": "PH2",
                }
            },
        }

        result = migrate_v1_to_v2(data)

        # In flat structure, probability_occurrence should be removed from top-level risk
        assert "probability_occurrence" not in result["risks"]["R001"]
        assert result["risks"]["R001"]["probability_harm"] == "PH2"


class TestMigrateToLatest:
    """Tests for migrate_to_latest function."""

    def test_migrate_to_latest_from_v1_0(self):
        """Test migrating from v1.0 to current version."""
        data = {
            "metadata": {},
            "configuration": {
                "probability_occurrence_mapping": {"PO1": {"name": "Low"}}
            },
            "risks": {
                "patient_safety": {
                    "group_name": "Patient Safety",
                    "risks": {
                        "R001": {
                            "id": "R001",
                            "severity": "S2",
                            "probability_occurrence": "PO1",
                            "probability_harm": "PH2",
                        }
                    },
                }
            },
        }

        result = migrate_to_latest(data)

        assert get_schema_version(result) == CURRENT_SCHEMA_VERSION
        assert "probability_occurrence_mapping" not in result["configuration"]
        assert (
            "probability_occurrence"
            not in result["risks"]["patient_safety"]["risks"]["R001"]
        )

    def test_migrate_to_latest_already_current(self):
        """Test that migrating already-current data returns unchanged."""
        data = {
            "metadata": {"schema_version": CURRENT_SCHEMA_VERSION},
            "configuration": {},
            "risks": {},
        }

        result = migrate_to_latest(data)

        assert result == data
        assert get_schema_version(result) == CURRENT_SCHEMA_VERSION

    def test_migrate_to_latest_with_explicit_from_version(self):
        """Test specifying explicit from_version parameter."""
        data = {"metadata": {}, "configuration": {}, "risks": {}}

        result = migrate_to_latest(data, from_version=SCHEMA_VERSION_1_0)

        assert get_schema_version(result) == CURRENT_SCHEMA_VERSION

    def test_migrate_to_latest_raises_on_missing_migration(self):
        """Test that error is raised when migration path doesn't exist."""
        data = {"metadata": {"schema_version": "99.0"}, "configuration": {}}

        with pytest.raises(ValueError, match="No migration available"):
            migrate_to_latest(data)


class TestRealWorldMigration:
    """Tests using real v1.0 sample data."""

    def test_migrate_real_v1_0_sample_data(self):
        """Test migrating the actual v1.0 sample data file."""
        # Load the v1.0 sample data
        with open("sample-data/dhf_data_v1.yaml", "r", encoding="utf-8") as f:
            v1_data = yaml.safe_load(f)

        # Perform migration
        v2_data = migrate_to_latest(v1_data)

        # Verify schema version is updated
        assert v2_data["metadata"]["schema_version"] == SCHEMA_VERSION_2_0

        # Verify probability_occurrence_mapping is removed
        assert "probability_occurrence_mapping" not in v2_data["configuration"]

        # Verify probability_harm_mapping is preserved
        assert "probability_harm_mapping" in v2_data["configuration"]

        # Count risks and verify probability_occurrence is removed from all
        risk_count = 0
        for group in v2_data["risks"].values():
            if "risks" in group:
                for risk in group["risks"].values():
                    risk_count += 1
                    assert "probability_occurrence" not in risk
                    assert "probability_harm" in risk
                    assert "severity" in risk

        # Should have migrated all risks from original data (16 risks total, R005 is skipped)
        assert risk_count >= 16, f"Expected at least 16 risks, found {risk_count}"

    def test_migration_idempotency(self):
        """Test that migrating v2.0 data again is safe (idempotent)."""
        # Load and migrate v1.0 data
        with open("sample-data/dhf_data_v1.yaml", "r", encoding="utf-8") as f:
            v1_data = yaml.safe_load(f)

        v2_data = migrate_to_latest(v1_data)

        # Migrate again - should be safe
        v2_data_again = migrate_to_latest(v2_data)

        # Should be identical (or at least have same structure)
        assert v2_data_again["metadata"]["schema_version"] == SCHEMA_VERSION_2_0
        assert "probability_occurrence_mapping" not in v2_data_again["configuration"]

    def test_migration_preserves_all_risk_count(self):
        """Test that migration doesn't lose any risks."""
        with open("sample-data/dhf_data_v1.yaml", "r", encoding="utf-8") as f:
            v1_data = yaml.safe_load(f)

        # Count v1 risks
        v1_risk_count = 0
        for group in v1_data["risks"].values():
            if "risks" in group:
                v1_risk_count += len(group["risks"])

        # Migrate
        v2_data = migrate_to_latest(v1_data)

        # Count v2 risks
        v2_risk_count = 0
        for group in v2_data["risks"].values():
            if "risks" in group:
                v2_risk_count += len(group["risks"])

        assert (
            v1_risk_count == v2_risk_count
        ), f"Migration lost risks: v1 had {v1_risk_count}, v2 has {v2_risk_count}"
