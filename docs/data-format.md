# Pocket DHF Data Format Guide

Complete reference for the YAML data format used by Pocket DHF.

## Table of Contents

- [Overview](#overview)
- [File Structure](#file-structure)
- [Metadata Section](#metadata-section)
- [Configuration Section](#configuration-section)
- [User Needs](#user-needs)
- [Product Requirements](#product-requirements)
- [Specifications](#specifications)
- [Risks](#risks)
- [Mitigation Links](#mitigation-links)
- [Validation and Best Practices](#validation-and-best-practices)

## Overview

Pocket DHF stores all Device History File data in a single YAML file. This format is:

- **Human-readable**: Easy to read and edit
- **Version-control friendly**: Works great with Git
- **Structured**: Enforces consistent organization
- **Portable**: Pure text, no proprietary formats

### Example File

See `sample-data/dhf_data.yaml` for a complete working example.

## File Structure

A DHF file contains these top-level sections:

```yaml
metadata:           # Project information
configuration:      # Risk scoring configuration
user_needs:         # User needs (UN###)
product_requirements:  # Product requirements (PR###)
software_specifications:  # Software specs (SW###)
hardware_specifications:  # Hardware specs (HW###)
risks:              # Risk assessments (R###)
mitigation_links:   # Links between risks and mitigations
```

## Metadata Section

Project-level information:

```yaml
metadata:
  project_name: "Your Device Name"
  device_type: "Device Classification"
  version: "1.0"
  created_date: "2025-01-15"
  last_modified: "2025-01-15"
  description: "Brief description of your device"
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project_name` | string | Yes | Name of your medical device |
| `device_type` | string | Yes | Device classification or type |
| `version` | string | Yes | DHF version number |
| `created_date` | string (YYYY-MM-DD) | Yes | Date DHF was created |
| `last_modified` | string (YYYY-MM-DD) | Yes | Last modification date |
| `description` | string | No | Brief project description |

## Configuration Section

Risk scoring configuration for ISO 14971 compliance.

### Severity Mapping

```yaml
configuration:
  severity_mapping:
    S1:
      name: "Negligible"
      description: "Inconvenience or temporary discomfort"
    S2:
      name: "Minor"
      description: "Minor injury requiring first aid"
    S3:
      name: "Serious"
      description: "Serious injury requiring medical intervention"
    S4:
      name: "Critical"
      description: "Life-threatening injury"
    S5:
      name: "Catastrophic"
      description: "Death"
```

Severity levels S1-S9 are configurable. Higher numbers = more severe.

### Probability Mappings

**Probability of Occurrence** (how likely the hazardous situation occurs):

```yaml
  probability_occurrence_mapping:
    PO1:
      name: "Remote"
      description: "<1% probability"
    PO2:
      name: "Occasional"
      description: "1-10% probability"
    PO3:
      name: "Frequent"
      description: ">10% probability"
```

**Probability of Harm** (if situation occurs, likelihood of harm):

```yaml
  probability_harm_mapping:
    PH1:
      name: "Unlikely"
      description: "Harm unlikely if hazard occurs"
    PH2:
      name: "Possible"
      description: "Harm possible if hazard occurs"
    PH3:
      name: "Probable"
      description: "Harm probable if hazard occurs"
```

### Risk-Benefit Matrix Calculation

```
RBM Score = Severity × Probability of Occurrence × Probability of Harm
```

The numeric values used are:
- Severity: S1=1, S2=2, ... S9=9
- PO: PO1=1, PO2=2, PO3=3
- PH: PH1=1, PH2=2, PH3=3

## User Needs

User needs describe what users want from the device.

```yaml
user_needs:
  UN001:
    id: UN001
    title: "Real-time Monitoring"
    description: "Users need continuous, real-time monitoring of vital signs with immediate alerts for abnormal values."
  UN002:
    id: UN002
    title: "Easy Data Export"
    description: "Users need to export historical data in standard formats for clinical review."
```

### Schema

```yaml
user_needs:
  <ID>:
    id: <ID>           # Must match the key (e.g., UN001)
    title: string      # Short descriptive title
    description: string  # Detailed description of the need
```

### Naming Convention

- Use format: `UN###` (e.g., UN001, UN002, ...)
- Number sequentially
- Use leading zeros for sorting (UN001, not UN1)

## Product Requirements

Product requirements define how the device will meet user needs. Supports 3-level hierarchy.

### Level 1 Requirements

```yaml
product_requirements:
  PR001:
    id: PR001
    title: "Continuous Data Acquisition"
    description: "The system shall continuously acquire sensor data at minimum 1Hz sampling rate."
    verification: "Design review and system testing"
    linked_user_needs:
      - UN001
```

### Level 2 Requirements (Sub-requirements)

```yaml
  PR001.1:
    id: PR001.1
    title: "Sensor Interface"
    description: "The system shall interface with approved biosensors via I2C protocol."
    verification: "Integration testing"
    parent: PR001    # Links to parent requirement
    linked_user_needs:
      - UN001
```

### Level 3 Requirements (Detailed requirements)

```yaml
  PR001.1.1:
    id: PR001.1.1
    title: "I2C Communication"
    description: "I2C bus shall operate at 400kHz fast mode with hardware CRC checking."
    verification: "Design review and protocol testing"
    parent: PR001.1  # Links to parent
    linked_user_needs:
      - UN001
```

### Schema

```yaml
product_requirements:
  <ID>:
    id: <ID>                    # Unique identifier
    title: string               # Short title
    description: string         # Detailed requirement
    verification: string        # How to verify (test, review, analysis, inspection)
    parent: <Parent_ID>         # Optional: Parent requirement ID
    linked_user_needs: [<UN_IDs>]  # List of user need IDs this addresses
```

### Hierarchical Naming

- **Level 1**: `PR###` (e.g., PR001, PR002)
- **Level 2**: `PR###.#` (e.g., PR001.1, PR001.2)
- **Level 3**: `PR###.#.#` (e.g., PR001.1.1, PR001.1.2)

## Specifications

Design specifications that implement requirements.

### Software Specifications

```yaml
software_specifications:
  SW001:
    id: SW001
    title: "Data Acquisition Module"
    description: "Python module implementing sensor data acquisition with error handling and data validation."
    module: "data_acquisition.py"
    linked_requirements:
      - PR001
      - PR001.1
```

### Hardware Specifications

```yaml
hardware_specifications:
  HW001:
    id: HW001
    title: "Main Processing Unit"
    description: "ARM Cortex-M4 microcontroller with 256KB RAM, 1MB Flash, running at 168MHz."
    component: "STM32F407"
    linked_requirements:
      - PR002
      - PR002.1
```

### Schema

```yaml
<type>_specifications:
  <ID>:
    id: <ID>                          # Unique identifier
    title: string                     # Short title
    description: string               # Detailed specification
    module: string                    # (SW) Module/file name
    component: string                 # (HW) Component/part number
    linked_requirements: [<PR_IDs>]  # Requirements this implements
```

### Naming Convention

- **Software**: `SW###` (e.g., SW001, SW002)
- **Hardware**: `HW###` (e.g., HW001, HW002)

## Risks

ISO 14971 risk assessments organized by categories.

### Structure

```yaml
risks:
  patient_safety:                    # Category name
    group_name: "Patient Safety"     # Display name
    risks:
      R001:
        id: R001
        title: "Incorrect Glucose Reading"
        description: "Sensor drift or failure could lead to incorrect glucose readings, causing inappropriate insulin dosing."
        severity: S4                 # From severity_mapping
        probability_occurrence: PO2  # From probability_occurrence_mapping
        probability_harm: PH3        # From probability_harm_mapping
        linked_specs:               # Specifications that mitigate this risk
          - SW001
          - SW002
          - HW001
```

### Risk Categories

Organize risks into logical groups:

```yaml
risks:
  patient_safety:
    group_name: "Patient Safety"
    risks: { ... }
  
  device_functionality:
    group_name: "Device Functionality"
    risks: { ... }
  
  data_security:
    group_name: "Data Security & Privacy"
    risks: { ... }
```

### Schema

```yaml
risks:
  <category_key>:
    group_name: string              # Display name for category
    risks:
      <Risk_ID>:
        id: <Risk_ID>              # Unique identifier (R###)
        title: string              # Brief hazard description
        description: string        # Detailed hazard scenario
        severity: <S#>             # S1-S9 from severity_mapping
        probability_occurrence: <PO#>  # PO1-PO3
        probability_harm: <PH#>    # PH1-PH3
        linked_specs: [<Spec_IDs>] # Mitigation measures
```

### RBM Calculation

The Risk-Benefit Matrix score is automatically calculated:

```
RBM = severity_number × PO_number × PH_number
```

Example: S4 × PO2 × PH3 = 4 × 2 × 3 = 24

## Mitigation Links

*Note: Currently, risk mitigations are specified directly in the risk's `linked_specs` field. This section is reserved for future enhancement.*

## Validation and Best Practices

### YAML Syntax

- Use 2 spaces for indentation (not tabs)
- Strings with special characters need quotes
- Lists use `- item` format or `[item1, item2]`
- Dates in `YYYY-MM-DD` format

### ID Conventions

- **User Needs**: `UN###`
- **Requirements**: `PR###`, `PR###.#`, `PR###.#.#`
- **Software Specs**: `SW###`
- **Hardware Specs**: `HW###`
- **Risks**: `R###`

### Validation Checks

Before committing your DHF file:

1. **Syntax Check**: Valid YAML
   ```bash
   poetry run python -c "import yaml; yaml.safe_load(open('your-dhf.yaml'))"
   ```

2. **ID Uniqueness**: No duplicate IDs
3. **Link Validity**: All referenced IDs exist
4. **Required Fields**: All required fields present
5. **Hierarchy**: Parent IDs exist for sub-requirements

### Version Control

```bash
# Add your DHF file to Git
git add my-device-dhf.yaml
git commit -m "Updated requirements for feature X"

# Create branches for major changes
git checkout -b feature/new-requirements
```

### Backup Strategy

- Store in Git repository
- Tag releases: `git tag v1.0`
- Export reports regularly
- Keep offline backups

## Example Templates

### Minimal DHF File

```yaml
metadata:
  project_name: "My Device"
  device_type: "Medical Device"
  version: "1.0"
  created_date: "2025-01-15"
  last_modified: "2025-01-15"

configuration:
  severity_mapping:
    S1: { name: "Low", description: "Minor" }
    S2: { name: "Medium", description: "Moderate" }
    S3: { name: "High", description: "Serious" }
  probability_occurrence_mapping:
    PO1: { name: "Low", description: "Unlikely" }
    PO2: { name: "Medium", description: "Possible" }
    PO3: { name: "High", description: "Probable" }
  probability_harm_mapping:
    PH1: { name: "Low", description: "Unlikely harm" }
    PH2: { name: "Medium", description: "Possible harm" }
    PH3: { name: "High", description: "Probable harm" }

user_needs:
  UN001:
    id: UN001
    title: "Basic Need"
    description: "Users need X"

product_requirements:
  PR001:
    id: PR001
    title: "Basic Requirement"
    description: "System shall do X"
    verification: "Testing"
    linked_user_needs: [UN001]

software_specifications: {}
hardware_specifications: {}

risks:
  safety:
    group_name: "Safety"
    risks:
      R001:
        id: R001
        title: "Basic Risk"
        description: "Hazard scenario"
        severity: S2
        probability_occurrence: PO2
        probability_harm: PH2
        linked_specs: []

mitigation_links: {}
```

## Troubleshooting

### Common YAML Errors

**Indentation Error**
```yaml
# Wrong:
user_needs:
UN001:  # Missing indentation
  
# Right:
user_needs:
  UN001:  # Proper indentation
```

**String Quoting**
```yaml
# Use quotes for strings with colons
description: "Error: Invalid input"  # Correct
description: Error: Invalid input    # Wrong - colon causes error
```

**List Format**
```yaml
# Both formats work:
linked_user_needs: [UN001, UN002]

# or
linked_user_needs:
  - UN001
  - UN002
```

### Validation Errors

If Pocket DHF won't load your file:

1. Check YAML syntax with online validator
2. Verify all IDs are unique
3. Check that linked IDs exist
4. Ensure required fields are present
5. Check indentation (2 spaces, no tabs)

## Migration and Import

### From Excel/CSV

Create a script to convert:
```python
import yaml
import pandas as pd

df = pd.read_excel('requirements.xlsx')
requirements = {}
for _, row in df.iterrows():
    requirements[row['ID']] = {
        'id': row['ID'],
        'title': row['Title'],
        'description': row['Description'],
        # ... other fields
    }

with open('dhf.yaml', 'w') as f:
    yaml.dump({'product_requirements': requirements}, f)
```

### From Other DHF Tools

Export to CSV, then convert to YAML format.

## Reference

- [YAML Specification](https://yaml.org/spec/)
- [ISO 14971:2019](https://www.iso.org/standard/72704.html) - Medical device risk management
- [FDA 21 CFR Part 820](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/cfrsearch.cfm?cfrpart=820) - Quality System Regulation

---

*For usage instructions, see the [User Guide](user-guide.md)*

