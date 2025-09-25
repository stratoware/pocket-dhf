# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Data utilities for loading and managing DHF YAML data."""

import os
from typing import Any, Dict, List, Optional

import yaml


class DHFDataManager:
    """Manages loading and saving of DHF data from YAML files."""

    def __init__(self, data_file_path: str = None):
        """Initialize the data manager with a YAML file path."""
        if data_file_path is None:
            # Default to sample data file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_file_path = os.path.join(current_dir, "sample-data", "dhf_data.yaml")

        self.data_file_path = data_file_path
        self._data = None

    def load_data(self) -> Dict[str, Any]:
        """Load DHF data from YAML file."""
        if self._data is None:
            try:
                with open(self.data_file_path, "r", encoding="utf-8") as file:
                    self._data = yaml.safe_load(file)
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"DHF data file not found: {self.data_file_path}"
                )
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML format: {e}")

        return self._data

    def save_data(self, data: Dict[str, Any]) -> None:
        """Save DHF data to YAML file."""
        try:
            with open(self.data_file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file, default_flow_style=False, sort_keys=False)
            self._data = data  # Update cached data
        except Exception as e:
            raise ValueError(f"Failed to save data: {e}")

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
                if any(isinstance(req, dict) and "requirements" in req for req in group["requirements"].values()):
                    # 3-level structure: search in nested requirements
                    for sub_group in group["requirements"].values():
                        if "requirements" in sub_group and item_id in sub_group["requirements"]:
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
                if any(isinstance(req, dict) and "requirements" in req for req in group["requirements"].values()):
                    # 3-level structure: search in nested requirements
                    for sub_key, sub_group in group["requirements"].items():
                        if "requirements" in sub_group and item_id in sub_group["requirements"]:
                            data["product_requirements"][group_key]["requirements"][sub_key]["requirements"][item_id].update(
                                updated_item
                            )
                            self.save_data(data)
                            return True
                else:
                    # 2-level structure: search in direct requirements
                    if item_id in group["requirements"]:
                        data["product_requirements"][group_key]["requirements"][item_id].update(
                            updated_item
                        )
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
                if any(isinstance(req, dict) and "requirements" in req for req in group["requirements"].values()):
                    # 3-level structure: add nested requirements
                    for sub_group in group["requirements"].values():
                        if "requirements" in sub_group:
                            for item_id, item in sub_group["requirements"].items():
                                linkable["product_requirements"].append(
                                    {"id": item_id, "title": item.get("title", "Untitled")}
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
        probability_mapping = config.get("probability_mapping", {})  # Legacy
        probability_occurrence_mapping = config.get(
            "probability_occurrence_mapping", {}
        )
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

        if not probability_occurrence_mapping:
            probability_occurrence_mapping = {
                "PO1": {
                    "name": "Low",
                    "description": "Unlikely to occur under normal conditions",
                },
                "PO2": {
                    "name": "Medium",
                    "description": "May occur occasionally during normal use",
                },
                "PO3": {
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
        probability_ids_in_use = set()  # Legacy
        probability_occurrence_ids_in_use = set()
        probability_harm_ids_in_use = set()

        for risk in data.get("risks", {}).values():
            if "severity" in risk:
                severity_ids_in_use.add(risk["severity"])
            if "probability" in risk:  # Legacy
                probability_ids_in_use.add(risk["probability"])
            if "probability_occurrence" in risk:
                probability_occurrence_ids_in_use.add(risk["probability_occurrence"])
            if "probability_harm" in risk:
                probability_harm_ids_in_use.add(risk["probability_harm"])

        return {
            "severity_mapping": severity_mapping,
            "probability_mapping": probability_mapping,  # Legacy
            "probability_occurrence_mapping": probability_occurrence_mapping,
            "probability_harm_mapping": probability_harm_mapping,
            "severity_ids_in_use": list(severity_ids_in_use),
            "probability_ids_in_use": list(probability_ids_in_use),  # Legacy
            "probability_occurrence_ids_in_use": list(
                probability_occurrence_ids_in_use
            ),
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

    def calculate_rbm_score(
        self, probability_occurrence_id: str, probability_harm_id: str, severity_id: str
    ) -> int:
        """Calculate RBM score: Probability of Occurrence × Probability of Harm × Severity."""
        # Map IDs to numeric values (1, 2, 3)
        po_value = (
            int(probability_occurrence_id.replace("PO", ""))
            if probability_occurrence_id.startswith("PO")
            else 1
        )
        ph_value = (
            int(probability_harm_id.replace("PH", ""))
            if probability_harm_id.startswith("PH")
            else 1
        )
        s_value = (
            int(severity_id.replace("S", "")) if severity_id.startswith("S") else 1
        )

        return po_value * ph_value * s_value
