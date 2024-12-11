from zs_utils.api.insales.base_api import InsalesAPI


class CreateInsalesOrder(InsalesAPI):
    """
    https://api.insales.ru/#order-create-order-with-product-json
    """

    resource_method = "orders.json"
    http_method = "POST"
    required_params = ["order"]


class DeleteInsalesOrder(InsalesAPI):
    """
    В доках нет, но догадаться как это сделать было нетрудно
    """

    resource_method = "orders/{order_id}.json"
    http_method = "DELETE"
    required_params = ["order_id"]
