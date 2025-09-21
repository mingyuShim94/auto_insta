# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Instagram text extraction tool (`auto_insta`) - a Python CLI application that extracts text content from Instagram posts. The project supports both single URL processing and batch processing of multiple URLs.

## Key Architecture

### Core Components
- **`src/main.py`**: CLI interface with argument parsing, interactive mode, and batch processing
- **`src/extractor.py`**: Instagram text extraction logic using instaloader library
- **`src/utils.py`**: Utility functions for formatting, file saving, and user interaction
- **`src/__main__.py`**: Package entry point for module execution

### Processing Modes
1. **Interactive Mode**: User-friendly CLI for single URLs with guided prompts
2. **Command Line Mode**: Direct URL processing with options
3. **Batch Mode**: Process multiple URLs from a file with optional combined output

## Development Environment

### Python Setup
- **Python Version**: 3.13+ (uses virtual environment at `./.venv/bin/python`)
- **Main Dependency**: instaloader>=4.13.0 for Instagram data extraction

### Environment Commands
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Common Commands

### Running the Application
```bash
# Interactive mode
PYTHONPATH=. ./.venv/bin/python -m src

# Single URL with metadata
PYTHONPATH=. ./.venv/bin/python -m src "https://www.instagram.com/p/ABC123/" --metadata

# Batch processing (recommended)
make batch
# or
./run_batch.sh

# Manual batch processing
PYTHONPATH=. ./.venv/bin/python -m src --batch-file urls.txt --metadata --save json --combined-output
```

### Testing and Quality
```bash
# Run tests
pytest
pytest tests/test_extractor.py  # specific test file
pytest -v  # verbose output

# Code formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Makefile Commands
```bash
make batch           # JSON combined output (default)
make batch-txt       # Text combined output
make batch-individual # Individual JSON files
make clean          # Clear outputs directory
make help           # Show available commands
```

## File Handling

### Input
- **URLs file**: `urls.txt` (one URL per line, supports comments with #)
- **Supported URL formats**: `/p/`, `/reel/`, `/tv/` paths

### Output
- **Directory**: `outputs/` (auto-created)
- **Formats**: Text (.txt) or JSON (.json)
- **Batch mode**: Combined files with timestamp (e.g., `instagram_batch_combined_20231215_143000.json`)

## Error Handling

The application handles:
- Invalid URLs
- Private/deleted posts
- Network issues
- Rate limiting
- Failed URLs are logged to `failed_urls_{timestamp}.txt`

## Important Notes

- Uses `PYTHONPATH=.` prefix for module execution
- Korean language UI and documentation
- Rate limiting with configurable delays (default: 3 seconds between requests)
- Batch processing includes success/failure reporting
- All user-facing text is in Korean