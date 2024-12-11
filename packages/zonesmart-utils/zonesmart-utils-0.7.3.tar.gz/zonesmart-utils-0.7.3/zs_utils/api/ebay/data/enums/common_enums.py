from model_utils import Choices
from zs_utils.data.enums import COUNTRIES

from django.utils.translation import gettext_lazy as _


WeightUnitOfMeasureEnum = Choices(
    ("POUND", _("Фунт")),
    ("KILOGRAM", _("Килограмм")),
    ("OUNCE", _("Унция")),
    ("GRAM", _("Грамм")),
)

LengthUnitOfMeasureEnum = Choices(
    ("INCH", _("Дюйм")),
    ("FEET", _("Фут")),
    ("CENTIMETER", _("Сантиметр")),
    ("METER", _("Метр")),
)

TimeDurationUnitEnum = Choices(
    ("YEAR", _("Год")),
    ("MONTH", _("Месяц")),
    ("DAY", _("День")),
    ("HOUR", _("Час")),
    ("CALENDAR_DAY", _("Календарный день")),
    ("BUSINESS_DAY", _("Рабочий день")),
    ("MINUTE", _("Минута")),
    ("SECOND", _("Секунда")),
    ("MILLISECOND", _("Миллисекунда")),
)

DayOfWeekEnum = Choices(
    ("MONDAY", _("Понедельник")),
    ("TUESDAY", _("Вторник")),
    ("WEDNESDAY", _("Среда")),
    ("THURSDAY", _("Четверг")),
    ("FRIDAY", _("Пятница")),
    ("SATURDAY", _("Суббота")),
    ("SUNDAY", _("Воскресенье")),
)

EbayCountryCodeEnum = COUNTRIES.subset(
    "US",
    "CA",
    "DE",
    "ES",
    "FR",
    "GB",
    "IT",
    "AU",
    "JP",
    "CN",
    "BR",
    "MX",
    "IN",
    "TR",
    "TR",
    "AE",
    "AE",
    "SG",
)
