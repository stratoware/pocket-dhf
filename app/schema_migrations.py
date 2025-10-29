# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Schema migration system for DHF YAML data files.

This module provides version migration capabilities to ensure backward
compatibility when the DHF YAML schema changes.
"""

import logging
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)

# Schema version constants
SCHEMA_VERSION_1_0 = "1.0"
SCHEMA_VERSION_2_0 = "2.0"
CURRENT_SCHEMA_VERSION = SCHEMA_VERSION_2_0


# Migration registry: maps (from_version, to_version) -> migration function
MIGRATION_REGISTRY: Dict[tuple, Callable] = {}


def register_migration(from_version: str, to_version: str):
    """Decorator to register a migration function."""
    def decorator(func: Callable):
        MIGRATION_REGISTRY[(from_version, to_version)] = func
        return func
    return decorator


@register_migration(SCHEMA_VERSION_1_0, SCHEMA_VERSION_2_0)
def migrate_v1_to_v2(data: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate from schema v1.0 to v2.0.
    
    Changes in v2.0:
    - Remove probability_occurrence_mapping from configuration
    - Remove probability_occurrence field from all risks
    - Risk scoring changes from S × PO × PH to S × PH
    
    Args:
        data: The DHF data dictionary in v1.0 format
        
    Returns:
        The migrated data dictionary in v2.0 format
    """
    logger.info("Migrating DHF data from schema v1.0 to v2.0")
    
    # Update metadata to reflect new schema version
    if "metadata" not in data:
        data["metadata"] = {}
    data["metadata"]["schema_version"] = SCHEMA_VERSION_2_0
    
    # Remove probability_occurrence_mapping from configuration
    if "configuration" in data and "probability_occurrence_mapping" in data["configuration"]:
        logger.info("Removing probability_occurrence_mapping from configuration")
        del data["configuration"]["probability_occurrence_mapping"]
    
    # Remove probability_occurrence from all risks
    if "risks" in data:
        risks_migrated = 0
        for group_key, group_data in data["risks"].items():
            if isinstance(group_data, dict) and "risks" in group_data:
                # New grouped structure
                for risk_id, risk in group_data["risks"].items():
                    if "probability_occurrence" in risk:
                        logger.debug(f"Removing probability_occurrence from risk {risk_id}")
                        del risk["probability_occurrence"]
                        risks_migrated += 1
            elif isinstance(group_data, dict) and "probability_occurrence" in group_data:
                # Legacy flat structure
                logger.debug(f"Removing probability_occurrence from risk {group_key}")
                del group_data["probability_occurrence"]
                risks_migrated += 1
        
        logger.info(f"Migrated {risks_migrated} risk entries")
    
    logger.info("Migration from v1.0 to v2.0 completed successfully")
    return data


def get_schema_version(data: Dict[str, Any]) -> str:
    """Extract the schema version from DHF data.
    
    Args:
        data: The DHF data dictionary
        
    Returns:
        The schema version string (e.g., "1.0", "2.0")
    """
    if "metadata" in data and "schema_version" in data["metadata"]:
        return data["metadata"]["schema_version"]
    
    # If no schema_version field, check for v1.0 indicators
    if "configuration" in data and "probability_occurrence_mapping" in data["configuration"]:
        return SCHEMA_VERSION_1_0
    
    # Default to current version if we can't determine
    return CURRENT_SCHEMA_VERSION


def migrate_to_latest(data: Dict[str, Any], from_version: str = None) -> Dict[str, Any]:
    """Migrate data from any version to the current schema version.
    
    This function can handle multi-step migrations (e.g., v1.0 -> v1.5 -> v2.0).
    
    Args:
        data: The DHF data dictionary to migrate
        from_version: The starting version (if None, will be auto-detected)
        
    Returns:
        The migrated data dictionary at the current schema version
        
    Raises:
        ValueError: If migration path is not available
    """
    if from_version is None:
        from_version = get_schema_version(data)
    
    # If already at current version, return as-is
    if from_version == CURRENT_SCHEMA_VERSION:
        logger.debug(f"Data is already at current schema version {CURRENT_SCHEMA_VERSION}")
        return data
    
    # Find migration path (currently only supporting single-step migrations)
    migration_key = (from_version, CURRENT_SCHEMA_VERSION)
    
    if migration_key not in MIGRATION_REGISTRY:
        available_migrations = list(MIGRATION_REGISTRY.keys())
        raise ValueError(
            f"No migration available from {from_version} to {CURRENT_SCHEMA_VERSION}. "
            f"Available migrations: {available_migrations}"
        )
    
    # Execute migration
    migration_func = MIGRATION_REGISTRY[migration_key]
    logger.info(f"Migrating data from {from_version} to {CURRENT_SCHEMA_VERSION}")
    migrated_data = migration_func(data)
    
    # Verify migration was successful
    new_version = get_schema_version(migrated_data)
    if new_version != CURRENT_SCHEMA_VERSION:
        raise ValueError(
            f"Migration failed: expected version {CURRENT_SCHEMA_VERSION}, "
            f"but got {new_version}"
        )
    
    return migrated_data


def needs_migration(data: Dict[str, Any]) -> bool:
    """Check if data needs migration to the current schema version.
    
    Args:
        data: The DHF data dictionary
        
    Returns:
        True if migration is needed, False otherwise
    """
    current_version = get_schema_version(data)
    return current_version != CURRENT_SCHEMA_VERSION

