# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Early-stage Python project (`auto_insta`) with Python 3.13 virtual environment set up. The project appears to be related to Instagram automation based on the directory name.

## Development Environment

### Python Setup
- **Python Version**: 3.13.7 (installed via Homebrew)
- **Virtual Environment**: `.venv/` (already created and configured)
- **Virtual Environment Path**: `./.venv/bin/python`

### Environment Activation
```bash
# Activate virtual environment
source .venv/bin/activate

# Deactivate when done
deactivate
```

### Development Tools Installation
The project follows the setup guide in `docs/python-setup.md`. Install development tools with:
```bash
pip install --upgrade pip
pip install black flake8 mypy pytest
```

## Code Quality Commands

### Formatting
```bash
# Format all Python files
black .

# Format specific file
black src/main.py
```

### Linting
```bash
# Check code style
flake8 src/
```

### Type Checking
```bash
# Check type hints
mypy src/
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src tests/
```

## Recommended Project Structure

Based on the setup guide, the project should follow this structure:
```
auto_insta/
├── .venv/                # Virtual environment (already exists)
├── src/                  # Source code (to be created)
│   ├── __init__.py
│   └── main.py
├── tests/                # Test code (to be created)
│   ├── __init__.py
│   └── test_main.py
├── docs/                 # Documentation (exists)
├── requirements.txt      # Production dependencies (to be created)
├── requirements-dev.txt  # Development dependencies (to be created)
└── README.md            # Project documentation (to be created)
```

## Dependency Management

### Save Dependencies
```bash
# Save current packages to requirements.txt
pip freeze > requirements.txt
```

### Install Dependencies
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## VS Code Configuration

The setup guide recommends creating `.vscode/settings.json` with:
- Python interpreter: `./venv/bin/python`
- Black formatter enabled
- Flake8 and mypy linting enabled
- Format on save enabled
- Pytest configuration for tests

## Important Notes

- The project uses Korean documentation in `docs/python-setup.md`
- Virtual environment is already configured with Python 3.13
- No source code exists yet - this is a fresh project setup
- Follow the Korean setup guide for detailed VS Code configuration