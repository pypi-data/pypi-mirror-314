from zs_utils.api.shopify.base_api import ShopifyAPI


class GetShopifyShopInfoAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/shop#get-shop?fields=address1,address2,city,province,country
    """

    http_method = "GET"
    resource_method = "shop.json"
    allowed_params = ["fields"]  # address1,address2,city,province,country
