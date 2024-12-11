from zs_utils.api.fedex.base_api import FedexAPI


class FedexCreateShipment(FedexAPI):
    http_method = "POST"
    resource_method = "/ship/v1/shipments"
    required_params = [
        "requestedShipment",
        "labelResponseOptions",
        "accountNumber",
    ]
    allowed_params = [
        "mergeLabelDocOption",
        "shipAction",
        "processingOptionType",
        "oneLabelAtATime",
    ]


class FedexCancelShipment(FedexAPI):
    http_method = "PUT"
    resource_method = "/ship/v1/shipments/cancel"
    required_params = [
        "accountNumber",
        "trackingNumber",
    ]
    allowed_params = [
        "senderCountryCode",
        "deletionControl",
    ]
