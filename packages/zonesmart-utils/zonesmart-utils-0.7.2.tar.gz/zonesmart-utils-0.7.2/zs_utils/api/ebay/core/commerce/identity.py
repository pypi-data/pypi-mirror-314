from zs_utils.api.ebay.base_api import EbayAPI


class GetUser(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/identity/resources/user/methods/getUser
    """

    production_api_url = "https://apiz.ebay.com/"
    sandbox_api_url = "https://apiz.sandbox.ebay.com/"
    resource_method = "commerce/identity/v1/user"
    http_method = "GET"
