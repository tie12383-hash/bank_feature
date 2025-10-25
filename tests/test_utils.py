"""Tests for utils module."""

import json
import tempfile
import os
from typing import List, Dict, Any
import pytest
from src.utils import read_json_file, filter_executed_transactions, get_transaction_amount


class TestReadJsonFile:
    """Test class for read_json_file function."""

    def test_read_valid_json_file(self) -> None:
        """Test reading valid JSON file with transactions."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([
                {"id": 1, "state": "EXECUTED", "amount": "100.0"},
                {"id": 2, "state": "CANCELED", "amount": "200.0"}
            ], f)
            temp_file = f.name

        try:
            result = read_json_file(temp_file)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2
        finally:
            os.unlink(temp_file)

    def test_read_nonexistent_file(self) -> None:
        """Test reading non-existent file."""
        result = read_json_file("nonexistent_file.json")
        assert result == []

    def test_read_invalid_json(self) -> None:
        """Test reading invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name

        try:
            result = read_json_file(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)

    def test_read_empty_file(self) -> None:
        """Test reading empty JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("")
            temp_file = f.name

        try:
            result = read_json_file(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)

    def test_read_json_with_non_list(self) -> None:
        """Test reading JSON file that doesn't contain a list."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"id": 1, "name": "test"}, f)
            temp_file = f.name

        try:
            result = read_json_file(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)


class TestFilterExecutedTransactions:
    """Test class for filter_executed_transactions function."""

    @pytest.fixture
    def sample_transactions(self) -> List[Dict[str, Any]]:
        """Sample transactions for testing."""
        return [
            {"id": 1, "state": "EXECUTED", "amount": "100.0"},
            {"id": 2, "state": "CANCELED", "amount": "200.0"},
            {"id": 3, "state": "EXECUTED", "amount": "300.0"},
            {"id": 4, "state": "PENDING", "amount": "400.0"},
            {"id": 5, "state": "EXECUTED", "amount": "500.0"}
        ]

    def test_filter_executed(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Test filtering executed transactions."""
        result = filter_executed_transactions(sample_transactions)

        assert len(result) == 3
        assert all(t["state"] == "EXECUTED" for t in result)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3
        assert result[2]["id"] == 5

    def test_filter_empty_list(self) -> None:
        """Test filtering empty transactions list."""
        result = filter_executed_transactions([])
        assert result == []

    def test_filter_no_executed(self) -> None:
        """Test filtering when no executed transactions exist."""
        transactions = [
            {"id": 1, "state": "CANCELED"},
            {"id": 2, "state": "PENDING"}
        ]
        result = filter_executed_transactions(transactions)
        assert result == []

    def test_filter_missing_state(self) -> None:
        """Test filtering transactions with missing state field."""
        transactions = [
            {"id": 1, "state": "EXECUTED"},
            {"id": 2},  # Missing state
            {"id": 3, "state": "EXECUTED"}
        ]
        result = filter_executed_transactions(transactions)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3


class TestGetTransactionAmount:
    """Test class for get_transaction_amount function."""

    def test_valid_amount(self) -> None:
        """Test getting valid amount from transaction."""
        transaction = {
            "operationAmount": {
                "amount": "123.45",
                "currency": {"code": "RUB"}
            }
        }
        result = get_transaction_amount(transaction)
        assert result == 123.45

    def test_missing_operation_amount(self) -> None:
        """Test transaction missing operationAmount."""
        transaction = {"id": 1, "state": "EXECUTED"}
        result = get_transaction_amount(transaction)
        assert result == 0.0

    def test_missing_amount(self) -> None:
        """Test transaction missing amount."""
        transaction = {
            "operationAmount": {
                "currency": {"code": "RUB"}
            }
        }
        result = get_transaction_amount(transaction)
        assert result == 0.0

    def test_invalid_amount_format(self) -> None:
        """Test transaction with invalid amount format."""
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {"code": "RUB"}
            }
        }
        result = get_transaction_amount(transaction)
        assert result is None

    @pytest.mark.parametrize("amount_str, expected", [
        ("100.50", 100.5),
        ("0", 0.0),
        ("-50.25", -50.25),
        ("1234567.89", 1234567.89),
    ])
    def test_various_amount_formats(self, amount_str: str, expected: float) -> None:
        """Test various amount string formats."""
        transaction = {
            "operationAmount": {
                "amount": amount_str,
                "currency": {"code": "RUB"}
            }
        }
        result = get_transaction_amount(transaction)
        assert result == expected