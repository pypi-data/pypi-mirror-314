from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetStoreInfo",
]


class GetStoreInfo(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetStore.html
    """

    method_name = "GetStore"

    def get_params(self, category_structure_only: bool = False, **kwargs):
        return {
            "CategoryStructureOnly": category_structure_only,
        }
