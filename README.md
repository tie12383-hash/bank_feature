# bank_feature

Widget for displaying client bank operations.

## Project Purpose

Development of a backend component for a widget displaying recent successful bank operations. The project includes functions for data masking, operations processing, and date formatting.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tie12383-hash/verbose-parakeet.git
cd bank_feature
```
## Testing

### Overview

The project includes comprehensive tests for all main modules:
- **masks.py**: Tests for card and account number masking functions
- **widget.py**: Tests for bank operations widget functionality  
- **processing.py**: Tests for bank operations processing and filtering

### Running Tests

#### Basic Test Execution

## Logging

The project now includes comprehensive logging for key modules using Python's built-in `logging` library.

### Log Files

Logs are stored in the `logs/` directory with the following structure:
- `logs/utils.log` - Logs for utility functions (JSON file operations, transaction filtering)
- `logs/masks.log` - Logs for card and account masking operations

### Log Format

Each log entry includes:
- **Timestamp**: When the event occurred
- **Module**: Which module generated the log
- **Level**: Severity level (DEBUG, INFO, WARNING, ERROR)
- **Message**: Descriptive message about the event

Example log entry:
```bash
pytest
```