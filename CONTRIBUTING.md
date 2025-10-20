# Contributing to Pocket DHF

Thank you for your interest in contributing to Pocket DHF! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- Git
- A GitHub account

### Finding Issues to Work On

- Check the [Issues](https://github.com/stratoware/pocket-dhf/issues) page
- Look for issues labeled `good first issue` for newcomers
- Issues labeled `help wanted` are great opportunities to contribute
- Feel free to ask questions on any issue

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/pocket-dhf.git
cd pocket-dhf
```

### 2. Set Up Upstream Remote

```bash
git remote add upstream https://github.com/stratoware/pocket-dhf.git
git fetch upstream
```

### 3. Install Dependencies

```bash
# Using Make (recommended)
make install

# Or using Poetry directly
poetry install
```

### 4. Install Pre-commit Hooks

```bash
make pre-commit-install
# or
poetry run pre-commit install
```

This will automatically run code quality checks before each commit.

### 5. Verify Setup

```bash
# Run tests to ensure everything works
make test

# Start the application
poetry run python main.py
```

## Making Changes

### 1. Create a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

#### Branch Naming Conventions

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions or updates

Examples:
- `feature/add-pdf-export`
- `fix/traceability-matrix-display`
- `docs/update-api-guide`

### 2. Make Your Changes

- Write clean, readable code
- Follow the [Code Style](#code-style) guidelines
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: brief description

More detailed explanation of what changed and why.
Reference any related issues: #123"
```

#### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant
- Separate subject from body with a blank line

Good examples:
```
Add PDF export functionality for reports

Implements PDF generation using ReportLab library.
Users can now export reports directly to PDF format.

Fixes #45
```

```
Fix traceability matrix link navigation

Links in the traceability matrix were not properly
handling multi-level requirements. Updated the
navigation logic to support hierarchical IDs.

Closes #78
```

## Code Style

Pocket DHF follows strict code quality standards:

### Python Style

- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting
- **flake8**: Linting
- **Type hints**: Encouraged but not required

### Running Code Quality Checks

```bash
# Format code
make format

# Check linting
make lint

# Check copyright headers
make copyright-check

# Check docstrings
make docstring-check

# All checks (automatically run by pre-commit)
make format && make lint
```

### Documentation Standards

- All public classes should have docstrings
- Functions with non-obvious behavior should have docstrings
- Use Google-style docstrings:

```python
def calculate_rbm_score(severity: int, po: int, ph: int) -> int:
    """Calculate Risk-Benefit Matrix score.
    
    Args:
        severity: Severity level (1-9)
        po: Probability of occurrence (1-3)
        ph: Probability of harm (1-3)
        
    Returns:
        RBM score (severity × po × ph)
        
    Raises:
        ValueError: If any parameter is out of range
    """
    return severity * po * ph
```

## Testing

### Writing Tests

- Tests are located in the `tests/` directory
- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`
- Test files should start with `test_`
- Test functions should start with `test_`

Example test:

```python
def test_calculate_rbm_score():
    """Test RBM score calculation."""
    manager = DHFDataManager("test_data.yaml")
    score = manager.calculate_rbm_score(4, 2, 3)
    assert score == 24
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
poetry run pytest tests/unit/test_data_utils.py

# Run with verbose output
poetry run pytest -v

# Run with coverage report
poetry run pytest --cov=app --cov-report=html
```

### Coverage Requirements

- All new code must maintain >80% test coverage
- Pull requests that decrease coverage will not be merged
- View coverage report: `open htmlcov/index.html`

## Submitting Changes

### Before Submitting

1. **Sync with upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks:**
   ```bash
   make format
   make lint
   make test
   ```

3. **Update documentation** if you've changed functionality

4. **Test manually** in the browser if you've changed the UI

### Creating a Pull Request

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request on GitHub:**
   - Go to the [Pocket DHF repository](https://github.com/stratoware/pocket-dhf)
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the pull request template

3. **Pull Request Checklist:**
   - [ ] Tests pass locally
   - [ ] Code is formatted (Black, isort)
   - [ ] Linting passes (flake8)
   - [ ] Coverage remains >80%
   - [ ] Documentation is updated
   - [ ] Commit messages are clear
   - [ ] Branch is up to date with main
   - [ ] Copyright headers are present (run `make copyright-check`)

### Pull Request Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## Testing
Describe how you tested these changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Code formatted with Black
- [ ] Linting passes
- [ ] Documentation updated
- [ ] Coverage >80%
```

### Code Review Process

1. A maintainer will review your PR within a few days
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Your contribution will be included in the next release!

## Reporting Bugs

### Before Reporting

1. Check the [existing issues](https://github.com/stratoware/pocket-dhf/issues)
2. Try the latest version from `main` branch
3. Gather information about the bug

### Creating a Bug Report

Include:

- **Clear title** describing the issue
- **Steps to reproduce** the bug
- **Expected behavior**
- **Actual behavior**
- **Environment details:**
  - OS and version
  - Python version
  - Pocket DHF version
  - Browser (if UI bug)
- **Error messages** or screenshots
- **Sample data file** if relevant (remove sensitive info)

Use the bug report template on GitHub.

## Suggesting Features

We love feature suggestions! Here's how:

### Before Suggesting

1. Check [existing issues and discussions](https://github.com/stratoware/pocket-dhf/discussions)
2. Ensure it aligns with project goals
3. Consider if it's a general use case

### Feature Request Template

Include:

- **Clear title** of the feature
- **Problem description:** What problem does this solve?
- **Proposed solution:** How should it work?
- **Alternatives considered:** Other ways to solve this
- **Use case:** When would this be used?
- **Regulatory impact:** Any compliance considerations?

Submit via [GitHub Discussions](https://github.com/stratoware/pocket-dhf/discussions/categories/ideas) or Issues.

## Documentation Contributions

Documentation is crucial! Ways to help:

- Fix typos or unclear wording
- Add examples or tutorials
- Improve the User Guide
- Add screenshots or diagrams
- Translate documentation (future)

Documentation files:
- `README.md` - Project overview
- `docs/user-guide.md` - User documentation
- `docs/data-format.md` - YAML schema reference
- Code comments and docstrings

## Development Tips

### Useful Commands

```bash
# Code quality
make format          # Format code with Black and isort
make lint           # Run flake8 linting
make copyright-check # Check copyright headers
make docstring-check # Check for missing docstrings

# Testing
make test           # Run full test suite
make clean          # Clean temporary files

# Development
make install        # Install dependencies
make pre-commit-install  # Install git hooks
```

### Working with YAML Data

- Use `sample-data/dhf_data.yaml` for testing
- Create minimal test files for specific scenarios
- Validate YAML syntax before committing
- Test with both small and large data files

### Debugging

```bash
# Run with debug output
FLASK_DEBUG=1 poetry run python main.py

# Run specific test with print output
poetry run pytest tests/unit/test_data_utils.py -v -s

# Start Python debugger
poetry run python -m pdb main.py
```

## Community

### Communication Channels

- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/stratoware/pocket-dhf/issues)
- 💡 **Feature Requests:** [GitHub Discussions](https://github.com/stratoware/pocket-dhf/discussions)
- 💬 **Questions:** [GitHub Discussions Q&A](https://github.com/stratoware/pocket-dhf/discussions/categories/q-a)
- 📖 **Documentation:** [User Guide](docs/user-guide.md)

### Getting Help

- Check the documentation first
- Search existing issues and discussions
- Ask in GitHub Discussions for general questions
- Be patient and respectful

### Recognition

Contributors will be:
- Listed in release notes
- Acknowledged in the repository
- Forever appreciated by the medical device community! 🎉

## License

By contributing to Pocket DHF, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask! Create a discussion in [GitHub Discussions](https://github.com/stratoware/pocket-dhf/discussions) and we'll help you get started.

---

**Thank you for contributing to Pocket DHF!** 

Your work helps improve medical device development and compliance for teams around the world.


