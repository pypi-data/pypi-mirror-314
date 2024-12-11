from zs_utils.api.ebay.base_api import EbayAPI


class CreateOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/createOffer
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/offer"


class UpdateOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/updateOffer
    """

    http_method = "PUT"
    resource_method = "sell/inventory/v1/offer/{offerId}"
    required_params = ["offerId"]


class GetOffers(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/getOffers
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/offer"
    required_params = ["sku"]
    allowed_params = ["marketplace_id", "offset", "limit"]


class GetOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/getOffer
    """

    http_method = "GET"
    resource_method = "sell/inventory/v1/offer/{offerId}"
    required_params = ["offerId"]


class DeleteOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/deleteOffer
    """

    http_method = "DELETE"
    resource_method = "sell/inventory/v1/offer/{offerId}"
    required_params = ["offerId"]


class PublishOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/publishOffer
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/offer/{offerId}/publish"
    required_params = ["offerId"]


class WithdrawOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/withdrawOffer
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/offer/{offerId}/withdraw"
    required_params = ["offerId"]


class GetListingFees(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/getListingFees
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/offer/get_listing_fees"


class BulkCreateOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/bulkCreateOffer
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/bulk_create_offer"


class BulkPublishOffer(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/inventory/resources/offer/methods/bulkPublishOffer
    """

    http_method = "POST"
    resource_method = "sell/inventory/v1/bulk_publish_offer"
