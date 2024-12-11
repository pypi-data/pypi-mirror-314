from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipGetOrderStatusAPI(ApishipAPI):
    resource_method = "orders/{order_id}/status"
    http_method = "GET"
    required_params = ["order_id"]


class ApishipGetOrderStatusByClientNumberAPI(ApishipAPI):
    resource_method = "orders/status"
    http_method = "GET"
    required_params = ["clientNumber"]


class ApishipGetOrderStatusHistoryAPI(ApishipAPI):
    resource_method = "orders/{order_id}/statusHistory"
    http_method = "GET"
    required_params = ["order_id"]
    allowed_params = ["offset", "limit"]


class ApishipGetOrderStatusHistoryByClientNumberAPI(ApishipAPI):
    resource_method = "orders/status/history"
    http_method = "GET"
    required_params = ["clientNumber"]


class ApishipGetOrderStatusListAPI(ApishipAPI):
    resource_method = "orders/statuses"
    http_method = "POST"
    required_params = ["orderIds"]


class ApishipGetOrdersWithChangedStatusAPI(ApishipAPI):
    resource_method = "orders/statuses/date/{date}"
    http_method = "GET"
    required_params = ["date"]


class ApishipGetOrderStatusHistoryListByDateAPI(ApishipAPI):
    resource_method = "orders/statuses/history/date/{date}"
    http_method = "GET"
    required_params = ["date"]
    allowed_params = ["offset", "limit"]


class ApishipGetOrdersStatusChangeByIntervalAPI(ApishipAPI):
    resource_method = "orders/statuses/interval"
    http_method = "GET"
    required_params = ["from", "to"]
    allowed_params = ["offset", "limit", "filter"]
