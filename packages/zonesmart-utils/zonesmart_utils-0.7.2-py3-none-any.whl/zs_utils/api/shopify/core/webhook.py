from zs_utils.api.shopify.base_api import ShopifyAPI


class CreateShopifyWebhookAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/webhook#post-webhooks
    """

    http_method = "POST"
    resource_method = "webhooks.json"
    payload_key = "webhook"
    required_params = ["address", "topic"]
    allowed_params = ["format", "fields"]


class DeleteShopifyWebhookAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/webhook#delete-webhooks-webhook-id
    """

    http_method = "DELETE"
    resource_method = "webhooks/{webhook_id}.json"
    required_params = ["webhook_id"]


class GetShopifyWebhookListAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/webhook#get-webhooks
    """

    http_method = "GET"
    resource_method = "webhooks.json"
    allowed_params = [
        "address",
        "created_at_max",
        "created_at_min",
        "fields",
        "limit",  # <= 250 default 50
        "since_id",
        "topic",
        "updated_at_max",
        "updated_at_min",
        "page_info",
    ]


class UpdateShopifyWebhookAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/webhook#put-webhooks-webhook-id
    """

    http_method = "PUT"
    resource_method = "webhooks/{webhook_id}.json"
    payload_key = "webhook"
    required_params = ["webhook_id", "address"]
