from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyAccountInfo(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getUser
    """

    http_method = "GET"
    resource_method = "users/{user_id}"
    required_params = ["user_id"]
