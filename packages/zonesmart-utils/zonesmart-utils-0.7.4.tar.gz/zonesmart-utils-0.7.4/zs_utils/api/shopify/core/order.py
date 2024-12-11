from zs_utils.api.shopify.base_api import ShopifyAPI


class GetShopifyOrderListAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/order#get-orders?status=any
    """

    http_method = "GET"
    resource_method = "orders.json"
    allowed_params = [
        "attribution_app_id",
        "created_at_max",
        "created_at_min",
        "fields",
        "financial_status",
        "fulfillment_status",
        "ids",
        "limit",
        "processed_at_max",
        "processed_at_min",
        "since_id",
        "status",
        "updated_at_max",
        "updated_at_min",
        "page_info",
    ]


class GetShopifyOrderAPI(ShopifyAPI):
    """
    https://shopify.dev/docs/api/admin-rest/2023-10/resources/order#get-orders-order-id?fields=id,line-items,name,total-price
    """

    http_method = "GET"
    resource_method = "orders/{order_id}.json"
    required_params = ["order_id"]


class UpdateShopifyOrderAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/order#put-orders-order-id
    """

    http_method = "PUT"
    resource_method = "orders/{order_id}.json"
    payload_key = "order"
    required_params = ["order_id"]
    allowed_params = [
        "note",
        "note_attributes",
        "email",
        "phone",
        "buyer_accepts_marketing",
        "shipping_address",
        "customer",
        "tags",
        "metafields",
    ]


class CreateShopifyOrderAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/order#post-orders
    """

    http_method = "POST"
    resource_method = "orders.json"
    payload_key = "order"
    required_params = ["line_items"]
    allowed_params = [
        "email",
        "phone",
        "fulfillment_status",
        "inventory_behaviour",
        "send_receipt",
        "send_fulfillment_receipt",
        "fulfillments",
        "total_tax",
        "currency",
        "tax_lines",
        "customer",
        "financial_status",
        "billing_address",
        "shipping_address",
        "discount_codes",
        "note",
        "note_attributes",
        "buyer_accepts_marketing",
        "tags",
        "transactions",
        "metafields",
    ]


class DeleteShopifyOrderAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/order#delete-orders-order-id
    """

    http_method = "DELETE"
    resource_method = "orders/{order_id}.json"
    required_params = ["order_id"]


class GetShopifyOrdersCountAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/order#get-orders-count?status=any
    """

    http_method = "GET"
    resource_method = "orders/count.json"
    allowed_params = [
        "created_at_max",
        "created_at_min",
        "financial_status",
        "fulfillment_status",
        "status",
        "updated_at_max",
        "updated_at_min",
    ]
