from zs_utils.api.ebay.base_api import EbayAPI


# SINGLE ITEM API


class CreateOrReplaceInventoryItem(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/createOrReplaceInventoryItem
    """

    http_method = "PUT"
    resource_method = "sell/inventory/v1/inventory_item/{sku}"
    required_params = ["sku"]


class GetInventoryItem(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItem
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/inventory_item/{sku}"
    required_params = ["sku"]


class GetInventoryItems(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItems
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/inventory_item"
    allowed_params = ["offset", "limit"]


class DeleteInventoryItem(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/deleteInventoryItem
    """

    http_method = "DELETE"
    resource_method = "sell/inventory/v1/inventory_item/{sku}"
    required_params = ["sku"]


# PRODUCT COMPATIBILITY API


class ProductCompatibilityAPI(EbayAPI):
    resource_method = "sell/inventory/v1/inventory_item/{sku}/product_compatibility"
    required_params = ["sku"]


class CreateOrReplaceProductCompatibility(ProductCompatibilityAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/product_compatibility/methods/createOrReplaceProductCompatibility
    """  # noqa

    http_method = "PUT"


class GetProductCompatibility(ProductCompatibilityAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/product_compatibility/methods/getProductCompatibility
    """  # noqa

    http_method = "GET"


class DeleteProductCompatibility(ProductCompatibilityAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/product_compatibility/methods/deleteProductCompatibility
    """  # noqa

    http_method = "DELETE"


# BULK API


class BulkUpdatePriceQuantity(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/bulkUpdatePriceQuantity
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/bulk_update_price_quantity"


class BulkCreateOrReplaceInventoryItem(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/bulkCreateOrReplaceInventoryItem
    """  # noqa

    http_method = "POST"
    resource_method = "sell/inventory/v1/bulk_create_or_replace_inventory_item"


class BulkGetInventoryItem(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/bulkGetInventoryItem
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/bulk_get_inventory_item"
