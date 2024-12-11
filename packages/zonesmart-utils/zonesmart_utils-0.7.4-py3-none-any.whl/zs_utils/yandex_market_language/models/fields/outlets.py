__all__ = [
    "OutletsField",
]


class OutletsField:
    _outlets = []

    @property
    def outlets(self):
        return self._outlets

    @outlets.setter
    def outlets(self, outlets: list):
        self._outlets = outlets if outlets else []
