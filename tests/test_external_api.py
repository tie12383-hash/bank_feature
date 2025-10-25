"""Tests for external_api module."""

import os
from typing import Dict, Any
from unittest.mock import Mock, patch
import pytest
import requests
from src.external_api import ExchangeRateAPI, convert_amount_to_rubles, get_transaction_amount_in_rubles


class TestExchangeRateAPI:
    """Test class for ExchangeRateAPI."""

    def test_init_without_api_key(self) -> None:
        """Test initialization without API key."""
        with patch.dict(os.environ, {}, clear=True):
            api = ExchangeRateAPI()
            assert api.api_key is None

    def test_init_with_api_key(self) -> None:
        """Test initialization with API key."""
        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            api = ExchangeRateAPI()
            assert api.api_key == 'test_key'

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get: Mock) -> None:
        """Test successful exchange rate retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': True,
            'rates': {'RUB': 75.5}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            api = ExchangeRateAPI()
            rate = api.get_exchange_rate('USD', 'RUB')

            assert rate == 75.5
            mock_get.assert_called_once()

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_api_failure(self, mock_get: Mock) -> None:
        """Test exchange rate retrieval when API returns failure."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': False,
            'error': 'Invalid API key'
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            api = ExchangeRateAPI()
            rate = api.get_exchange_rate('USD', 'RUB')

            assert rate is None

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_request_exception(self, mock_get: Mock) -> None:
        """Test exchange rate retrieval when request fails."""
        mock_get.side_effect = requests.RequestException("Network error")

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            api = ExchangeRateAPI()
            rate = api.get_exchange_rate('USD', 'RUB')

            assert rate is None

    def test_get_exchange_rate_no_api_key(self) -> None:
        """Test exchange rate retrieval without API key."""
        with patch.dict(os.environ, {}, clear=True):
            api = ExchangeRateAPI()
            with pytest.raises(ValueError, match="EXCHANGE_RATE_API_KEY not found"):
                api.get_exchange_rate('USD', 'RUB')


class TestConvertAmountToRubles:
    """Test class for convert_amount_to_rubles function."""

    def test_rub_transaction(self) -> None:
        """Test RUB transaction (no conversion needed)."""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {
                    "code": "RUB",
                    "name": "руб."
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 1000.50

    @patch('src.external_api.ExchangeRateAPI.get_exchange_rate')
    def test_usd_transaction(self, mock_get_rate: Mock) -> None:
        """Test USD transaction with successful conversion."""
        mock_get_rate.return_value = 75.5

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "code": "USD",
                    "name": "US Dollar"
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 7550.0
        mock_get_rate.assert_called_once_with('USD', 'RUB')

    @patch('src.external_api.ExchangeRateAPI.get_exchange_rate')
    def test_eur_transaction(self, mock_get_rate: Mock) -> None:
        """Test EUR transaction with successful conversion."""
        mock_get_rate.return_value = 85.2

        transaction = {
            "operationAmount": {
                "amount": "50.0",
                "currency": {
                    "code": "EUR",
                    "name": "Euro"
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 4260.0  # 50 * 85.2
        mock_get_rate.assert_called_once_with('EUR', 'RUB')

    @patch('src.external_api.ExchangeRateAPI.get_exchange_rate')
    def test_usd_transaction_api_failure(self, mock_get_rate: Mock) -> None:
        """Test USD transaction when API fails (uses fallback)."""
        mock_get_rate.return_value = None

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "code": "USD",
                    "name": "US Dollar"
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 7500.0

    @patch('src.external_api.ExchangeRateAPI.get_exchange_rate')
    def test_eur_transaction_api_failure(self, mock_get_rate: Mock) -> None:
        """Test EUR transaction when API fails (uses fallback)."""
        mock_get_rate.return_value = None

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "code": "EUR",
                    "name": "Euro"
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 8500.0

    def test_unknown_currency(self) -> None:
        """Test transaction with unknown currency (no conversion)."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {
                    "code": "GBP",
                    "name": "British Pound"
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 100.0

    def test_invalid_amount_format(self) -> None:
        """Test transaction with invalid amount format."""
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {
                    "code": "USD",
                    "name": "US Dollar"
                }
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 0.0

    def test_missing_operation_amount(self) -> None:
        """Test transaction missing operationAmount."""
        transaction = {
            "id": 1,
            "state": "EXECUTED"
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 0.0

    def test_missing_currency(self) -> None:
        """Test transaction missing currency info."""
        transaction = {
            "operationAmount": {
                "amount": "100.0"
            }
        }

        result = convert_amount_to_rubles(transaction)
        assert result == 100.0


class TestGetTransactionAmountInRubles:
    """Test class for get_transaction_amount_in_rubles function."""

    def test_wrapper_function(self) -> None:
        """Test that wrapper function calls convert_amount_to_rubles."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "RUB"}
            }
        }

        result = get_transaction_amount_in_rubles(transaction)
        assert result == 100.0


class TestIntegration:
    """Integration tests for the modules."""

    @patch('src.external_api.ExchangeRateAPI.get_exchange_rate')
    def test_full_workflow(self, mock_get_rate: Mock) -> None:
        """Test full workflow: read JSON -> filter -> convert amounts."""
        mock_get_rate.return_value = 75.0

        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 2,
                "state": "CANCELED",
                "operationAmount": {
                    "amount": "200.0",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 3,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "300.0",
                    "currency": {"code": "RUB"}
                }
            }
        ]

        executed = [t for t in transactions if t.get('state') == 'EXECUTED']
        assert len(executed) == 2

        amounts = [convert_amount_to_rubles(t) for t in executed]
        assert amounts == [7500.0, 300.0]