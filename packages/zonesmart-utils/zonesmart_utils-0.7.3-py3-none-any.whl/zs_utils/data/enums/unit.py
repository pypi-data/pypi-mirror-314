from django.utils.translation import gettext_lazy as _

from model_utils import Choices


__all__ = [
    "WEIGHT_UNITS",
    "ENGLISH_WEIGHT_UNITS",
    "METRIC_WEIGHT_UNITS",
    "LENGTH_UNITS",
    "ENGLISH_LENGTH_UNITS",
    "METRIC_LENGTH_UNITS",
]


WEIGHT_UNITS = Choices(
    ("G", _("Грамм")),
    ("KG", _("Килограмм")),
    ("LB", _("Фунт")),
    ("OZ", _("Унция")),
)

ENGLISH_WEIGHT_UNITS = WEIGHT_UNITS.subset("LB", "OZ")

METRIC_WEIGHT_UNITS = WEIGHT_UNITS.subset("G", "KG")

LENGTH_UNITS = Choices(
    ("IN", _("Дюйм")),
    ("FT", _("Фут")),
    ("YD", _("Ярд")),
    ("MM", _("Миллиметр")),
    ("CM", _("Сантиметр")),
    ("M", _("Метр")),
)

ENGLISH_LENGTH_UNITS = LENGTH_UNITS.subset("IN", "FT", "YD")

METRIC_LENGTH_UNITS = LENGTH_UNITS.subset("MM", "CM", "M")
