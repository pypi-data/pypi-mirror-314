from zs_utils.api.shipstation.base_api import ShipstationAPI


class ShipmentShipstationAPIMixin:
    resource_method = "shipments"


class GetShipstationShipmentsListAPI(ShipstationAPI):
    http_method = "GET"
    resource_method = "shipments"


class CreateShipstationLabelAPI(ShipstationAPI):
    """
    Docs: https://www.shipstation.com/docs/api/shipments/create-label/
    """

    http_method = "POST"
    resource_method = "shipments/createlabel"
    allowed_params = [
        "carrierCode",
        "serviceCode",
        "packageCode",
        "confirmation",
        "shipDate",
        "weight",
        "dimensions",
        "shipFrom",
        "shipTo",
        "insuranceOptions",
        "internationalOptions",
        "advancedOptions",
        "testLabel",
    ]


class VoidShipstationLabelAPI(ShipstationAPI):
    http_method = "POST"
    resource_method = "shipments/voidlabel"
    allowed_params = ["shipmentId"]
