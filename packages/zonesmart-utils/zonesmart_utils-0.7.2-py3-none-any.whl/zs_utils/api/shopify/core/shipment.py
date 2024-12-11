from zs_utils.api.shopify.base_api import ShopifyAPI


class GetShopifyFulfillmentAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/fulfillment#get-orders-order-id-fulfillments-fulfillment-id
    """

    http_method = "GET"
    resource_method = "orders/{order_id}/fulfillments/{fulfillment_id}.json"
    required_params = ["order_id", "fulfillment_id"]


class GetShopifyFulfillmentListAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/fulfillment#get-orders-order-id-fulfillments
    """

    http_method = "GET"
    resource_method = "orders/{order_id}/fulfillments.json"
    required_params = ["order_id"]
    allowed_params = ["page_info"]


class GetShopifyFulfillmentOrderListAPI(ShopifyAPI):
    """
    https://shopify.dev/docs/api/admin-rest/2023-10/resources/fulfillmentorder#get-orders-order-id-fulfillment-orders
    """

    http_method = "GET"
    resource_method = "orders/{order_id}/fulfillment_orders.json"
    required_params = ["order_id"]


class UpdateShopifyFulfillmentAPI(ShopifyAPI):
    """
    https://shopify.dev/docs/api/admin-rest/2023-10/resources/fulfillment#post-fulfillments-fulfillment-id-update-tracking
    """

    http_method = "PUT"
    resource_method = "fulfillments/{fulfillment_id}/update_tracking.json"
    payload_key = "fulfillment"
    required_params = ["fulfillment_id", "tracking_number"]


class CreateShopifyFulfillmentAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/fulfillment#post-orders-order-id-fulfillments
    """

    http_method = "POST"
    resource_method = "fulfillments.json"
    payload_key = "fulfillment"
    required_params = [
        "line_items_by_fulfillment_order",
    ]
    allowed_params = [
        "message",
        "notify_customer",
        "origin_address",
        "tracking_info",
    ]
