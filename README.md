# bank_feature

Widget for displaying client bank operations.

## Project Purpose

Development of a backend component for a widget displaying recent successful bank operations. The project includes functions for data masking, operations processing, and date formatting.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tie12383-hash/bank_feature.git
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

## Generators Module

The `generators` module provides efficient data processing tools for working with large volumes of transaction data using Python generators.

### Functions

#### `filter_by_currency(transactions, currency_code)`
Filters transactions by currency code and returns an iterator.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["id"], transaction["operationAmount"]["amount"])
```