#!/usr/bin/env python
# coding=utf-8

"""Converter object to handle string input."""

from decimal import Decimal as D

from zs_utils.unit_converter.parser import QuantityParser, UnitParser


def convertd(quantity: str, desired_unit: str) -> D:
    """

    :param quantity:
    :param desired_unit:
    :return:

    Examples :
    ----------

    >>> from unit_converter import convert
    >>> convert('2.78 daN*mm^2', 'mN*µm^2')
    Decimal('2.78E+10')
    """
    quantity = QuantityParser().parse(quantity)
    desired_unit = UnitParser().parse(desired_unit)
    return quantity.convert(desired_unit).value


def converts(quantity: str, desired_unit: str) -> str:
    """

    :param quantity:
    :param desired_unit:
    :return:

    Examples :
    ----------

    >>> from unit_converter import converts
    >>> converts('2.78 daN*mm^2', 'mN*µm^2')
    '2.78E+10'
    """
    return str(convertd(quantity=quantity, desired_unit=desired_unit))


def convert(value: str, from_unit: str, to_unit: str) -> float:
    """

    :param value:
    :param from_unit:
    :param to_unit:
    :return:

    Examples :
    ----------

    >>> from unit_converter import convert
    >>> convertf('2.78', 'daN*mm^2', 'mN*µm^2')
    27800000000.0
    """

    # Тривиальные случаи
    if (float(value) == 0) or (from_unit == to_unit):
        return float(value)

    return float(convertd(quantity=f"{value} {from_unit}", desired_unit=to_unit))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
