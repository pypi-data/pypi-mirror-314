from zs_utils.api.ebay.base_api import EbayAPI


class CreateShippingFulfillment(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/shipping_fulfillment/methods/createShippingFulfillment
    """

    http_method = "POST"
    resource_method = "sell/fulfillment/v1/order/{orderId}/shipping_fulfillment"
    required_params = ["orderId"]


class GetShippingFulfillment(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/shipping_fulfillment/methods/getShippingFulfillment
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/order/{orderId}/shipping_fulfillment/{fulfillmentId}"
    required_params = ["orderId", "fulfillmentId"]


class GetShippingFulfillments(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/shipping_fulfillment/methods/getShippingFulfillments
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/order/{orderId}/shipping_fulfillment"
    required_params = ["orderId"]
