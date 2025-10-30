# Analyses Feature - Implementation Summary

## Overview
The Analyses feature has been successfully implemented, allowing users to create, edit, and manage FMEA (Failure Mode and Effects Analysis) and FTA (Fault Tree Analysis) documents, with the ability to sync findings back to the main DHF.

## Features Implemented

### 1. Data Storage
- ✅ Each analysis stored as separate YAML file in `sample-data/analyses/`
- ✅ Support for parent repo override (checks `../analyses/` folder first)
- ✅ Two sample analyses created:
  - `fmea-001.yaml`: Sleep Apnea Monitor - Sensor System FMEA with 10 realistic rows
  - `fta-001.yaml`: Sleep Apnea Monitor - Missed Critical Event FTA with hierarchical structure

### 2. Backend Implementation
- ✅ Added analyses management methods to `DHFDataManager`:
  - `get_analyses()`: List all analyses
  - `load_analysis()`: Load specific analysis
  - `save_analysis()`: Save analysis changes
  - `delete_analysis()`: Delete analysis file
  - `create_analysis()`: Create new analysis with auto-generated ID (FM####/FT####)
  - `sync_analysis_to_dhf()`: Preview sync changes
  - `apply_dhf_sync()`: Apply sync to DHF

- ✅ Added Flask routes in `app/routes.py`:
  - `GET /analyses`: Render analyses page
  - `GET /api/analyses`: List all analyses
  - `GET /api/analyses/<id>`: Get specific analysis
  - `PUT /api/analyses/<id>`: Update analysis
  - `DELETE /api/analyses/<id>`: Delete analysis
  - `POST /api/analyses`: Create new analysis
  - `GET /api/analyses/<id>/sync-preview`: Preview DHF sync
  - `POST /api/analyses/<id>/sync`: Apply DHF sync

### 3. Frontend Implementation
- ✅ Created `app/templates/analyses.html` with:
  - Left panel: List of analyses with type badges and delete buttons
  - Right panel: Conditional rendering for FMEA/FTA editors
  - Add analysis button with modal dialog
  
- ✅ FMEA Table Editor:
  - Inline editing for all fields
  - Automatic Risk Score calculation (Severity × Probability of Harm) per ISO 14971:2019
  - Multi-select dropdowns for Current Controls (links to specs)
  - Multi-select for Recommended Actions
  - Add/delete rows functionality
  - All 9 FMEA columns: Process Step, Failure Mode, Effects, Severity, Causes, Probability of Harm, Current Controls, Risk Score, Recommended Actions

- ✅ FTA Tree Editor:
  - Top Event editing (description, gate type, severity)
  - Intermediate Events management (add/edit/delete with AND/OR gates)
  - Basic Events management (description, probability, parent ID, mitigations)
  - Tree visualization showing hierarchical structure
  - Support for mitigation linking

### 4. Navigation
- ✅ Added "Analyses" link to navbar (positioned before "Reports")
- ✅ Icon: fa-sitemap (appropriate for tree/network analysis)

### 5. DHF Sync Feature
- ✅ Sync preview modal showing planned changes:
  - Risks to create
  - Specifications to create
  - Specifications to link
- ✅ Confirmation workflow (preview → confirm → sync)
- ✅ Creates new RK#### entities for risks
- ✅ Creates new SS#### entities for specifications
- ✅ Organizes synced items in "Analysis-Derived" groups

## Testing Results

### API Endpoints
- ✅ GET /api/analyses - Returns both sample analyses
- ✅ GET /api/analyses/FM0001 - Returns complete FMEA with all rows
- ✅ GET /api/analyses/FT0001 - Returns complete FTA with tree structure
- ✅ GET /api/analyses/FM0001/sync-preview - Returns preview of DHF changes

### Web Interface
- ✅ Page renders correctly at /analyses
- ✅ Analyses list displays with proper badges
- ✅ Navigation link appears in correct position

## File Structure
```
sample-data/
  analyses/
    fmea-001.yaml  (FM0001 - Sensor System FMEA)
    fta-001.yaml   (FT0001 - Missed Critical Event FTA)

app/
  data_utils.py    (+450 lines: analyses management methods)
  routes.py        (+133 lines: analyses routes and API)
  templates/
    analyses.html  (1000+ lines: comprehensive editor UI)
    base.html      (modified: added Analyses nav link)
```

## Usage

### Viewing Analyses
1. Navigate to "Analyses" in the navbar
2. Select an analysis from the left panel
3. View and edit in the appropriate editor (FMEA table or FTA tree)

### Editing FMEA
1. Click into table cells to edit values
2. Use dropdowns for multi-select fields
3. Risk Score updates automatically (Severity × Probability of Harm)
4. Click "Add Row" to create new FMEA rows
5. Click "Save" to persist changes

### Editing FTA
1. Modify top event properties
2. Add/edit/delete intermediate events
3. Add/edit/delete basic events with mitigations
4. Tree visualization updates automatically
5. Click "Save" to persist changes

### Syncing to DHF
1. Click "Preview Sync" to see planned changes
2. Review the list of entities to be created/linked
3. Click "Confirm & Sync" to apply changes
4. New risks and specifications will be added to DHF under "Analysis-Derived" groups

### Creating New Analysis
1. Click the "+" button in the left panel
2. Select type (FMEA or FTA)
3. Enter title and description
4. Click "Create"
5. New analysis appears with auto-generated ID

### Deleting Analysis
1. Click the trash icon next to an analysis
2. Confirm deletion
3. Analysis file is removed

## Technical Details

### ID Generation
- FMEA: FM0001, FM0002, FM0003, ...
- FTA: FT0001, FT0002, FT0003, ...
- Auto-increments based on existing analyses

### Parent Repo Override
The system checks for analyses in this order:
1. `../analyses/` (parent repo, sibling to pocket-dhf)
2. `sample-data/analyses/` (fallback)

This allows parent projects to maintain their own analyses while using pocket-dhf as a submodule.

### FMEA Data Structure
```yaml
id: FM0001
type: fmea
rows:
  - id: FM0001-01
    process_step: "..."
    failure_mode: "..."
    effects: "..."
    severity: 4           # 1-4 scale (Minor, Moderate, Major, Critical)
    causes: "..."
    probability_of_harm: 2  # 1-3 scale per ISO 14971
    current_controls: ["SS0001", "SS0002"]
    risk_score: 8        # Calculated as severity × probability_of_harm
    recommended_actions: ["Action 1", "Action 2"]
```

### FTA Data Structure
```yaml
id: FT0001
type: fta
top_event:
  id: FT0001-TE
  description: "Top level hazard"
  gate_type: OR
  severity: 10
intermediate_events:
  - id: FT0001-IE01
    parent_id: FT0001-TE
    description: "Intermediate failure"
    gate_type: OR
basic_events:
  - id: FT0001-BE01
    parent_id: FT0001-IE01
    description: "Basic failure event"
    probability: 0.001
    mitigations: ["SS0001"]
```

## Future Enhancements (Not in Current Implementation)
- Export FMEA/FTA to PDF
- More sophisticated tree visualization (D3.js)
- Probability calculations for FTA
- Risk priority filtering
- Import/export from Excel
- Multi-user collaboration
- Revision history
- Advanced search/filtering

## Commit
All changes committed with GPG signature:
- Commit: f01004d
- Branch: feature/analyses-page
- Message: "feat: Add Analyses page for FMEA and FTA management"

