# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Data utilities for loading and managing DHF YAML data."""

import logging
import os
from typing import Any, Dict, List, Optional

import yaml

from app.schema_migrations import migrate_to_latest, needs_migration

logger = logging.getLogger(__name__)


class DHFDataManager:
    """Manages loading and saving of DHF data from YAML files."""

    def __init__(self, data_file_path: str = None, analyses_dir: str = None):
        """Initialize the data manager with a YAML file path and optional analyses directory."""
        if data_file_path is None:
            # Default to sample data file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_file_path = os.path.join(current_dir, "sample-data", "dhf_data.yaml")

        self.data_file_path = data_file_path
        self.analyses_dir = analyses_dir  # Custom analyses directory path
        self._data = None
        self._last_modified = None

    def load_data(self, force_reload: bool = False) -> Dict[str, Any]:
        """Load DHF data from YAML file.

        Args:
            force_reload: If True, bypass cache and reload from disk
        """
        # Check if file has been modified
        try:
            current_mtime = os.path.getmtime(self.data_file_path)
            if self._last_modified is not None and current_mtime > self._last_modified:
                force_reload = True
        except OSError:
            # File doesn't exist or cannot be accessed; continue without forcing reload
            pass

        if self._data is None or force_reload:
            try:
                with open(self.data_file_path, "r", encoding="utf-8") as file:
                    self._data = yaml.safe_load(file)
                    self._last_modified = os.path.getmtime(self.data_file_path)

                # Check if migration is needed
                if needs_migration(self._data):
                    logger.info(f"Schema migration required for {self.data_file_path}")
                    self._data = migrate_to_latest(self._data)
                    # Save the migrated data
                    logger.info("Saving migrated data to disk")
                    self.save_data(self._data)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"DHF data file not found: {self.data_file_path}"
                )
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML format: {e}")

        return self._data

    def save_data(self, data: Dict[str, Any]) -> None:
        """Save DHF data to YAML file."""
        from app.schema_migrations import CURRENT_SCHEMA_VERSION

        try:
            # Ensure metadata section exists
            if "metadata" not in data:
                data["metadata"] = {}

            # Always write current schema version
            data["metadata"]["schema_version"] = CURRENT_SCHEMA_VERSION

            with open(self.data_file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file, default_flow_style=False, sort_keys=False)
            self._data = data  # Update cached data
            self._last_modified = os.path.getmtime(self.data_file_path)
        except Exception as e:
            raise ValueError(f"Failed to save data: {e}")

    def invalidate_cache(self) -> None:
        """Invalidate the cached data, forcing a reload on next access."""
        self._data = None
        self._last_modified = None

    def get_user_needs(self) -> Dict[str, Any]:
        """Get all user needs."""
        data = self.load_data()
        return data.get("user_needs", {})

    def get_risks(self) -> Dict[str, Any]:
        """Get all risks organized by groups."""
        data = self.load_data()
        risks_data = data.get("risks", {})

        # Return the grouped structure directly for the template
        return risks_data

    def get_risks_flat(self) -> Dict[str, Any]:
        """Get all risks in a flat structure for backward compatibility."""
        data = self.load_data()
        risks_data = data.get("risks", {})

        # If risks are already in the old flat format, return them
        if not any(
            isinstance(group, dict) and "risks" in group
            for group in risks_data.values()
        ):
            return risks_data

        # If risks are in the new grouped format, flatten them for backward compatibility
        flattened_risks = {}
        for group_key, group_data in risks_data.items():
            if isinstance(group_data, dict) and "risks" in group_data:
                for risk_id, risk_data in group_data["risks"].items():
                    flattened_risks[risk_id] = risk_data
            else:
                # Handle legacy flat structure
                flattened_risks[group_key] = group_data

        return flattened_risks

    def get_product_requirements(self) -> Dict[str, Any]:
        """Get all product requirements organized by groups."""
        data = self.load_data()
        return data.get("product_requirements", {})

    def get_software_specifications(self) -> Dict[str, Any]:
        """Get all software specifications organized by groups."""
        data = self.load_data()
        return data.get("software_specifications", {})

    def get_hardware_specifications(self) -> Dict[str, Any]:
        """Get all hardware specifications organized by groups."""
        data = self.load_data()
        return data.get("hardware_specifications", {})

    def get_mitigation_links(self) -> Dict[str, Any]:
        """Get all mitigation links."""
        data = self.load_data()
        return data.get("mitigation_links", {})

    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get any item by its ID across all categories."""
        data = self.load_data()

        # Search in user needs (handle both flat and nested structures)
        user_needs_data = data.get("user_needs", {})
        for group_key, group_data in user_needs_data.items():
            if isinstance(group_data, dict) and "needs" in group_data:
                # New nested structure
                if item_id in group_data["needs"]:
                    return group_data["needs"][item_id]
            else:
                # Legacy flat structure
                if group_key == item_id:
                    return group_data

        # Search in risks (handle both grouped and flat structures)
        risks_data = data.get("risks", {})
        for group_key, group_data in risks_data.items():
            if isinstance(group_data, dict) and "risks" in group_data:
                # New grouped structure
                if item_id in group_data["risks"]:
                    return group_data["risks"][item_id]
            else:
                # Legacy flat structure
                if group_key == item_id:
                    return group_data

        # Search in product requirements (handle both 2-level and 3-level structures)
        for group in data.get("product_requirements", {}).values():
            if "requirements" in group:
                # Check if this is a 3-level structure (nested requirements)
                if any(
                    isinstance(req, dict) and "requirements" in req
                    for req in group["requirements"].values()
                ):
                    # 3-level structure: search in nested requirements
                    for sub_group in group["requirements"].values():
                        if (
                            "requirements" in sub_group
                            and item_id in sub_group["requirements"]
                        ):
                            return sub_group["requirements"][item_id]
                else:
                    # 2-level structure: search in direct requirements
                    if item_id in group["requirements"]:
                        return group["requirements"][item_id]

        # Search in software specifications
        for group in data.get("software_specifications", {}).values():
            if "specifications" in group:
                if item_id in group["specifications"]:
                    return group["specifications"][item_id]

        # Search in hardware specifications
        for group in data.get("hardware_specifications", {}).values():
            if "specifications" in group:
                if item_id in group["specifications"]:
                    return group["specifications"][item_id]

        return None

    def update_item(self, item_id: str, updated_item: Dict[str, Any]) -> bool:
        """Update an item by its ID."""
        data = self.load_data()

        # Update in user needs (handle both flat and nested structures)
        user_needs_data = data.get("user_needs", {})
        for group_key, group_data in user_needs_data.items():
            if isinstance(group_data, dict) and "needs" in group_data:
                # New nested structure
                if item_id in group_data["needs"]:
                    data["user_needs"][group_key]["needs"][item_id].update(updated_item)
                    self.save_data(data)
                    return True
            else:
                # Legacy flat structure
                if group_key == item_id:
                    data["user_needs"][group_key].update(updated_item)
                    self.save_data(data)
                    return True

        # Update in risks (handle both grouped and flat structures)
        risks_data = data.get("risks", {})
        for group_key, group_data in risks_data.items():
            if isinstance(group_data, dict) and "risks" in group_data:
                # New grouped structure
                if item_id in group_data["risks"]:
                    data["risks"][group_key]["risks"][item_id].update(updated_item)
                    self.save_data(data)
                    return True
            else:
                # Legacy flat structure
                if group_key == item_id:
                    data["risks"][group_key].update(updated_item)
                    self.save_data(data)
                    return True

        # Update in product requirements (handle both 2-level and 3-level structures)
        for group_key, group in data.get("product_requirements", {}).items():
            if "requirements" in group:
                # Check if this is a 3-level structure (nested requirements)
                if any(
                    isinstance(req, dict) and "requirements" in req
                    for req in group["requirements"].values()
                ):
                    # 3-level structure: search in nested requirements
                    for sub_key, sub_group in group["requirements"].items():
                        if (
                            "requirements" in sub_group
                            and item_id in sub_group["requirements"]
                        ):
                            data["product_requirements"][group_key]["requirements"][
                                sub_key
                            ]["requirements"][item_id].update(updated_item)
                            self.save_data(data)
                            return True
                else:
                    # 2-level structure: search in direct requirements
                    if item_id in group["requirements"]:
                        data["product_requirements"][group_key]["requirements"][
                            item_id
                        ].update(updated_item)
                        self.save_data(data)
                        return True

        # Update in software specifications
        for group_key, group in data.get("software_specifications", {}).items():
            if "specifications" in group and item_id in group["specifications"]:
                data["software_specifications"][group_key]["specifications"][
                    item_id
                ].update(updated_item)
                self.save_data(data)
                return True

        # Update in hardware specifications
        for group_key, group in data.get("hardware_specifications", {}).items():
            if "specifications" in group and item_id in group["specifications"]:
                data["hardware_specifications"][group_key]["specifications"][
                    item_id
                ].update(updated_item)
                self.save_data(data)
                return True

        return False

    def get_linkable_items(self) -> Dict[str, List[Dict[str, str]]]:
        """Get all items that can be linked to (for dropdowns)."""
        data = self.load_data()
        linkable = {"user_needs": [], "risks": [], "product_requirements": []}

        # Add user needs (handle both flat and nested structures)
        user_needs_data = data.get("user_needs", {})
        for group_key, group_data in user_needs_data.items():
            if isinstance(group_data, dict) and "needs" in group_data:
                # New nested structure
                for item_id, item in group_data["needs"].items():
                    linkable["user_needs"].append(
                        {"id": item_id, "title": item.get("title", "Untitled")}
                    )
            else:
                # Legacy flat structure
                linkable["user_needs"].append(
                    {"id": group_key, "title": group_data.get("title", "Untitled")}
                )

        # Add risks (use flattened structure)
        for item_id, item in self.get_risks_flat().items():
            linkable["risks"].append(
                {"id": item_id, "title": item.get("title", "Untitled")}
            )

        # Add product requirements (handle both 2-level and 3-level structures)
        for group in data.get("product_requirements", {}).values():
            if "requirements" in group:
                # Check if this is a 3-level structure (nested requirements)
                if any(
                    isinstance(req, dict) and "requirements" in req
                    for req in group["requirements"].values()
                ):
                    # 3-level structure: add nested requirements
                    for sub_group in group["requirements"].values():
                        if "requirements" in sub_group:
                            for item_id, item in sub_group["requirements"].items():
                                linkable["product_requirements"].append(
                                    {
                                        "id": item_id,
                                        "title": item.get("title", "Untitled"),
                                    }
                                )
                else:
                    # 2-level structure: add direct requirements
                    for item_id, item in group["requirements"].items():
                        linkable["product_requirements"].append(
                            {"id": item_id, "title": item.get("title", "Untitled")}
                        )

        return linkable

    def update_folder_name(
        self, group_type: str, group_key: str, new_name: str
    ) -> bool:
        """Update a folder/group name."""
        data = self.load_data()

        # Update in the appropriate group type
        if group_type in data:
            if group_key in data[group_type]:
                data[group_type][group_key]["group_name"] = new_name
                self.save_data(data)
                return True

        return False

    def get_configuration(self) -> Dict[str, Any]:
        """Get configuration settings including dropdown options."""
        data = self.load_data()

        # Get mapping configuration
        config = data.get("configuration", {})
        severity_mapping = config.get("severity_mapping", {})
        probability_mapping = config.get(
            "probability_mapping", {}
        )  # Legacy (deprecated)
        probability_harm_mapping = config.get("probability_harm_mapping", {})

        # Default mappings if none found
        if not severity_mapping:
            severity_mapping = {
                "S1": {
                    "name": "Low",
                    "description": "Minor impact, low risk to patient safety",
                },
                "S2": {
                    "name": "Medium",
                    "description": "Moderate impact, potential for patient harm",
                },
                "S3": {
                    "name": "High",
                    "description": "Significant impact, serious risk to patient safety",
                },
            }

        if not probability_mapping:
            probability_mapping = {
                "P1": {
                    "name": "Low",
                    "description": "Unlikely to occur under normal conditions",
                },
                "P2": {
                    "name": "Medium",
                    "description": "May occur occasionally during normal use",
                },
                "P3": {
                    "name": "High",
                    "description": "Likely to occur frequently during normal use",
                },
            }

        if not probability_harm_mapping:
            probability_harm_mapping = {
                "PH1": {
                    "name": "Low",
                    "description": "Unlikely to cause harm if it occurs",
                },
                "PH2": {"name": "Medium", "description": "May cause harm if it occurs"},
                "PH3": {
                    "name": "High",
                    "description": "Likely to cause harm if it occurs",
                },
            }

        # Find which IDs are currently in use
        severity_ids_in_use = set()
        probability_ids_in_use = set()  # Legacy (deprecated)
        probability_harm_ids_in_use = set()

        for group in data.get("risks", {}).values():
            if isinstance(group, dict) and "risks" in group:
                # New grouped structure
                for risk in group["risks"].values():
                    if "severity" in risk:
                        severity_ids_in_use.add(risk["severity"])
                    if "probability" in risk:  # Legacy
                        probability_ids_in_use.add(risk["probability"])
                    if "probability_harm" in risk:
                        probability_harm_ids_in_use.add(risk["probability_harm"])
            elif isinstance(group, dict):
                # Legacy flat structure
                if "severity" in group:
                    severity_ids_in_use.add(group["severity"])
                if "probability" in group:  # Legacy
                    probability_ids_in_use.add(group["probability"])
                if "probability_harm" in group:
                    probability_harm_ids_in_use.add(group["probability_harm"])

        return {
            "severity_mapping": severity_mapping,
            "probability_mapping": probability_mapping,  # Legacy (deprecated)
            "probability_harm_mapping": probability_harm_mapping,
            "severity_ids_in_use": list(severity_ids_in_use),
            "probability_ids_in_use": list(
                probability_ids_in_use
            ),  # Legacy (deprecated)
            "probability_harm_ids_in_use": list(probability_harm_ids_in_use),
        }

    def add_config_option(
        self, config_type: str, name: str, description: str = ""
    ) -> str:
        """Add a new option to a configuration dropdown. Returns the new ID."""
        data = self.load_data()

        # Ensure configuration section exists
        if "configuration" not in data:
            data["configuration"] = {}

        mapping_key = f"{config_type}_mapping"
        if mapping_key not in data["configuration"]:
            data["configuration"][mapping_key] = {}

        # Find next available ID
        prefix = "S" if config_type == "severity" else "P"
        existing_ids = [
            k for k in data["configuration"][mapping_key].keys() if k.startswith(prefix)
        ]

        # Extract numbers and find the next one
        numbers = []
        for id_key in existing_ids:
            try:
                numbers.append(int(id_key[1:]))
            except ValueError:
                continue

        next_num = max(numbers) + 1 if numbers else 1
        new_id = f"{prefix}{next_num}"

        # Add the new mapping
        data["configuration"][mapping_key][new_id] = {
            "name": name,
            "description": description or f"{name} option for {config_type}",
        }

        self.save_data(data)
        return new_id

    def remove_config_option(self, config_type: str, option_id: str) -> bool:
        """Remove an option from a configuration dropdown."""
        data = self.load_data()

        # Check if the ID is being used by any risks
        for risk in data.get("risks", {}).values():
            if config_type == "severity" and risk.get("severity") == option_id:
                return False  # Cannot remove option that's in use
            if config_type == "probability" and risk.get("probability") == option_id:
                return False  # Cannot remove option that's in use

        # Remove from configuration mapping
        mapping_key = f"{config_type}_mapping"
        if (
            "configuration" in data
            and mapping_key in data["configuration"]
            and option_id in data["configuration"][mapping_key]
        ):
            del data["configuration"][mapping_key][option_id]
            self.save_data(data)
            return True

        return False

    def update_config_option(
        self, config_type: str, option_id: str, name: str, description: str = ""
    ) -> bool:
        """Update the name and description of a configuration option."""
        data = self.load_data()

        mapping_key = f"{config_type}_mapping"
        if (
            "configuration" in data
            and mapping_key in data["configuration"]
            and option_id in data["configuration"][mapping_key]
        ):
            data["configuration"][mapping_key][option_id]["name"] = name
            if description:
                data["configuration"][mapping_key][option_id][
                    "description"
                ] = description

            self.save_data(data)
            return True

        return False

    def get_severity_name(self, severity_id: str) -> str:
        """Get the display name for a severity ID."""
        config = self.get_configuration()
        return config["severity_mapping"].get(severity_id, {}).get("name", severity_id)

    def get_probability_name(self, probability_id: str) -> str:
        """Get the display name for a probability ID."""
        config = self.get_configuration()
        return (
            config["probability_mapping"]
            .get(probability_id, {})
            .get("name", probability_id)
        )

    def get_probability_occurrence_name(self, probability_occurrence_id: str) -> str:
        """Get the display name for a probability occurrence ID."""
        config = self.get_configuration()
        return (
            config["probability_occurrence_mapping"]
            .get(probability_occurrence_id, {})
            .get("name", probability_occurrence_id)
        )

    def get_probability_harm_name(self, probability_harm_id: str) -> str:
        """Get the display name for a probability harm ID."""
        config = self.get_configuration()
        return (
            config["probability_harm_mapping"]
            .get(probability_harm_id, {})
            .get("name", probability_harm_id)
        )

    def calculate_rbm_score(self, probability_harm_id: str, severity_id: str) -> int:
        """Calculate RBM score: Severity × Probability of Harm.

        This follows ISO 14971:2019 risk scoring using a two-factor model.

        Args:
            probability_harm_id: Probability of harm ID (PH1, PH2, PH3, etc.)
            severity_id: Severity ID (S1, S2, S3, etc.)

        Returns:
            The calculated risk score (S × PH)
        """
        # Map IDs to numeric values
        ph_value = (
            int(probability_harm_id.replace("PH", ""))
            if probability_harm_id.startswith("PH")
            else 1
        )
        s_value = (
            int(severity_id.replace("S", "")) if severity_id.startswith("S") else 1
        )

        return s_value * ph_value

    # Analyses Management Methods

    def get_analyses_directory(self) -> str:
        """Get the analyses directory path.

        If analyses_dir was provided during initialization, use that.
        Otherwise, defaults to internal sample data (sample-data/analyses).
        """
        # If a custom analyses directory was specified, use it
        if self.analyses_dir:
            return self.analyses_dir

        # Default to sample-data/analyses
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(current_dir, "sample-data", "analyses")

    def get_analyses(self) -> List[Dict[str, Any]]:
        """Get list of all analyses (FMEA and FTA)."""
        analyses_dir = self.get_analyses_directory()
        analyses = []

        if not os.path.exists(analyses_dir):
            return analyses

        for filename in os.listdir(analyses_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                try:
                    filepath = os.path.join(analyses_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as file:
                        analysis_data = yaml.safe_load(file)
                        if analysis_data and isinstance(analysis_data, dict):
                            analyses.append(
                                {
                                    "id": analysis_data.get("id", filename),
                                    "title": analysis_data.get("title", filename),
                                    "type": analysis_data.get("type", "unknown"),
                                    "description": analysis_data.get("description", ""),
                                    "status": analysis_data.get("status", "active"),
                                    "last_modified": analysis_data.get(
                                        "last_modified", ""
                                    ),
                                    "filename": filename,
                                }
                            )
                except Exception as e:
                    print(f"Error loading analysis {filename}: {e}")
                    continue

        # Sort by ID
        analyses.sort(key=lambda x: x["id"])
        return analyses

    def load_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific analysis by ID."""
        analyses_dir = self.get_analyses_directory()

        if not os.path.exists(analyses_dir):
            return None

        # Find the file with this ID
        for filename in os.listdir(analyses_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                try:
                    filepath = os.path.join(analyses_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as file:
                        analysis_data = yaml.safe_load(file)
                        if analysis_data and analysis_data.get("id") == analysis_id:
                            analysis_data["filename"] = filename
                            return analysis_data
                except Exception as e:
                    print(f"Error loading analysis {filename}: {e}")
                    continue

        return None

    def save_analysis(self, analysis_id: str, analysis_data: Dict[str, Any]) -> bool:
        """Save an analysis to its file."""
        import re

        analyses_dir = self.get_analyses_directory()

        if not os.path.exists(analyses_dir):
            os.makedirs(analyses_dir, exist_ok=True)

        # Determine filename
        filename = analysis_data.get("filename")
        if not filename:
            # Generate filename from ID
            filename = f"{analysis_id.lower()}.yaml"

        # Security: Validate filename to prevent path traversal
        # Use basename to strip any path components
        safe_filename = os.path.basename(filename)

        # Only allow safe characters: alphanumeric, underscore, hyphen, and dots
        # Must end with .yaml or .yml
        if not re.match(r"^[a-zA-Z0-9_\-]+\.(yaml|yml)$", safe_filename):
            print(
                f"Error: Invalid filename '{safe_filename}' for analysis {analysis_id}"
            )
            return False

        filepath = os.path.join(analyses_dir, safe_filename)

        # Security: Verify the resolved path is within analyses_dir
        real_path = os.path.realpath(filepath)
        real_dir = os.path.realpath(analyses_dir)
        if not real_path.startswith(real_dir + os.sep):
            print(f"Error: Path traversal attempt detected for analysis {analysis_id}")
            return False

        try:
            # Remove filename from data before saving
            save_data = {k: v for k, v in analysis_data.items() if k != "filename"}

            with open(filepath, "w", encoding="utf-8") as file:
                yaml.safe_dump(
                    save_data, file, default_flow_style=False, sort_keys=False
                )
            return True
        except Exception as e:
            print(f"Error saving analysis {analysis_id}: {e}")
            return False

    def delete_analysis(self, analysis_id: str) -> bool:
        """Delete an analysis file."""
        analyses_dir = self.get_analyses_directory()

        if not os.path.exists(analyses_dir):
            return False

        # Find and delete the file
        for filename in os.listdir(analyses_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                try:
                    filepath = os.path.join(analyses_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as file:
                        analysis_data = yaml.safe_load(file)
                        if analysis_data and analysis_data.get("id") == analysis_id:
                            os.remove(filepath)
                            return True
                except Exception as e:
                    print(f"Error deleting analysis {filename}: {e}")
                    continue

        return False

    def create_analysis(
        self, analysis_type: str, title: str, description: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Create a new analysis with auto-generated ID."""
        # Get existing analyses to determine next ID
        existing_analyses = self.get_analyses()
        prefix = "FM" if analysis_type == "fmea" else "FT"

        # Find highest ID number
        max_num = 0
        for analysis in existing_analyses:
            if analysis["id"].startswith(prefix):
                try:
                    num = int(analysis["id"][2:])
                    max_num = max(max_num, num)
                except ValueError:
                    continue

        # Generate new ID
        new_id = f"{prefix}{max_num + 1:04d}"

        # Create analysis structure
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d")

        if analysis_type == "fmea":
            analysis_data = {
                "id": new_id,
                "title": title,
                "type": "fmea",
                "description": description,
                "created_date": now,
                "last_modified": now,
                "author": "User",
                "status": "active",
                "rows": [],
            }
        else:  # FTA
            analysis_data = {
                "id": new_id,
                "title": title,
                "type": "fta",
                "description": description,
                "created_date": now,
                "last_modified": now,
                "author": "User",
                "status": "active",
                "top_event": {
                    "id": f"{new_id}-TE",
                    "description": "Top event description",
                    "gate_type": "OR",
                    "severity": 5,
                    "linked_risks": [],
                },
                "intermediate_events": [],
                "basic_events": [],
            }

        # Save the new analysis
        if self.save_analysis(new_id, analysis_data):
            return analysis_data

        return None

    def sync_analysis_to_dhf(self, analysis_id: str) -> Dict[str, Any]:
        """
        Sync an analysis to DHF, creating or updating risk and specification entities.
        Returns a dict with preview of changes to be made.
        """
        analysis = self.load_analysis(analysis_id)
        if not analysis:
            return {"error": "Analysis not found"}

        dhf_data = self.load_data()
        changes = {
            "risks_to_create": [],
            "risks_to_update": [],
            "specs_to_create": [],
            "specs_to_link": [],
        }

        if analysis["type"] == "fmea":
            changes = self._sync_fmea_to_dhf(analysis, dhf_data, changes)
        elif analysis["type"] == "fta":
            changes = self._sync_fta_to_dhf(analysis, dhf_data, changes)

        return changes

    def _sync_fmea_to_dhf(
        self,
        analysis: Dict[str, Any],
        dhf_data: Dict[str, Any],
        changes: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Sync FMEA to DHF data."""
        # For each FMEA row, check if controls/actions need to be created or linked
        for row in analysis.get("rows", []):
            # Check current controls
            for control_ref in row.get("current_controls", []):
                if isinstance(control_ref, str):
                    # Check if it's an existing spec or needs to be created
                    existing_spec = self.get_item_by_id(control_ref)
                    if existing_spec:
                        changes["specs_to_link"].append(
                            {
                                "spec_id": control_ref,
                                "fmea_row": row["id"],
                                "action": "Link existing control",
                            }
                        )
                    else:
                        # Need to create new spec
                        changes["specs_to_create"].append(
                            {
                                "spec_id": control_ref,
                                "title": f"Control for {row['failure_mode']}",
                                "description": f"Mitigation control from FMEA {analysis['id']}",
                                "fmea_row": row["id"],
                            }
                        )

            # Check recommended actions
            for action in row.get("recommended_actions", []):
                if (
                    isinstance(action, str)
                    and action.startswith("SS")
                    or action.startswith("HS")
                ):
                    existing_spec = self.get_item_by_id(action)
                    if not existing_spec:
                        changes["specs_to_create"].append(
                            {
                                "spec_id": action,
                                "title": action,
                                "description": f"Action from FMEA {analysis['id']}: {action}",
                                "fmea_row": row["id"],
                            }
                        )

        return changes

    def _sync_fta_to_dhf(
        self,
        analysis: Dict[str, Any],
        dhf_data: Dict[str, Any],
        changes: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Sync FTA to DHF data."""
        # Check top event - may need to create or link risk
        top_event = analysis.get("top_event", {})
        linked_risks = top_event.get("linked_risks", [])

        if not linked_risks:
            # Create new risk for top event
            changes["risks_to_create"].append(
                {
                    "title": top_event.get("description", "Unknown hazard"),
                    "severity": top_event.get("severity", 5),
                    "source": f"FTA {analysis['id']} top event",
                }
            )

        # Check basic events for mitigations
        for event in analysis.get("basic_events", []):
            for mitigation in event.get("mitigations", []):
                if isinstance(mitigation, str):
                    # Check if it's an existing spec
                    existing_spec = self.get_item_by_id(mitigation)
                    if existing_spec:
                        changes["specs_to_link"].append(
                            {
                                "spec_id": mitigation,
                                "fta_event": event["id"],
                                "action": "Link existing mitigation",
                            }
                        )
                    else:
                        # May need to create if it looks like an ID
                        if mitigation.startswith("SS") or mitigation.startswith("HS"):
                            changes["specs_to_create"].append(
                                {
                                    "spec_id": mitigation,
                                    "title": mitigation,
                                    "description": event.get(
                                        "mitigation_description", ""
                                    ),
                                    "fta_event": event["id"],
                                }
                            )

        return changes

    def apply_dhf_sync(self, analysis_id: str, changes: Dict[str, Any]) -> bool:
        """Apply the DHF sync changes."""
        dhf_data = self.load_data()

        # Ensure risks section exists
        if "risks" not in dhf_data:
            dhf_data["risks"] = {}

        # Create a group for analysis-derived risks if needed
        analysis_risk_group_key = "analysis_derived"
        if analysis_risk_group_key not in dhf_data["risks"]:
            dhf_data["risks"][analysis_risk_group_key] = {
                "group_name": "Analysis-Derived Risks",
                "description": "Risks identified through FMEA/FTA analyses",
                "risks": {},
            }

        # Create new risks
        for risk_data in changes.get("risks_to_create", []):
            # Generate new risk ID
            existing_risk_ids = []
            for group in dhf_data["risks"].values():
                if isinstance(group, dict) and "risks" in group:
                    existing_risk_ids.extend(group["risks"].keys())

            max_num = 0
            for risk_id in existing_risk_ids:
                if risk_id.startswith("RK"):
                    try:
                        num = int(risk_id[2:])
                        max_num = max(max_num, num)
                    except ValueError:
                        continue

            new_risk_id = f"RK{max_num + 1:04d}"

            dhf_data["risks"][analysis_risk_group_key]["risks"][new_risk_id] = {
                "title": risk_data["title"],
                "severity": f"S{risk_data['severity']}",
                "probability_occurrence": "PO2",
                "probability_harm": "PH2",
                "harm": risk_data.get("source", "From analysis"),
                "justification": f"Identified through {analysis_id}",
                "benefits_outweigh_risk": False,
                "cannot_be_reduced_further": False,
            }

        # Create new specifications
        # Ensure software_specifications section exists
        if "software_specifications" not in dhf_data:
            dhf_data["software_specifications"] = {}

        analysis_spec_group_key = "analysis_derived"
        if analysis_spec_group_key not in dhf_data["software_specifications"]:
            dhf_data["software_specifications"][analysis_spec_group_key] = {
                "group_name": "Analysis-Derived Specifications",
                "description": "Specifications from FMEA/FTA analyses",
                "specifications": {},
            }

        for spec_data in changes.get("specs_to_create", []):
            spec_id = spec_data.get("spec_id")

            # If spec_id doesn't start with SS, generate one
            if not spec_id or not spec_id.startswith("SS"):
                # Generate new spec ID
                existing_spec_ids = []
                for group in dhf_data["software_specifications"].values():
                    if isinstance(group, dict) and "specifications" in group:
                        existing_spec_ids.extend(group["specifications"].keys())

                max_num = 0
                for s_id in existing_spec_ids:
                    if s_id.startswith("SS"):
                        try:
                            num = int(s_id[2:])
                            max_num = max(max_num, num)
                        except ValueError:
                            continue

                spec_id = f"SS{max_num + 1:04d}"

            dhf_data["software_specifications"][analysis_spec_group_key][
                "specifications"
            ][spec_id] = {
                "title": spec_data["title"],
                "description": spec_data["description"],
                "linked_product_requirements": [],
                "verification_method": "Analysis",
            }

        # Save updated DHF data
        self.save_data(dhf_data)
        return True
