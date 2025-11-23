"""Tests for services module."""
import pytest
import pandas as pd
from datetime import datetime
from src.services import (
    profitable_cashback_categories,
    investment_bank,
    simple_search,
    search_by_phone_numbers,
    search_person_transfers
)


class TestServices:
    @pytest.fixture
    def sample_transactions(self):
        return [
            {
                'date': datetime(2024, 3, 15),
                'amount': -1000.0,
                'category': 'Супермаркеты',
                'description': 'Покупка в магазине'
            },
            {
                'date': datetime(2024, 3, 10),
                'amount': -500.0,
                'category': 'Рестораны',
                'description': 'Ужин в кафе'
            }
        ]

    def test_profitable_cashback_categories(self, sample_transactions):
        result = profitable_cashback_categories(sample_transactions, 2024, 3)
        assert 'Супермаркеты' in result
        assert result['Супермаркеты'] == 10.0

    def test_simple_search(self, sample_transactions):
        result = simple_search('магазин', sample_transactions)
        assert len(result) == 1
        assert result[0]['description'] == 'Покупка в магазине'