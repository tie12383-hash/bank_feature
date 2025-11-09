"""Web page views for generating JSON responses for bank_feature."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from .utils import (
    get_greeting_by_time,
    get_currency_rates,
    get_stock_prices,
    load_user_settings,
    get_date_range,
    filter_transactions_by_date
)

logger = logging.getLogger(__name__)


def main_page_data(datetime_str: str, transactions: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate data for main page for bank_feature.

    Args:
        datetime_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'
        transactions: DataFrame with transactions

    Returns:
        Dictionary with main page data
    """
    logger.info(f"Generating main page data for {datetime_str}")

    try:
        # Greeting
        greeting = get_greeting_by_time(datetime_str)

        # Cards data (assuming card number in 'card_number' column)
        cards_data = []
        if 'card_number' in transactions.columns and 'amount' in transactions.columns:
            card_transactions = transactions[transactions['card_number'].notna()]
            for card in card_transactions['card_number'].unique():
                card_data = card_transactions[card_transactions['card_number'] == card]
                total_spent = card_data[card_data['amount'] > 0]['amount'].sum()
                cashback = total_spent * 0.01  # 1% cashback

                cards_data.append({
                    "last_digits": str(card)[-4:],
                    "total_spent": round(total_spent, 2),
                    "cashback": round(cashback, 2)
                })

        # Top 5 transactions by amount
        top_transactions = []
        if not transactions.empty and 'amount' in transactions.columns:
            top_5 = transactions.nlargest(5, 'amount')[['date', 'amount', 'category', 'description']]
            for _, row in top_5.iterrows():
                top_transactions.append({
                    "date": row['date'].strftime('%d.%m.%Y') if hasattr(row['date'], 'strftime') else str(row['date']),
                    "amount": round(float(row['amount']), 2),
                    "category": str(row.get('category', 'N/A')),
                    "description": str(row.get('description', 'N/A'))
                })

        # Currency rates and stock prices from user settings
        settings = load_user_settings()
        currency_rates = get_currency_rates(settings.get('user_currencies', []))
        stock_prices = get_stock_prices(settings.get('user_stocks', []))

        return {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

    except Exception as e:
        logger.error(f"Error generating main page data: {str(e)}")
        return {
            "greeting": "Добрый день",
            "cards": [],
            "top_transactions": [],
            "currency_rates": [],
            "stock_prices": []
        }


def events_page_data(
        date_str: str,
        transactions: pd.DataFrame,
        period: str = "M"
) -> Dict[str, Any]:
    """
    Generate data for events page for bank_feature.

    Args:
        date_str: Date string in format 'YYYY-MM-DD'
        transactions: DataFrame with transactions
        period: Period type (W, M, Y, ALL)

    Returns:
        Dictionary with events page data
    """
    logger.info(f"Generating events page data for {date_str} with period {period}")

    try:
        # Get date range
        start_date, end_date = get_date_range(date_str, period)
        filtered_transactions = filter_transactions_by_date(
            transactions, start_date, end_date
        )

        if filtered_transactions.empty:
            return {
                "expenses": {"total_amount": 0, "main": [], "transfers_and_cash": []},
                "income": {"total_amount": 0, "main": []},
                "currency_rates": [],
                "stock_prices": []
            }

        # Expenses
        expenses_df = filtered_transactions[filtered_transactions['amount'] < 0].copy()
        expenses_df['amount'] = expenses_df['amount'].abs()
        total_expenses = int(expenses_df['amount'].sum())

        # Main expense categories (top 6 + others)
        expense_by_category = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        main_expenses = []
        other_expenses = 0

        for i, (category, amount) in enumerate(expense_by_category.items()):
            if i < 6:
                main_expenses.append({
                    "category": str(category),
                    "amount": int(amount)
                })
            else:
                other_expenses += amount

        if other_expenses > 0:
            main_expenses.append({
                "category": "Остальное",
                "amount": int(other_expenses)
            })

        # Transfers and cash
        transfers_cash_categories = ['Наличные', 'Переводы']
        transfers_and_cash = []
        for category in transfers_cash_categories:
            if category in expense_by_category:
                transfers_and_cash.append({
                    "category": category,
                    "amount": int(expense_by_category[category])
                })

        # Income
        income_df = filtered_transactions[filtered_transactions['amount'] > 0].copy()
        total_income = int(income_df['amount'].sum())

        income_by_category = income_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        main_income = [
            {
                "category": str(category),
                "amount": int(amount)
            }
            for category, amount in income_by_category.items()
        ]

        # Currency rates and stock prices
        settings = load_user_settings()
        currency_rates = get_currency_rates(settings.get('user_currencies', []))
        stock_prices = get_stock_prices(settings.get('user_stocks', []))

        return {
            "expenses": {
                "total_amount": total_expenses,
                "main": main_expenses,
                "transfers_and_cash": transfers_and_cash
            },
            "income": {
                "total_amount": total_income,
                "main": main_income
            },
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

    except Exception as e:
        logger.error(f"Error generating events page data: {str(e)}")
        return {
            "expenses": {"total_amount": 0, "main": [], "transfers_and_cash": []},
            "income": {"total_amount": 0, "main": []},
            "currency_rates": [],
            "stock_prices": []
