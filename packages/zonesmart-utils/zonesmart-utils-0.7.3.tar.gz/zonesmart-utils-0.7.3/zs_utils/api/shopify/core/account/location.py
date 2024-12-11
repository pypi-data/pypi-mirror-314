from zs_utils.api.shopify.base_api import ShopifyAPI


class GetShopifyLocationListAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/location#get-locations
    """

    http_method = "GET"
    resource_method = "locations.json"


class GetShopifyLocationAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/location#get-locations-location-id
    """

    http_method = "GET"
    resource_method = "locations/{location_id}.json"
    required_params = ["location_id"]
