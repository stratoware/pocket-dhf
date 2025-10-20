# Pocket DHF

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight, open-source Device History File (DHF) management system for medical device compliance.

## Description

Pocket DHF provides an efficient way to manage and track device history files for medical devices, ensuring compliance and streamlined documentation. Built for medical device manufacturers, quality engineers, and regulatory professionals, this system is designed to be lightweight, fast, and user-friendly while maintaining the necessary regulatory compliance features.

Unlike heavy enterprise document management systems, Pocket DHF uses simple YAML files for data storage, making it perfect for version control and team collaboration.

## ⚠️ Important Notice

**Regulatory Compliance Disclaimer**: Pocket DHF is a tool for managing Device History Files. Users are solely responsible for ensuring compliance with applicable regulations including FDA 21 CFR Part 820, ISO 13485, and other medical device standards. This software is provided "as-is" without warranty and does not guarantee regulatory compliance.

**Not a Medical Device**: This software is a documentation management tool and is not itself a medical device. It does not diagnose, treat, cure, or prevent any disease.

## Features

### 📋 Document Management
- Organize user needs, product requirements, design specifications, and risk assessments
- Three-level nested requirements structure for complex product hierarchies
- Folder-based organization with intuitive navigation
- Real-time editing with validation

### 🔗 Traceability
- Full bidirectional traceability matrix
- Link requirements to specifications to risks
- Visual traceability navigation with hyperlinks
- Automatic relationship tracking and validation

### 🎯 Risk Management
- ISO 14971 compliant risk assessment
- Risk-Benefit Matrix (RBM) calculations
- Link risks to mitigation strategies
- Configurable risk severity and probability scoring

### 📊 Reporting
- Generate comprehensive DHF reports
- Customizable report templates (Markdown-based)
- Export to HTML and PDF
- Auto-populated traceability matrices

### 🛠️ Developer-Friendly
- YAML-based data storage (version control friendly)
- RESTful API for integrations
- Modern web interface (Bootstrap 5)
- Lightweight - no database required
- Extensive test coverage (>80%)

## Screenshots

### Main Dashboard
![Dashboard](docs/images/dashboard.png)
*Browse and navigate your device history file structure*

### Requirements Editing
![Requirements](docs/images/requirements.png)
*Edit requirements with full traceability support*

### Traceability Matrix
![Traceability](docs/images/traceability.png)
*Visualize connections between user needs, requirements, and specifications*

### Risk Management
![Risk Management](docs/images/risk-management.png)
*Assess and manage risks per ISO 14971*

### Report Generation
![Reports](docs/images/reports.png)
*Generate regulatory-ready DHF reports*

## Quick Start

**Prerequisites:**
- Python 3.8 or higher
- Poetry (recommended) or pip
- Git

**Evaluate in 30 seconds:**

```bash
# Clone and try with sample data
git clone https://github.com/stratoware/pocket-dhf.git
cd pocket-dhf
poetry install
poetry run python main.py
```

Then open http://localhost:8080 in your browser to explore the sample data!

## Installation

### Recommended: Git Submodule in Your Device Repository

The recommended approach is to add Pocket DHF as a submodule to your medical device code repository, keeping your DHF data alongside your device code.

**Repository Structure:**
```
my-medical-device/              # Your main device repository
├── .git/
├── src/                        # Your device source code
├── tests/                      # Your device tests
├── docs/                       # Your device documentation
├── dhf/                        # DHF documentation
│   ├── device-dhf.yaml        # Your DHF data file
│   └── reports/               # Generated reports
└── pocket-dhf/                 # Git submodule
    ├── app/
    ├── main.py
    └── ...
```

**Setup Steps:**

1. **Add Pocket DHF as a submodule to your device repository:**
   ```bash
   cd my-medical-device
   git submodule add https://github.com/stratoware/pocket-dhf.git pocket-dhf
   git submodule update --init --recursive
   ```

2. **Install Pocket DHF dependencies:**
   ```bash
   cd pocket-dhf
   poetry install
   cd ..
   ```

3. **Create your DHF data file:**
   ```bash
   mkdir -p dhf
   cp pocket-dhf/sample-data/dhf_data.yaml dhf/device-dhf.yaml
   # Edit dhf/device-dhf.yaml with your project details
   ```

4. **Run Pocket DHF pointing to your data file:**
   ```bash
   cd pocket-dhf
   poetry run python main.py --data-file ../dhf/device-dhf.yaml
   ```

5. **Access the application:**
   Open http://localhost:8080 in your browser

**Benefits of This Approach:**
- ✅ DHF data is version-controlled with your device code
- ✅ Pocket DHF updates independently via git submodule
- ✅ Single repository for code + compliance documentation
- ✅ Easy to track changes to both code and DHF together
- ✅ Traceability between source code commits and DHF updates

**Cloning a Repository with Pocket DHF Submodule:**

