"""Tests for views module."""
import pytest
import pandas as pd
from datetime import datetime
from src.views import main_page_data, events_page_data


class TestViews:
    @pytest.fixture
    def sample_dataframe(self):
        return pd.DataFrame({
            'card_number': ['1234567812345678', '8765432187654321'],
            'amount': [-100.0, -200.0, 300.0, -50.0],
            'category': ['Супермаркеты', 'Рестораны', 'Зарплата', 'Транспорт'],
            'description': ['Магнит', 'Ресторан', 'ЗП', 'Такси'],
            'date': [
                datetime(2024, 3, 1),
                datetime(2024, 3, 2),
                datetime(2024, 3, 3),
                datetime(2024, 3, 4)
            ]
        })

    def test_main_page_data(self, sample_dataframe):
        result = main_page_data("2024-03-15 14:30:00", sample_dataframe)
        assert 'greeting' in result
        assert 'cards' in result
        assert 'top_transactions' in result

    def test_events_page_data(self, sample_dataframe):
        result = events_page_data("2024-03-15", sample_dataframe, "M")
        assert 'expenses' in result
        assert 'income' in result