from zs_utils.api.ebay.base_api import EbayAPI


class BulkMigrateListing(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/listing/methods/bulkMigrateListing
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/bulk_migrate_listing"
