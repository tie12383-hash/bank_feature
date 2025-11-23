"""Tests for bank_feature application."""

import pytest
import sys
import os
import pandas as pd
from datetime import datetime
from main import main
from main import display_transaction, display_transactions_summary, get_amount_display


class TestBankFeatureApp:
    """Test class for BankFeatureApp."""

    def test_app_initialization(self):
        """Test app initialization."""
        app = BankFeatureApp("data/operations.xlsx")
        assert app.data_file == "data/operations.xlsx"
        assert app.transactions_df is None
        assert app.transactions_list is None

    def test_load_data(self, tmp_path):
        """Test data loading functionality."""
        # Create a temporary Excel file for testing
        test_data = pd.DataFrame({
            'date': pd.to_datetime(['2024-03-01', '2024-03-02']),
            'amount': [100.0, -50.0],
            'category': ['Income', 'Food'],
            'description': ['Salary', 'Groceries'],
            'card_number': ['1234', '1234']
        })

        test_file = tmp_path / "test_operations.xlsx"
        test_data.to_excel(test_file, index=False)

        app = BankFeatureApp(str(test_file))
        app.load_data()

        assert app.transactions_df is not None
        assert len(app.transactions_df) == 2
        assert app.transactions_list is not None
        assert len(app.transactions_list) == 2

    @pytest.fixture
    def sample_app(self):
        """Sample app with test data."""
        app = BankFeatureApp()
        app.transactions_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-03-01', '2024-03-02', '2024-03-03']),
            'amount': [100.0, -50.0, -25.5],
            'category': ['Income', 'Food', 'Transport'],
            'description': ['Salary', 'Groceries', 'Bus ticket'],
            'card_number': ['1234', '1234', '5678']
        })
        app.transactions_list = app.transactions_df.to_dict('records')
        return app


class TestServices:
    """Test class for services module."""

    def test_profitable_cashback_categories(self):
        """Test cashback categories analysis."""
        from services import profitable_cashback_categories

        transactions = [
            {
                'date': datetime(2024, 3, 1),
                'amount': -100.0,
                'category': 'Food'
            },
            {
                'date': datetime(2024, 3, 2),
                'amount': -50.0,
                'category': 'Food'
            },
            {
                'date': datetime(2024, 3, 3),
                'amount': -30.0,
                'category': 'Transport'
            }
        ]

        result = profitable_cashback_categories(transactions, 2024, 3)

        assert isinstance(result, dict)
        assert 'Food' in result
        assert 'Transport' in result
        # 1% cashback on expenses
        assert result['Food'] == pytest.approx(1.5, 0.01)  # (100 + 50) * 0.01

    def test_simple_search(self):
        """Test simple search functionality."""
        from services import simple_search

        transactions = [
            {
                'description': 'Grocery store',
                'category': 'Food',
                'amount': -50.0
            },
            {
                'description': 'Gas station',
                'category': 'Transport',
                'amount': -30.0
            },
            {
                'description': 'Restaurant food',
                'category': 'Entertainment',
                'amount': -80.0
            }
        ]

        result = simple_search('food', transactions)
        assert len(result) == 2  # Grocery store and Restaurant food

        result = simple_search('transport', transactions)
        assert len(result) == 1


class TestUtils:
    """Test class for utils module."""

    def test_get_greeting_by_time(self):
        """Test greeting by time of day."""
        from utils import get_greeting_by_time

        assert get_greeting_by_time("2024-03-15 08:30:00") == "Доброе утро"
        assert get_greeting_by_time("2024-03-15 14:30:00") == "Добрый день"
        assert get_greeting_by_time("2024-03-15 19:30:00") == "Добрый вечер"
        assert get_greeting_by_time("2024-03-15 23:30:00") == "Доброй ночи"

    def test_get_date_range(self):
        """Test date range calculation."""
        from utils import get_date_range

        # Test month period
        start, end = get_date_range("2024-03-15", "M")
        assert start == "2024-03-01"
        assert end == "2024-03-15"

        # Test week period
        start, end = get_date_range("2024-03-15", "W")  # This was a Friday
        assert end == "2024-03-15"
        # Start should be Monday of that week (2024-03-11)


class TestViews:
    """Test class for views module."""

    def test_main_page_data_structure(self, sample_app):
        """Test main page data structure."""
        from views import main_page_data

        result = main_page_data("2024-03-15 14:30:00", sample_app.transactions_df)

        expected_keys = ["greeting", "cards", "top_transactions", "currency_rates", "stock_prices"]
        for key in expected_keys:
            assert key in result

        assert isinstance(result["cards"], list)
        assert isinstance(result["top_transactions"], list)
        assert isinstance(result["currency_rates"], list)
        assert isinstance(result["stock_prices"], list)


def test_display_transaction(capsys):
    """Test transaction display function."""
    transaction = {
        'date': '2023-10-01T12:00:00.000',
        'description': 'Test transaction',
        'from': 'Visa 1234567812345678',
        'to': 'Счет 1234567890123456',
        'operationAmount': {
            'amount': '100.00',
            'currency': {'code': 'RUB'}
        }
    }

    display_transaction(transaction)
    captured = capsys.readouterr()
    assert "Test transaction" in captured.out
    assert "100.00" in captured.out


def test_display_transactions_summary_empty(capsys):
    """Test summary display with empty transactions."""
    display_transactions_summary([])
    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out