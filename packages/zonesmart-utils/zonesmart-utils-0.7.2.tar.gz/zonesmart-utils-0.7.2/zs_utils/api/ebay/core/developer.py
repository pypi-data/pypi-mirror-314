from zs_utils.api.ebay.base_api import EbayAPI


class GetAppRateLimits(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/developer/analytics/resources/rate_limit/methods/getRateLimits
    """

    http_method = "GET"
    resource_method = "developer/analytics/v1_beta/rate_limit"
    allowed_params = ["api_name", "api_context"]


class GetUserRateLimits(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/developer/analytics/resources/user_rate_limit/methods/getUserRateLimits
    """

    http_method = "GET"
    resource_method = "developer/analytics/v1_beta/user_rate_limit"
    allowed_params = ["api_name", "api_context"]
