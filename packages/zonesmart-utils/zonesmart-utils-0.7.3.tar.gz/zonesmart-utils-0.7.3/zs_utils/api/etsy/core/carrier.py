from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyCarriers(EtsyAPI):
    """
    Docs:
    https://developers.etsy.com/documentation/reference/#operation/getShippingCarriers
    """

    description = "Получение списка курьерских служб Etsy"
    http_method = "GET"
    resource_method = "shipping-carriers"
    required_params = ["origin_country_iso"]
