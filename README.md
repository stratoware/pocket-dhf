# Pocket DHF

A lightweight Device History File management system built with Flask.

## Description

Pocket DHF provides an efficient way to manage and track device history files for medical devices, ensuring compliance and streamlined documentation. This system is designed to be lightweight, fast, and user-friendly while maintaining the necessary regulatory compliance features.

## Features

- 📋 **Document Management**: Organize and manage device history files with ease
- 🔍 **Compliance Tracking**: Ensure regulatory compliance with built-in tracking
- ⚡ **Lightweight**: Fast and efficient system designed for simplicity
- 🌐 **Web-based**: Modern web interface built with Flask and Bootstrap

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pocket-dhf
   ```

2. Install dependencies using Poetry:
   ```bash
   make install
   # or
   poetry install
   ```

## Running the Application

Start the development server:

```bash
poetry run python main.py
```

The application will be available at: http://localhost:8080

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
- **pytest**: Testing with coverage
- **pre-commit**: Git hooks for quality checks

## Project Structure

```
pocket-dhf/
├── app/                    # Main application package
│   ├── __init__.py        # Flask app factory
│   ├── routes.py          # Application routes
│   ├── templates/         # Jinja2 templates
│   └── static/            # Static files (CSS, JS, images)
├── tests/                 # Test files
├── scripts/               # Utility scripts
├── main.py                # Application entry point
├── pyproject.toml         # Poetry configuration
└── README.md              # This file
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Stratoware LLC
