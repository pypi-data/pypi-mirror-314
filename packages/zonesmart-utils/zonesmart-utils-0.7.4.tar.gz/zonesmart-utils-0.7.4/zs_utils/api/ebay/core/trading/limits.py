from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetAPILimits",
]


class GetAPILimits(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetApiAccessRules.html
    """

    method_name = "GetApiAccessRules"

    def get_params(self, **kwargs):
        return {}
