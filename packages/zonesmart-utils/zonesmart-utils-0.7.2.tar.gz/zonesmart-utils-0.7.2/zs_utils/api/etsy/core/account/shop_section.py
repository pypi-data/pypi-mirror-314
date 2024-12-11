from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyShopSectionList(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/getShopSections
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/sections"
    required_params = ["shop_id"]


class GetEtsyShopSection(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/getShopSection
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/sections/{shop_section_id}"
    required_params = ["shop_id", "shop_section_id"]


class CreateEtsyShopSection(EtsyAPI):
    """
    https://www.etsy.com/openapi/developers#operation/createShopSection
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/sections"
    required_params = ["shop_id", "title"]
