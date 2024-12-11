from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyShippingProfileList(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingShippingProfiles
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/shipping-profiles"
    required_params = ["shop_id"]


class GetEtsyShippingProfile(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingShippingProfile
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}"
    required_params = ["shop_id", "shipping_profile_id"]


class DeleteEtsyShippingProfile(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/deleteListingShippingProfile
    """

    http_method = "DELETE"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}"
    required_params = ["shop_id", "shipping_profile_id"]


class CreateEtsyShippingProfile(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/createListingShippingProfile
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/shipping-profiles"
    required_params = [
        "shop_id",
        "title",
        "origin_country_iso",
        "primary_cost",
        "secondary_cost",
        "min_processing_time",
        "max_processing_time",
    ]
    allowed_params = [
        "destination_country_iso",
        "destination_region",
        "origin_postal_code",
        "shipping_carrier_id",
        "mail_class",
        "min_processing_time",
        "max_processing_time",
        "min_delivery_days",
        "max_delivery_days",
    ]


class UpdateEtsyShippingProfile(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListingShippingProfile
    """

    http_method = "PUT"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}"
    required_params = ["shop_id", "shipping_profile_id"]
    allowed_params = [
        "title",
        "origin_country_iso",
        "origin_postal_code",
        "min_processing_time",
        "max_processing_time",
    ]
