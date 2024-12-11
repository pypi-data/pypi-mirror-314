from zs_utils.api.ebay.base_api import EbayAPI


class CreateOrReplaceInventoryItemGroup(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item_group/methods/createOrReplaceInventoryItemGroup
    """  # noqa

    http_method = "PUT"
    resource_method = "sell/inventory/v1/inventory_item_group/{inventoryItemGroupKey}"
    required_params = ["inventoryItemGroupKey"]


class DeleteInventoryItemGroup(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item_group/methods/deleteInventoryItemGroup
    """

    http_method = "DELETE"
    resource_method = "sell/inventory/v1/inventory_item_group/{inventoryItemGroupKey}"
    required_params = ["inventoryItemGroupKey"]


class GetInventoryItemGroup(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item_group/methods/getInventoryItemGroup
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/inventory_item_group/{inventoryItemGroupKey}"
    required_params = ["inventoryItemGroupKey"]


class PublishOfferByInventoryItemGroup(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/publishOfferByInventoryItemGroup
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/offer/publish_by_inventory_item_group"


class WithdrawOfferByInventoryItemGroup(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/withdrawOfferByInventoryItemGroup
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/offer/withdraw_by_inventory_item_group"
