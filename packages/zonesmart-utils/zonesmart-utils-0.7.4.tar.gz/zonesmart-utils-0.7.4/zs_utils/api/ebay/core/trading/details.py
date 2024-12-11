from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetEbayDetails",
]


class GetEbayDetails(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GeteBayDetails.html
    Available detail names:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/types/DetailNameCodeType.html
    """

    method_name = "GeteBayDetails"

    def get_params(self, detail_names: list, **kwargs):
        if detail_names:
            if not isinstance(detail_names, list):
                detail_names = [detail_names]
        else:
            raise AttributeError('Необходимо задать параметр "detail_names"')

        return {"DetailName": detail_names}
