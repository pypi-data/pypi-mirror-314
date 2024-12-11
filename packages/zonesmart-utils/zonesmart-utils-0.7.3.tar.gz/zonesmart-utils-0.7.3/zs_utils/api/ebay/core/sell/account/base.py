from zs_utils.api.ebay.base_api import EbayAPI


class GetPrivileges(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/privilege/methods/getPrivileges
    """

    http_method = "GET"
    resource_method = "sell/account/v1/privilege"
