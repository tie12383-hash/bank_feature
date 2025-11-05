"""Tests for file_reader module."""

import sys
from unittest.mock import Mock, patch
import pytest

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

if PANDAS_AVAILABLE:
    from src.file_reader import read_csv_file, read_excel_file


@pytest.mark.skipif(not PANDAS_AVAILABLE, reason="pandas not installed")
class TestFileReader:
    """Test class for file reader functions."""

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_success(self, mock_read_csv: Mock) -> None:
        """Test successful reading of CSV file."""
        mock_df = Mock()
        mock_df.to_dict.return_value = [
            {
                'id': 1,
                'state': 'EXECUTED',
                'date': '2024-01-01',
                'operationAmount': {
                    'amount': '100.0',
                    'currency': {'code': 'USD', 'name': 'US Dollar'}
                }
            },
            {
                'id': 2,
                'state': 'CANCELED',
                'date': '2024-01-02',
                'operationAmount': {
                    'amount': '200.0',
                    'currency': {'code': 'EUR', 'name': 'Euro'}
                }
            }
        ]
        mock_read_csv.return_value = mock_df

        result = read_csv_file('transactions.csv')

        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['state'] == 'EXECUTED'
        assert result[1]['state'] == 'CANCELED'
        mock_read_csv.assert_called_once_with('transactions.csv')

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_not_found(self, mock_read_csv: Mock) -> None:
        """Test reading non-existent CSV file."""
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        result = read_csv_file('nonexistent.csv')

        assert result == []
        mock_read_csv.assert_called_once_with('nonexistent.csv')

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_empty(self, mock_read_csv: Mock) -> None:
        """Test reading empty CSV file."""
        empty_data_error = type('EmptyDataError', (Exception,), {})
        mock_read_csv.side_effect = empty_data_error("No data")

        result = read_csv_file('empty.csv')

        assert result == []
        mock_read_csv.assert_called_once_with('empty.csv')

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_success(self, mock_read_excel: Mock) -> None:
        """Test successful reading of Excel file."""
        mock_df = Mock()
        mock_df.to_dict.return_value = [
            {
                'id': 3,
                'state': 'EXECUTED',
                'date': '2024-01-03',
                'operationAmount': {
                    'amount': '300.0',
                    'currency': {'code': 'RUB', 'name': 'Russian Ruble'}
                }
            }
        ]
        mock_read_excel.return_value = mock_df

        result = read_excel_file('transactions.xlsx')

        assert len(result) == 1
        assert result[0]['id'] == 3
        assert result[0]['state'] == 'EXECUTED'
        mock_read_excel.assert_called_once_with('transactions.xlsx')

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_not_found(self, mock_read_excel: Mock) -> None:
        """Test reading non-existent Excel file."""
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        result = read_excel_file('nonexistent.xlsx')

        assert result == []
        mock_read_excel.assert_called_once_with('nonexistent.xlsx')

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_general_error(self, mock_read_excel: Mock) -> None:
        """Test reading Excel file with general error."""
        mock_read_excel.side_effect = Exception("General error")

        result = read_excel_file('error.xlsx')

        assert result == []
        mock_read_excel.assert_called_once_with('error.xlsx')


def test_pandas_import_error() -> None:
    """Test that appropriate error is shown when pandas is not available."""
    if not PANDAS_AVAILABLE:
        with pytest.raises(ImportError, match="pandas"):
            from src.file_reader import read_csv_file