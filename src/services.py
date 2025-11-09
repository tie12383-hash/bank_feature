"""Services for transaction analysis for bank_feature."""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def profitable_cashback_categories(
        transactions: List[Dict[str, Any]],
        year: int,
        month: int
) -> Dict[str, float]:
    """
    Analyze profitable cashback categories for bank_feature.

    Args:
        transactions: List of transaction dictionaries
        year: Year for analysis
        month: Month for analysis

    Returns:
        Dictionary with cashback amounts by category
    """
    logger.info(f"Analyzing cashback categories for {year}-{month}")

    try:
        df = pd.DataFrame(transactions)

        # Filter by date
        mask = (df['date'].dt.year == year) & (df['date'].dt.month == month)
        filtered_df = df[mask].copy()

        # Calculate cashback (1% for expenses)
        expenses_df = filtered_df[filtered_df['amount'] < 0].copy()
        expenses_df['cashback'] = expenses_df['amount'].abs() * 0.01

        # Group by category
        cashback_by_category = expenses_df.groupby('category')['cashback'].sum()

        return {
            category: round(amount, 2)
            for category, amount in cashback_by_category.items()
        }

    except Exception as e:
        logger.error(f"Error analyzing cashback categories: {str(e)}")
        return {}


def investment_bank(
        month: str,
        transactions: List[Dict[str, Any]],
        limit: int
) -> float:
    """
    Calculate investment bank amount for bank_feature.

    Args:
        month: Month in format 'YYYY-MM'
        transactions: List of transaction dictionaries
        limit: Rounding limit (10, 50, 100)

    Returns:
        Total investment amount
    """
    logger.info(f"Calculating investment bank for {month} with limit {limit}")

    try:
        df = pd.DataFrame(transactions)

        # Filter by month
        df['month'] = df['date'].dt.strftime('%Y-%m')
        month_df = df[df['month'] == month].copy()

        # Calculate rounding difference for expenses
        expenses_df = month_df[month_df['amount'] < 0].copy()
        expenses_df['rounded_amount'] = (
                (expenses_df['amount'].abs() / limit).ceil() * limit
        )
        expenses_df['investment'] = (
                expenses_df['rounded_amount'] - expenses_df['amount'].abs()
        )

        total_investment = expenses_df['investment'].sum()

        return round(total_investment, 2)

    except Exception as e:
        logger.error(f"Error calculating investment bank: {str(e)}")
        return 0.0


def simple_search(
        search_query: str,
        transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Simple search in transactions for bank_feature.

    Args:
        search_query: Search query string
        transactions: List of transaction dictionaries

    Returns:
        List of matching transactions
    """
    logger.info(f"Performing simple search for: {search_query}")

    try:
        results = []
        search_lower = search_query.lower()

        for transaction in transactions:
            description = str(transaction.get('description', '')).lower()
            category = str(transaction.get('category', '')).lower()

            if (search_lower in description) or (search_lower in category):
                results.append(transaction)

        return results

    except Exception as e:
        logger.error(f"Error performing simple search: {str(e)}")
        return []


def search_by_phone_numbers(
        transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Search transactions containing phone numbers for bank_feature.

    Args:
        transactions: List of transaction dictionaries

    Returns:
        List of transactions with phone numbers
    """
    logger.info("Searching transactions with phone numbers")

    try:
        # Regex pattern for Russian phone numbers
        phone_pattern = r'\+7\s?[\(]?\d{3}[\)]?\s?\d{3}[\-]?\d{2}[\-]?\d{2}'

        results = []
        for transaction in transactions:
            description = str(transaction.get('description', ''))
            if re.search(phone_pattern, description):
                results.append(transaction)

        return results

    except Exception as e:
        logger.error(f"Error searching phone numbers: {str(e)}")
        return []


def search_person_transfers(
        transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Search person-to-person transfers for bank_feature.

    Args:
        transactions: List of transaction dictionaries

    Returns:
        List of person transfer transactions
    """
    logger.info("Searching person-to-person transfers")

    try:
        # Pattern for names like "Имя Ф."
        name_pattern = r'[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.'

        results = []
        for transaction in transactions:
            category = str(transaction.get('category', ''))
            description = str(transaction.get('description', ''))

            if (category == 'Переводы' and
                    re.search(name_pattern, description)):
                results.append(transaction)

        return results

    except Exception as e:
        logger.error(f"Error searching person transfers: {str(e)}")
        return []