from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipCreateOrderAPI(ApishipAPI):
    """
    Docs: https://docs.apiship.ru/docs/api/order-service/create-order-async/
    """

    resource_method = "orders"
    http_method = "POST"
    required_params = [
        "order",
        "cost",
        "sender",
        "recipient",
        "places",
    ]
    allowed_params = [
        "returnAddress",
        "extraParams",
    ]


class ApishipValidateOrderAPI(ApishipAPI):
    resource_method = "orders/validate"
    http_method = "POST"
    required_params = [
        "order",
        "cost",
        "sender",
        "recipient",
        "places",
    ]
    allowed_params = [
        "returnAddress",
        "extraParams",
    ]


class ApishipGetOrderAPI(ApishipAPI):
    resource_method = "orders/{order_id}"
    http_method = "GET"
    required_params = ["order_id"]


class ApishipUpdateOrderAPI(ApishipAPI):
    resource_method = "orders/{order_id}"
    http_method = "PUT"
    required_params = [
        "order_id",
        "order",
        "cost",
        "sender",
        "recipient",
        "returnAddress",
        "places",
        "extraParams",
    ]


class ApishipDeleteOrderAPI(ApishipAPI):
    resource_method = "orders/{order_id}"
    http_method = "DELETE"
    required_params = ["order_id"]


class ApishipResendOrderAPI(ApishipAPI):
    resource_method = "orders/{order_id}/resend"
    http_method = "POST"
    required_params = ["order_id"]


class ApishipCancelOrderAPI(ApishipAPI):
    resource_method = "orders/{order_id}/cancel"
    http_method = "GET"
    required_params = ["order_id"]


class ApishipUpdateOrderItemsAPI(ApishipAPI):
    resource_method = "orders/{order_id}/items"
    http_method = "POST"
    required_params = ["order_id", "items"]