If someone else clones your device repository:
```bash
git clone https://github.com/your-org/my-medical-device.git
cd my-medical-device
git submodule update --init --recursive
cd pocket-dhf && poetry install && cd ..
```

**Updating Pocket DHF:**
```bash
cd my-medical-device/pocket-dhf
git fetch origin
git checkout main
git pull
cd ..
git add pocket-dhf
git commit -m "Update Pocket DHF to latest version"
```

### Alternative: Standalone Installation

For evaluation or development of Pocket DHF itself:

**Using Poetry:**
```bash
git clone https://github.com/stratoware/pocket-dhf.git
cd pocket-dhf
poetry install
poetry run python main.py  # Uses sample data
```

**Using pip:**
```bash
git clone https://github.com/stratoware/pocket-dhf.git
cd pocket-dhf
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py  # Uses sample data
```

## Running the Application

### With Your Device Repository Data (Recommended)

From your main device repository root:
```bash
cd pocket-dhf
poetry run python main.py --data-file ../dhf/device-dhf.yaml
```

Or from within the pocket-dhf directory:
```bash
poetry run python main.py --data-file /path/to/your/device-dhf.yaml
```

### With Sample Data (Standalone)

```bash
poetry run python main.py
# Uses built-in sample-data/dhf_data.yaml
```

### Custom Port

```bash
poetry run python main.py --data-file ../dhf/device-dhf.yaml --port 5000
```

## Usage

### First Time Setup

1. **Add Pocket DHF as a submodule** (see Installation above)
2. **Copy sample data** as a starting point: `cp pocket-dhf/sample-data/dhf_data.yaml dhf/device-dhf.yaml`
3. **Customize your data file** with your device information
4. **Run Pocket DHF** pointing to your data file
5. **Edit via web UI** or directly in YAML (both work!)
6. **Commit changes** to your device repository to track DHF history

### Basic Workflow

1. **Create User Needs**: Define what users need from your device
2. **Define Requirements**: Break down user needs into product requirements
3. **Specify Design**: Create software and hardware specifications
4. **Assess Risks**: Identify and evaluate risks per ISO 14971
5. **Link Everything**: Create traceability links between all elements
6. **Generate Reports**: Export your DHF for regulatory submissions

For detailed instructions, see the [User Guide](docs/user-guide.md).

## Documentation

- **[Software Specifications](docs/specifications.md)** - Complete functional specifications and requirements
- **[User Guide](docs/user-guide.md)** - How to use Pocket DHF
- **[Data Format Guide](docs/data-format.md)** - YAML schema and structure documentation
- **[Report Templates](sample-data/report-templates/)** - Customizing report generation

## Development

### Available Commands

- `make install` - Install dependencies using Poetry
- `make test` - Run tests with pytest
- `make lint` - Run linting with flake8
- `make format` - Format code with black and isort
- `make copyright-check` - Check for missing copyright headers
- `make copyright-fix` - Automatically add missing copyright headers
- `make docstring-check` - Check for missing class docstrings
- `make docstring-fix` - Automatically add missing class docstrings
- `make pre-commit-install` - Install pre-commit hooks
- `make clean` - Clean up temporary files

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **pytest**: Testing with coverage (>80% required)
- **pre-commit**: Git hooks for quality checks

### Running Tests

```bash
make test
# or
poetry run pytest
```

View coverage report: `open htmlcov/index.html`

## Project Structure

```
pocket-dhf/
├── app/                    # Main application package
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # Application routes
│   ├── data_utils.py      # Data management utilities
│   ├── templates/         # Jinja2 templates
│   └── static/            # Static files (CSS, JS, images)
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── scripts/               # Utility scripts
├── sample-data/          # Sample DHF data
│   └── report-templates/ # Report templates
├── docs/                 # Documentation
│   └── images/          # Screenshots
├── main.py               # Application entry point
├── pyproject.toml        # Poetry configuration
└── README.md             # This file
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- How to set up the development environment
- Our code style guidelines
- How to submit pull requests
- Our code of conduct

**Quick Start for Contributors:**

```bash
# Fork the repo, then:
git clone https://github.com/YOUR-USERNAME/pocket-dhf.git
cd pocket-dhf
make install
make test
make format
```

## Support

- 📖 **Documentation**: See [docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/stratoware/pocket-dhf/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/stratoware/pocket-dhf/discussions)
- 💬 **Questions**: [GitHub Discussions Q&A](https://github.com/stratoware/pocket-dhf/discussions/categories/q-a)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Why MIT?

We chose the MIT License to maximize adoption and allow both open-source and commercial use. You're free to use Pocket DHF in your commercial products, fork it, modify it, and distribute it as you see fit - just retain the copyright notice.

**Copyright (c) 2025 Stratoware LLC**

---

*Built with ❤️ for the medical device community*
