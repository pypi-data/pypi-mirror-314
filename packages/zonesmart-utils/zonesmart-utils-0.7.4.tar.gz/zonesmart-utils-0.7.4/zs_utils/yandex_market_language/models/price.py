from typing import Optional

from .abstract import AbstractModel, XMLElement


class AbstractPrice(AbstractModel):
    tag_name = None

    __slots__ = ["_value", "_is_starting"]

    def __init__(self, value=None, is_starting=False):
        if not self.tag_name:
            raise ValueError("Необходимо определить атрибут 'tag_name'.")

        self.value = value
        self.is_starting = is_starting

    @property
    def is_starting(self) -> Optional[bool]:
        return self._str_to_bool(self._is_starting)

    @is_starting.setter
    def is_starting(self, value):
        self._is_starting = self._is_valid_bool(value, "is_starting", True)

    @property
    def value(self) -> float:
        return float(self._value)

    @value.setter
    def value(self, v):
        if isinstance(v, str):
            v = v.replace(",", ".")
        self._value = self._is_valid_float(v, self.tag_name)

    def create_dict(self, **kwargs) -> dict:
        return dict(value=self.value, is_starting=self.is_starting)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement(self.tag_name)

        if self.is_starting:
            el.attrib["from"] = "true"

        el.text = self._value
        return el

    @classmethod
    def from_xml(cls, el: XMLElement) -> "AbstractModel":
        return cls(el.text, el.attrib.get("from", False))


class Price(AbstractPrice):
    """
    Actual offer price model.
    """

    tag_name = "price"


class OldPrice(AbstractPrice):
    """
    Actual offer price model.
    """

    tag_name = "oldprice"
