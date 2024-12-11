from zs_utils.api.fedex.base_api import FedexAPI


class FedexGetRateShipment(FedexAPI):
    http_method = "POST"
    resource_method = "/rate/v1/rates/quotes"
    required_params = [
        "accountNumber",
        "requestedShipment",
    ]
    allowed_params = [
        "rateRequestControlParameters",
        "carrierCodes",
    ]
