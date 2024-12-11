from zs_utils.api.amazon.base_api import AmazonAPI


class GetListingBySkuAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#get-listings2021-08-01itemsselleridsku
    """

    http_method = "GET"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = ["marketplaceIds"]
    allowed_params = [
        "issueLocale",
        "includedData",
    ]


class GetListingListAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference#get-catalog2022-04-01items
    """

    http_method = "GET"
    resource_method = "/catalog/2022-04-01/items"
    required_params = [
        "marketplaceIds",
        "identifiersType",
        "identifiers",
    ]
    allowed_params = [
        "includedData",
        "locale",
        "keywords",
        "brandNames",
        "classificationIds",
        "pageSize",
        "pageToken",
        "keywordsLocale",
    ]


# allows you to update the attributes of a given SKU.
class PatchListingAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#patch-listings2021-08-01itemsselleridsku
    """

    http_method = "PATCH"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = [
        "marketplaceIds",
        "sku",
        "sellerId",
        "payload",
    ]
    allowed_params = [
        "includedData",
        "mode",
        "issueLocale",
    ]


# allows you to create a given SKU and update attributes like price, inventory, or both
class CreateOrUpdateListingAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#put-listings2021-08-01itemsselleridsku
    """

    http_method = "PUT"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = [
        "marketplaceIds",
        "sku",
        "sellerId",
        "payload",
    ]
    allowed_params = [
        "includedData",
        "mode",
        "issueLocale",
    ]


# allows you to delete a given SKU
class DeleteListingAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#delete-listings2021-08-01itemsselleridsku
    """

    http_method = "DELETE"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = [
        "marketplaceIds",
        "sku",
        "sellerId",
    ]
    allowed_params = [
        "issueLocale",
    ]


class GetInventoriesAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/fbainventory-api-v1-reference#get-fbainventoryv1summaries
    """

    http_method = "GET"
    resource_method = "fba/inventory/v1/summaries"
    required_params = [
        "marketplaceIds",
        "granularityType",
        "granularityId",
    ]
    allowed_params = [
        "details",
        "startDateTime",
        "sellerSkus",
        "sellerSku",
        "nextToken",
    ]


class GetListingPriceAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/product-pricing-api-v0-reference#get-productspricingv0price
    """

    http_method = "GET"
    resource_method = "products/pricing/v0/price"
    required_params = [
        "MarketplaceId",
        "ItemType",
    ]
    allowed_params = [
        "Asins",
        "ItemCondition",
        "OfferType",
    ]
