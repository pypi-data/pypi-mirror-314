from zs_utils.api.ebay.base_api import EbayAPI


class GetOrder(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrder
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/order/{orderId}"
    required_params = ["orderId"]


class GetOrders(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrders
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/order"
    allowed_params = ["orderIds", "filter", "offset", "limit"]
    MAX_OFFSET = 999
    MAX_LIMIT = 1000

    def get_clean_params(self, params: dict) -> dict:
        clean_params = super().get_clean_params(params)

        if clean_params.get("orderIds"):
            clean_params["orderIds"] = self.clean_orderIds(orderIds_string=clean_params["orderIds"])

        if clean_params.get("filter"):
            clean_params["filter"] = self.clean_filter(filter_string=clean_params["filter"])

        return clean_params

    def clean_orderIds(self, orderIds_string):
        message = ""
        order_ids = [order_id.strip() for order_id in orderIds_string.split(",")]
        if not (1 <= len(order_ids) <= 50):
            message = f"Количество ID заказов должно лежать в диапазоне [1:50]. Передано ID заказов: {len(order_ids)}"
        elif len(order_ids) != len(set(order_ids)):
            message = f"Среди ID заказов есть повторяющиеся.\nСписок ID: {orderIds_string}"
        else:
            for order_id in order_ids:
                for part in order_id.split("-"):
                    if not part.isdigit():
                        message += f"Недопустимый ID заказа: {order_id}.\n"
        if message:
            raise self.exception_class(message)
        return ",".join(order_ids)

    def clean_filter(self, filter_string):
        # Docs: https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrders#h2-input

        def _percent_encode(string):
            string = string.replace("[", "%5B")
            string = string.replace("]", "%5D")
            string = string.replace("{", "%7B")
            string = string.replace("}", "%7D")
            string = string.replace("|", "%7C")
            return string

        allowed_filters = ["creationdate", "lastmodifieddate", "orderfulfillmentstatus"]
        allowed_orderfulfillmentstatuses = [
            "{NOT_STARTED|IN_PROGRESS}",
            "{FULFILLED|IN_PROGRESS}",
        ]
        for pair in filter_string.split(","):
            key, value = pair.split(":")[0], ":".join(pair.split(":")[1:])

            if key == "orderfulfillmentstatus":
                if value.strip() not in allowed_orderfulfillmentstatuses:
                    self.exception_class(
                        f"Недопустимое значение фильтра {key}: {value}. Допустимые значения: {allowed_orderfulfillmentstatuses}.\n"
                    )
            elif key in ["creationdate", "lastmodifieddate"]:
                pass
                # TODO: проверить на соответствие шаблону YYYY-MM-DDThh:mm:ss.000Z
                # if not is_datetime(...):
                #     message += f"Недопустимое значение фильтра {key}: {value}.\n"
                #     message += f"Значение должно соответствовать шаблону: [<datetime>..<datetime or empty string>]"
            else:
                self.exception_class(f"Недопустимый фильтр: {key}. Допустимые фильтры: {allowed_filters}.\n")

        return ",".join([_percent_encode(filter_pair.strip()) for filter_pair in filter_string.split(",")])


class IssueRefund(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/issueRefund
    """

    http_method = "POST"
    resource_method = "sell/fulfillment/v1/order/{orderId}/issue_refund"
    required_params = ["orderId"]
