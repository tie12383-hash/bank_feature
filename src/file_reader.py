"""Module for reading financial transactions from CSV and XLSX files."""

from typing import List, Dict, Any, cast
from .logger_config import setup_logger

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

file_reader_logger = setup_logger('file_reader', 'logs/file_reader.log')


def _check_pandas_available() -> None:
    """Check if pandas is available and raise informative error if not."""
    if not PANDAS_AVAILABLE:
        raise ImportError(
            "pandas is required for CSV and Excel file support. "
            "Install it with: pip install pandas openpyxl"
        )


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Read financial transactions from CSV file."""
    _check_pandas_available()

    file_reader_logger.debug(f"Attempting to read CSV file: {file_path}")

    try:
        df = pd.read_csv(file_path)

        transactions: List[Dict[str, Any]] = cast(List[Dict[str, Any]], df.to_dict('records'))

        file_reader_logger.info(
            f"Successfully read {len(transactions)} transactions from {file_path}"
        )
        return transactions

    except FileNotFoundError:
        file_reader_logger.error(f"CSV file not found: {file_path}")
        return []
    except Exception as e:
        file_reader_logger.error(f"Error reading CSV file {file_path}: {str(e)}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """Read financial transactions from Excel file."""
    _check_pandas_available()

    file_reader_logger.debug(f"Attempting to read Excel file: {file_path}")

    try:
        df = pd.read_excel(file_path)

        transactions: List[Dict[str, Any]] = cast(List[Dict[str, Any]], df.to_dict('records'))

        file_reader_logger.info(
            f"Successfully read {len(transactions)} transactions from {file_path}"
        )
        return transactions

    except FileNotFoundError:
        file_reader_logger.error(f"Excel file not found: {file_path}")
        return []
    except Exception as e:
        file_reader_logger.error(f"Error reading Excel file {file_path}: {str(e)}")
        return []