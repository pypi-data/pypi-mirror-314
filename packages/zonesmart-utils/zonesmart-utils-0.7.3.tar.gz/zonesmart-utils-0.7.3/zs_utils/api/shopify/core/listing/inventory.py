from zs_utils.api.shopify.base_api import ShopifyAPI


class UpdateShopifyInventoryAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/inventorylevel#post-inventory-levels-set
    """

    http_method = "POST"
    resource_method = "inventory_levels/set.json"
    required_params = [
        "available",
        "inventory_item_id",
        "location_id",
    ]
    allowed_params = ["disconnect_if_necessary"]


class GetShopifyInventoryLevelListAPI(ShopifyAPI):
    """
    https://shopify.dev/docs/api/admin-rest/2023-10/resources/inventorylevel#get-inventory-levels?location-ids=655441491
    """

    http_method = "GET"
    resource_method = "inventory_levels.json"
    required_params = []
    allowed_params = [
        "inventory_item_ids",  # <= 50
        "limit",  # <= 250
        "location_ids",  # <= 50
        "updated_at_min",
        "page_info",
    ]
