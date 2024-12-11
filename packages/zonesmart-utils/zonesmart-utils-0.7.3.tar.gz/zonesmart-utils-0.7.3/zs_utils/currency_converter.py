import requests

from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext as _

from zs_utils.exceptions import CustomException


class CurrencyServiceError(CustomException):
    pass


def _convert_currency_by_coinlayer(from_currency: str, to_currency: str, amount: int = 1) -> float:
    """
    Docs: https://coinlayer.com/documentation
    Конвертация валют через сервис coinlayer
    """

    token = settings.COINLAYER_API_TOKEN
    url = (
        f"http://api.coinlayer.com/api/convert?access_key={token}&from={from_currency}&to={to_currency}&amount={amount}"
    )
    data = requests.get(url=url).json()

    if not data.get("success", True):
        message = _("Не удалось конвертировать валюту ({from_currency}-->{to_currency}): {error}").format(
            from_currency=from_currency,
            to_currency=to_currency,
            error=data.get("error", {}).get("info", "System error"),
        )
        raise CurrencyServiceError(message=message)

    return data["result"]


def _get_exchange_rate_cache_key(from_currency: str, to_currency: str):
    """
    Получения ключа кэша, в котором хранятся курсы валют
    """
    sorted_currencies = sorted([from_currency, to_currency])
    return f"exchange_rate_{sorted_currencies[0]}_{sorted_currencies[1]}"


def _get_exchange_rate_from_cache(from_currency: str, to_currency: str) -> float:
    """
    Получение курса валют из кэша
    """
    value = cache.get(key=_get_exchange_rate_cache_key(from_currency=from_currency, to_currency=to_currency))
    if value and (from_currency > to_currency):
        value = 1 / value
    return value


def _save_exchange_rate_in_cache(from_currency: str, to_currency: str, value: float) -> None:
    """
    Сохранение курса валют в кэш
    """
    assert value
    if from_currency > to_currency:
        value = 1 / value
    timeout = 0.5 * 60 * 60  # 0.5 часов
    cache.set(
        _get_exchange_rate_cache_key(from_currency=from_currency, to_currency=to_currency),
        value,
        timeout=timeout,
    )


def convert_amount(
    from_currency: str,
    to_currency: str,
    value: float,
    use_cache: bool = True,
) -> float:
    """
    Конвертация переданных валют, с возможностью использования кэша
    """
    if from_currency == "RUR":
        from_currency = "RUB"
    if to_currency == "RUR":
        to_currency = "RUB"

    # Тривиальный случай
    if (from_currency == to_currency) or (value == 0):
        return value

    coef = None

    # Получение сохраненного в кэше курса
    if use_cache:
        coef = _get_exchange_rate_from_cache(from_currency=from_currency, to_currency=to_currency)

    if not coef:
        coef = _convert_currency_by_coinlayer(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=1,
        )
        # Сохранение курса в кэш
        _save_exchange_rate_in_cache(from_currency=from_currency, to_currency=to_currency, value=coef)

    return round(value * coef, 5)


@classmethod
def is_greater(value1: float, currency1: str, value2: float, currency2: str) -> bool:
    """
    Метод для сравнения суммы в разных валютах
    """
    return convert_amount(from_currency=currency1, to_currency=currency2, value=value1) > value2
