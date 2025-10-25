"""Module for external API calls, specifically for currency conversion."""

import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class ExchangeRateAPI:
    """Class for handling exchange rate API operations."""

    def __init__(self) -> None:
        """Initialize API with credentials from environment variables."""
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        self.base_url = "https://api.apilayer.com/exchangerates_data"

    def get_exchange_rate(self, from_currency: str, to_currency: str = "RUB") -> Optional[float]:
        """Get current exchange rate from external API."""
        if not self.api_key:
            raise ValueError("EXCHANGE_RATE_API_KEY not found in environment variables")

        url = f"{self.base_url}/latest"
        headers = {"apikey": self.api_key}
        params = {"base": from_currency, "symbols": to_currency}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("success", False):
                rates = data.get("rates", {})
                rate = rates.get(to_currency)
                return float(rate) if rate is not None else None
            else:
                return None

        except (requests.RequestException, KeyError, ValueError, TypeError):
            return None


def convert_amount_to_rubles(transaction: Dict[str, Any]) -> float:
    """Convert transaction amount to rubles."""
    api = ExchangeRateAPI()

    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_info = operation_amount.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        exchange_rate = api.get_exchange_rate(currency_code, "RUB")
        if exchange_rate:
            return amount * exchange_rate
        else:
            fallback_rates = {"USD": 75.0, "EUR": 85.0}
            return amount * fallback_rates.get(currency_code, 1.0)

    return amount


def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """Simplified function to get transaction amount in rubles."""
    return convert_amount_to_rubles(transaction)
