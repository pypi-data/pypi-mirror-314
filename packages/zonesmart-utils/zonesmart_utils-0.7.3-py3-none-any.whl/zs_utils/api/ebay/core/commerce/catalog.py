from zs_utils.api.ebay.base_api import EbayAPI


class GetProduct(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/catalog/resources/product/methods/getProduct
    """

    http_method = "GET"
    resource_method = "commerce/catalog/v1_beta/product/{epid}"
    required_params = ["epid"]


class SearchProduct(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/catalog/resources/product_summary/methods/search
    """

    http_method = "GET"
    resource_method = "commerce/catalog/v1_beta/product_summary/search"
    allowed_params = [
        "q",
        "gtin",
        "mpn",
        "category_ids",
        "limit",
        "offset",
    ]
