from zs_utils.api.shipstation.base_api import ShipstationAPI


class GetShipstationRatesListAPI(ShipstationAPI):
    """
    Docs: https://www.shipstation.com/docs/api/shipments/get-rates/
    """

    http_method = "POST"
    resource_method = "shipments/getrates"
    allowed_params = [
        "carrierCode",
        "serviceCode",
        "packageCode",
        "fromPostalCode",
        "toState",
        "toCountry",
        "toPostalCode",
        "toCity",
        "weight",
        "dimensions",
        "confirmation",
        "residential",
    ]
