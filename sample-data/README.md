# Sample Data Directory

This directory contains sample data files for testing Pocket DHF functionality.

## Data Structure Schema

The `dhf_data.yaml` file follows this schema:

### Top Level Structure
- `metadata`: Project information and versioning
- `user_needs`: Collection of user requirements
- `risks`: Risk assessment data
- `product_requirements`: High-level requirements organized in groups
- `software_specifications`: Detailed software requirements organized in groups
- `hardware_specifications`: Detailed hardware requirements organized in groups

### User Needs
Each user need contains:
- `id`: Unique identifier (e.g., "UN001")
- `title`: Brief descriptive title
- `description`: Detailed description of the user need

### Risks
Each risk contains:
- `id`: Unique identifier (e.g., "R001")
- `title`: Brief risk title
- `description`: Detailed risk description
- `severity`: Risk severity level ("Low", "Medium", "High")
- `probability`: Probability of occurrence ("Low", "Medium", "High")

### Product Requirements
Organized in groups with each group containing:
- `group_name`: Display name for the requirement group
- `description`: Description of the requirement group
- `requirements`: Dictionary of individual requirements

Each requirement contains:
- `id`: Unique identifier (e.g., "PR001")
- `title`: Brief requirement title
- `description`: Detailed requirement description
- `linked_user_needs`: Array of user need IDs this requirement addresses
- `linked_risks`: Array of risk IDs this requirement mitigates

### Software Specifications
Organized in groups with each group containing:
- `group_name`: Display name for the specification group
- `description`: Description of the specification group
- `specifications`: Dictionary of individual specifications

Each specification contains:
- `id`: Unique identifier (e.g., "SS001")
- `title`: Brief specification title
- `description`: Detailed technical specification
- `linked_product_requirements`: Array of product requirement IDs this specification implements

### Hardware Specifications
Same structure as software specifications but for hardware components:
- `id`: Unique identifier (e.g., "HS001")
- `title`: Brief specification title
- `description`: Detailed technical specification
- `linked_product_requirements`: Array of product requirement IDs this specification implements

## Sample Data Content

The sample data represents a continuous glucose monitoring (CGM) medical device with:
- 5 user needs covering glucose monitoring, trend analysis, wearability, sensor longevity, and smartphone integration
- 5 risks covering measurement accuracy, hypoglycemia detection, sensor adhesion, skin reactions, and data privacy
- 7 product requirements organized in 3 groups (glucose monitoring, data management, physical design)
- 6 software specifications organized in 3 groups (glucose processing, data systems, sensor management)
- 10 hardware specifications organized in 5 groups (glucose sensing, processing, power, wearable interface, connectivity)

## Relationships

The data structure maintains traceability relationships:
- Product Requirements → User Needs & Risks
- Software Specifications → Product Requirements
- Hardware Specifications → Product Requirements

This allows for complete traceability from user needs through to implementation specifications.
