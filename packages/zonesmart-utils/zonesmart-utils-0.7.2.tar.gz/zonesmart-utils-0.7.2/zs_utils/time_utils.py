import datetime
import pytils

from django.utils import timezone


def now():
    return timezone.now()


def current_date():
    return now().date()


def days_ago_to_dates(days_ago: int, discard_time: bool = False):
    datetime_now = now()
    dates = {
        "date_before": datetime_now,
        "date_after": datetime_now - timezone.timedelta(days=int(days_ago)),
    }

    if discard_time:
        for key, value in dates.items():
            dates[key] = value.date()

    return dates


def from_datetime_str(value: str):
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return timezone.datetime.fromisoformat(value)


def datetime_str_to_date_str(value: str):
    return str(from_datetime_str(value).date())


def datetime_to_tsz(value) -> float:
    return timezone.datetime.timestamp(value)


def tsz_to_datetime(tsz, to_str=False, isoformat=False):
    dtm = timezone.make_aware(timezone.datetime.utcfromtimestamp(tsz), timezone=datetime.timezone.utc)
    if to_str:
        if isoformat:
            dtm = dtm.isoformat()
        else:
            dtm = dtm.strftime("%Y-%m-%d %H:%M:%S")
    return dtm


def datetime_to_words(value: timezone.timedelta, lang: str):
    seconds = int(value.total_seconds())
    periods = [
        ({"en": "year", "ru": ("год", "года", "лет")}, 60 * 60 * 24 * 365),
        ({"en": "month", "ru": ("месяц", "месяца", "месяцев")}, 60 * 60 * 24 * 30),
        ({"en": "day", "ru": ("день", "дня", "дней")}, 60 * 60 * 24),
        ({"en": "hour", "ru": ("час", "часа", "часов")}, 60 * 60),
        ({"en": "minute", "ru": ("минута", "минуты", "минут")}, 60),
        ({"en": "second", "ru": ("секунда", "секунды", "секунд")}, 1),
    ]

    strings = []
    for period_names, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if lang == "ru":
                strings.append(pytils.numeral.get_plural(amount=period_value, variants=period_names[lang]))
            elif lang == "en":
                has_s = "s" if period_value > 1 else ""
                strings.append("%s %s%s" % (period_value, period_names[lang], has_s))
            else:
                raise ValueError("Недопустимый язык 'lang'.")

    return ", ".join(strings)
