from zs_utils.api.etsy.base_api import EtsyAPI


class CreateEtsyShippingProfileDestination(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/createListingShippingProfileDestination
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations"
    required_params = [
        "shop_id",
        "shipping_profile_id",
        "primary_cost",
        "secondary_cost",
    ]
    allowed_params = [
        "destination_country_iso",
        "destination_region",
        "shipping_carrier_id",
        "mail_class",
        "min_delivery_days",
        "max_delivery_days",
    ]


class GetEtsyShippingProfileDestinationList(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingShippingProfileDestinationsByShippingProfile
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations"
    required_params = ["shop_id", "shipping_profile_id"]


class UpdateEtsyShippingProfileDestination(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListingShippingProfileDestination
    """

    http_method = "PUT"
    resource_method = (
        "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations/{shipping_profile_destination_id}"
    )
    required_params = [
        "shop_id",
        "shipping_profile_id",
        "shipping_profile_destination_id",
    ]
    allowed_params = [
        "primary_cost",
        "secondary_cost",
        "destination_country_iso",
        "destination_region",
        "shipping_carrier_id",
        "mail_class",
        "min_delivery_days",
        "max_delivery_days",
    ]


class DeleteEtsyShippingProfileDestination(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/deleteListingShippingProfileDestination
    """

    http_method = "DELETE"
    resource_method = (
        "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/destinations/{shipping_profile_destination_id}"
    )
    required_params = [
        "shop_id",
        "shipping_profile_id",
        "shipping_profile_destination_id",
    ]
