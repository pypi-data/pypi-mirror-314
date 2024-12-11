from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipGetOrderLabelAPI(ApishipAPI):
    resource_method = "orders/labels"
    http_method = "POST"
    required_params = ["orderIds", "format"]


class ApishipGetOrderWaybillsAPI(ApishipAPI):
    resource_method = "orders/waybills"
    http_method = "POST"
    required_params = ["orderIds"]
