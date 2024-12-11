from zs_utils.api.etsy.base_api import EtsyAPI


class FindAllShops(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/findShops
    """

    http_method = "GET"
    resource_method = "shops"
    required_params = ["shop_name"]
    allowed_params = ["limit", "offset"]


class GetEtsyShopByUserId(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/getShopByOwnerUserId
    """

    http_method = "GET"
    resource_method = "users/{user_id}/shops"
    required_params = ["user_id"]


class GetEtsyShop(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/getShop
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}"
    required_params = ["shop_id"]


class UpdateEtsyShop(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/updateShop
    """

    http_method = "PUT"
    resource_method = "shops/{shop_id}"
    required_params = ["shop_id"]
    allowed_params = [
        "title",
        "announcement",
        "sale_message",
        "digital_sale_message",
    ]
