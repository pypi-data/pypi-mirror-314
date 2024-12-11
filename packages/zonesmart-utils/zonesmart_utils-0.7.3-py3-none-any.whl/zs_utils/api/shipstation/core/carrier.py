from zs_utils.api.shipstation.base_api import ShipstationAPI


class GetShipstationCarrierListAPI(ShipstationAPI):
    http_method = "GET"
    resource_method = "carriers"


class GetShipstationCarrierAPI(ShipstationAPI):
    http_method = "GET"
    resource_method = "carriers/getcarrier"
    required_params = ["carrierCode"]
