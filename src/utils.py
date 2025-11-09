"""Utility functions for data loading, API calls, and date operations for bank_feature."""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_transactions_from_excel(file_path: str) -> pd.DataFrame:
    """
    Load transactions from Excel file for bank_feature.

    Args:
        file_path: Path to Excel file

    Returns:
        DataFrame with transactions
    """
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Successfully loaded {len(df)} transactions from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading transactions from {file_path}: {str(e)}")
        raise


def load_user_settings() -> Dict[str, Any]:
    """
    Load user settings from JSON file for bank_feature.

    Returns:
        Dictionary with user settings
    """
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        logger.info("Successfully loaded user settings")
        return settings
    except Exception as e:
        logger.error(f"Error loading user settings: {str(e)}")
        return {"user_currencies": [], "user_stocks": []}


def get_greeting_by_time(datetime_str: str) -> str:
    """
    Get greeting based on time of day for bank_feature.

    Args:
        datetime_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Greeting string
    """
    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        hour = dt.hour

        if 5 <= hour < 12:
            return "Доброе утро"
        elif 12 <= hour < 17:
            return "Добрый день"
        elif 17 <= hour < 22:
            return "Добрый вечер"
        else:
            return "Доброй ночи"
    except Exception as e:
        logger.error(f"Error parsing datetime {datetime_str}: {str(e)}")
        return "Добрый день"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Get current currency exchange rates for bank_feature.

    Args:
        currencies: List of currency codes

    Returns:
        List of currency rates
    """
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        logger.warning("Exchange rate API key not found, using fallback rates")
        # Fallback rates
        fallback_rates = {"USD": 75.0, "EUR": 85.0}
        return [
            {"currency": currency, "rate": fallback_rates.get(currency, 1.0)}
            for currency in currencies
        ]

    try:
        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": api_key}
        params = {"base": "RUB", "symbols": ",".join(currencies)}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        rates = data.get('rates', {})

        return [
            {"currency": currency, "rate": round(1 / rates.get(currency, 1.0), 2)}
            for currency in currencies
            if currency in rates
        ]
    except Exception as e:
        logger.error(f"Error fetching currency rates: {str(e)}")
        fallback_rates = {"USD": 75.0, "EUR": 85.0}
        return [
            {"currency": currency, "rate": fallback_rates.get(currency, 1.0)}
            for currency in currencies
        ]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """
    Get current stock prices for bank_feature.

    Args:
        stocks: List of stock symbols

    Returns:
        List of stock prices
    """
    api_key = os.getenv('STOCK_API_KEY')
    if not api_key:
        logger.warning("Stock API key not found, using fallback prices")
        # Fallback prices
        fallback_prices = {
            "AAPL": 150.0, "AMZN": 130.0, "GOOGL": 140.0,
            "MSFT": 300.0, "TSLA": 200.0
        }
        return [
            {"stock": stock, "price": fallback_prices.get(stock, 100.0)}
            for stock in stocks
        ]

    try:
        # Using Alpha Vantage API as example
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "apikey": api_key,
            "datatype": "json"
        }

        results = []
        for stock in stocks:
            try:
                params["symbol"] = stock
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                quote = data.get('Global Quote', {})
                price = float(quote.get('05. price', 100.0))

                results.append({"stock": stock, "price": round(price, 2)})
            except Exception as e:
                logger.error(f"Error fetching price for {stock}: {str(e)}")
                results.append({"stock": stock, "price": 100.0})

        return results
    except Exception as e:
        logger.error(f"Error fetching stock prices: {str(e)}")
        fallback_prices = {
            "AAPL": 150.0, "AMZN": 130.0, "GOOGL": 140.0,
            "MSFT": 300.0, "TSLA": 200.0
        }
        return [
            {"stock": stock, "price": fallback_prices.get(stock, 100.0)}
            for stock in stocks
        ]


def get_date_range(date_str: str, period: str = "M") -> tuple[str, str]:
    """
    Get date range for analysis for bank_feature.

    Args:
        date_str: Date string in format 'YYYY-MM-DD'
        period: Period type (W, M, Y, ALL)

    Returns:
        Tuple of (start_date, end_date)
    """
    try:
        end_date = datetime.strptime(date_str, '%Y-%m-%d')

        if period == "W":  # Week
            start_date = end_date - timedelta(days=end_date.weekday())
        elif period == "M":  # Month
            start_date = end_date.replace(day=1)
        elif period == "Y":  # Year
            start_date = end_date.replace(month=1, day=1)
        elif period == "ALL":  # All data
            start_date = datetime(2000, 1, 1)  # Very early date
        else:
            raise ValueError(f"Invalid period: {period}")

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    except Exception as e:
        logger.error(f"Error calculating date range: {str(e)}")
        return date_str, date_str


def filter_transactions_by_date(
    transactions: pd.DataFrame,
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Filter transactions by date range for bank_feature.

    Args:
        transactions: DataFrame with transactions
        start_date: Start date string
        end_date: End date string

    Returns:
        Filtered DataFrame
    """
    try:
        if 'date' not in transactions.columns:
            return transactions

        mask = (transactions['date'] >= start_date) & (transactions['date'] <= end_date)
        return transactions[mask].copy()
    except Exception as e:
        logger.error(f"Error filtering transactions by date: {str(e)}")
        return transactions
