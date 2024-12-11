from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetFeedbackList",
]


class GetFeedbackList(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetFeedback.html
    """

    method_name = "GetFeedback"

    def get_params(self, **kwargs):
        return {
            "DetailLevel": "ReturnAll",
            "Pagination": {
                "EntriesPerPage": 200,
                "PageNumber": kwargs["page"],
            },
        }
