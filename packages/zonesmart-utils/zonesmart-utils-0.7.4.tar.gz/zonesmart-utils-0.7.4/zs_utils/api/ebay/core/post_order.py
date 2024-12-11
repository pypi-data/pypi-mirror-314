from zs_utils.api.ebay.base_api import EbayAPI


class PostOrderAPI(EbayAPI):
    @property
    def headers(self):
        return {
            "Authorization": f"IAF {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
        }


class SearchCancellations(PostOrderAPI):
    """
    Docs: https://developer.ebay.com/Devzone/post-order/post-order_v2_cancellation_search__get.html
    """

    resource_method = "post-order/v2/cancellation/search"
    http_method = "GET"
    allowed_params = [
        "limit",
        "offset",
        "role",
        "creation_date_range_from",
        "creation_date_range_to",
        "cancel_id",
        "item_id",
        "legacy_order_id",
        "transaction_id",
        "sort",
    ]


class SearchReturns(PostOrderAPI):
    """
    Docs: https://developer.ebay.com/devzone/post-order/post-order_v2_return_search__get.html
    """

    resource_method = "post-order/v2/return/search"
    http_method = "GET"
    allowed_params = [
        "limit",
        "offset",
        "creation_date_range_from",
        "creation_date_range_to",
        "role",
        "item_id",
        "order_id",
        "return_id",
        "return_state",
        "sort",
        "states",
        "transaction_id",
    ]


class CancelOrder(PostOrderAPI):
    """
    Docs: https://developer.ebay.com/devzone/post-order/post-order_v2_cancellation__post.html#Samples
    """

    resource_method = "post-order/v2/cancellation"
    http_method = "POST"


class CheckOrderCancellationEligibility(PostOrderAPI):
    """
    Docs: https://developer.ebay.com/devzone/post-order/post-order_v2_cancellation_check_eligibility__post.html#Samples
    """

    resource_method = "post-order/v2/cancellation/check_eligibility"
    http_method = "POST"
