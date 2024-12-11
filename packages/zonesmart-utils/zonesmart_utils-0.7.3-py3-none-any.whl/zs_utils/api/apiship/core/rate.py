from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipGetRatesAPI(ApishipAPI):
    resource_method = "calculator"
    http_method = "POST"
    required_params = [
        "from",
        "to",
        "weight",
        "width",
        "height",
        "length",
    ]
    allowed_params = [
        "assessedCost",
        "pickupDate",
        "pickupTypes",
        "deliveryTypes",
        "codCost",
        "includeFees",
        "providerKeys",
        "timeout",
        "extraParams",
    ]
