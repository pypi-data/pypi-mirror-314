from zs_utils.api.etsy.base_api import EtsyAPI


class CreateEtsyShippingProfileUpgrade(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/createListingShippingProfileUpgrade
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades"
    required_params = [
        "shop_id",
        "shipping_profile_id",
        "type",
        "upgrade_name",
        "price",
        "secondary_price",
    ]
    allowed_params = [
        "shipping_carrier_id",
        "mail_class",
        "min_delivery_days",
        "max_delivery_days",
    ]


class GetEtsyShippingProfileUpgradeList(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingShippingProfileUpgrades
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades"
    required_params = ["shop_id", "shipping_profile_id"]


class UpdateEtsyShippingProfileUpgrade(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListingShippingProfileUpgrade
    """

    http_method = "PUT"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades/{upgrade_id}"
    required_params = ["shop_id", "shipping_profile_id", "upgrade_id"]
    allowed_params = [
        "upgrade_name",
        "type",
        "price",
        "secondary_price",
        "shipping_carrier_id",
        "mail_class",
        "min_delivery_days",
        "max_delivery_days",
    ]


class DeleteEtsyShippingProfileUpgrade(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListingShippingProfileUpgrade
    """

    http_method = "DELETE"
    resource_method = "shops/{shop_id}/shipping-profiles/{shipping_profile_id}/upgrades/{upgrade_id}"
    required_params = ["shop_id", "shipping_profile_id", "upgrade_id"]
