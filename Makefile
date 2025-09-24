.PHONY: help install test lint format copyright-check copyright-fix docstring-check docstring-fix pre-commit-install clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install          Install dependencies using Poetry"
	@echo "  test             Run tests with pytest"
	@echo "  lint             Run linting with flake8"
	@echo "  format           Format code with black and isort"
	@echo "  copyright-check  Check for missing copyright headers"
	@echo "  copyright-fix    Automatically add missing copyright headers"
	@echo "  docstring-check  Check for missing class docstrings"
	@echo "  docstring-fix    Automatically add missing class docstrings"
	@echo "  pre-commit-install  Install pre-commit hooks"
	@echo "  clean            Clean up temporary files"

# Development setup
install:
	poetry install

# Testing
test:
	poetry run pytest

# Code quality
lint:
	poetry run flake8 .

format:
	poetry run black .
	poetry run isort .

# Copyright management
copyright-check:
	python3 scripts/check_copyright.py

copyright-fix:
	python3 scripts/check_copyright.py --fix

docstring-check:
	python3 scripts/check_docstrings.py

docstring-fix:
	python3 scripts/check_docstrings.py --fix

# Pre-commit hooks
pre-commit-install:
	poetry run pre-commit install

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
