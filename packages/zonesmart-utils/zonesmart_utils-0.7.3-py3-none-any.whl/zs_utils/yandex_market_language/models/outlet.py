from .abstract import AbstractModel, XMLElement


class Outlet(AbstractModel):
    """
    Используйте элемент outlets, чтобы указать:
    1) количество товара, доступное в конкретной точке продаж;
    2) цены, которые действуют в конкретных точках и отличаются от цены в большинстве точек.

    Docs:
    https://yandex.ru/support/edadeal-partner/pricelist/outlets.html
    """

    __slots__ = ["id", "instock"]

    def __init__(self, id: str = None, instock: int = 0):
        self.id = id
        self.instock = instock

    def create_dict(self, **kwargs) -> dict:
        return dict(id=self.id, instock=self.instock)

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"id": self.id, "instock": self.instock}
        el = XMLElement("outlet", attrib=attribs)
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Outlet":
        return Outlet(**el.attrib)
