from zs_utils.api.ebay.base_api import EbayAPI


class CreateInventoryLocation(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/createInventoryLocation
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/location/{merchantLocationKey}"
    required_params = ["merchantLocationKey"]


class DeleteInventoryLocation(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/deleteInventoryLocation
    """

    http_method = "DELETE"
    resource_method = "sell/inventory/v1/location/{merchantLocationKey}"
    required_params = ["merchantLocationKey"]


class DisableInventoryLocation(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/disableInventoryLocation
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/location/{merchantLocationKey}/disable"
    required_params = ["merchantLocationKey"]


class EnableInventoryLocation(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/enableInventoryLocation
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/location/{merchantLocationKey}/enable"
    required_params = ["merchantLocationKey"]


class GetInventoryLocation(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/getInventoryLocation
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/location/{merchantLocationKey}"
    required_params = ["merchantLocationKey"]


class GetInventoryLocations(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/getInventoryLocations
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/location"
    allowed_params = ["offset", "limit"]


class UpdateInventoryLocation(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/updateInventoryLocation
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/location/{merchantLocationKey}/update_location_details"
    required_params = ["merchantLocationKey"]
