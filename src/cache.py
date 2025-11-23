from functools import lru_cache
from datetime import datetime, timedelta


@lru_cache(maxsize=100)
def get_cached_currency_rates(currencies_str: str, timestamp: int) -> List[Dict[str, Any]]:
    """Кэширование курсов валют на 1 час"""
    currencies = currencies_str.split(',')
    # вызов реального API
    return get_currency_rates_impl(currencies)


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    cache_key = ",".join(sorted(currencies)), int(current_hour.timestamp())

    return get_cached_currency_rates(*cache_key)