from zs_utils.api.fedex.base_api import FedexAPI


class FedexTrackByTrackingNumber(FedexAPI):
    http_method = "POST"
    resource_method = "/track/v1/trackingnumbers"
    required_params = [
        "includeDetailedScans",
        "trackingInfo",
    ]
