from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyProduct(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingProduct
    """

    http_method = "GET"
    resource_method = "listings/{listing_id}/inventory/products/{product_id}"
    required_params = ["listing_id", "product_id"]


class GetEtsyOffering(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingOffering
    """

    http_method = "GET"
    resource_method = "listings/{listing_id}/products/{product_id}/offerings/{product_offering_id}"
    required_params = ["listing_id", "product_id", "product_offering_id"]


class GetEtsyListingProductList(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingInventory
    """

    http_method = "GET"
    resource_method = "listings/{listing_id}/inventory"
    required_params = ["listing_id"]


class UpdateEtsyListingInventory(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListingInventory
    """

    http_method = "PUT"
    resource_method = "listings/{listing_id}/inventory"
    required_params = [
        "listing_id",
        "products",
    ]
    allowed_params = [
        "price_on_property",
        "quantity_on_property",
        "sku_on_property",
    ]


class GetEtsyListingList(EtsyAPI):
    """
    Endpoint to list Listings that belong to a Shop. Listings can be filtered using the 'state' param.

    Docs:
    https://www.etsy.com/openapi/developers#operation/getListings
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings"
    required_params = ["shop_id"]
    allowed_params = ["state", "limit", "offset", "sort_on", "sort_order"]


class GetEtsySingleListing(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/developers/documentation/reference/listing#method_getlisting
    """

    http_method = "GET"
    resource_method = "listings/{listing_id}"
    required_params = ["listing_id"]


class GetEtsyListingAttributeList(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingProperties
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/properties"
    required_params = ["shop_id", "listing_id"]


class GetEtsyListingAttribute(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingProperty
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/properties/{property_id}"
    required_params = ["shop_id", "listing_id", "property_id"]


class CreateOrUpdateEtsyListingAttribute(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListingProperty
    """

    http_method = "PUT"
    resource_method = "shops/{shop_id}/listings/{listing_id}/properties/{property_id}"
    required_params = [
        "shop_id",
        "listing_id",
        "property_id",
        "values",
    ]
    allowed_params = [
        "value_ids",
        "scale_id",
    ]


class DeleteEtsyListingAttribute(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/deleteListingProperty
    """

    http_method = "DELETE"
    resource_method = "shops/{shop_id}/listings/{listing_id}/properties/{property_id}"
    required_params = ["shop_id", "listing_id", "property_id"]


class DeleteEtsyListing(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/deleteListing
    """

    http_method = "DELETE"
    resource_method = "listings/{listing_id}"
    required_params = ["listing_id"]


class GetEtsyOrderListings(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingsByShopReceipt
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/receipts/{receipt_id}/listings"
    required_params = ["receipt_id", "shop_id"]


class GetEtsyShopSectionListings(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingsByShopSectionId
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/sections/{shop_section_id}/listings"
    required_params = ["shop_id", "shop_section_id"]
    allowed_params = ["limit", "offset", "sort_on", "sort_order"]


class CreateEtsySingleListing(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/createListing
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/listings"
    required_params = [
        "shop_id",
        "quantity",
        "title",
        "description",
        "price",
        "who_made",
        "when_made",
        "taxonomy_id",
        "shipping_profile_id",
    ]
    allowed_params = [
        "materials",
        "shop_section_id",
        "processing_min",
        "processing_max",
        "tags",
        "recipient",
        "occasion",
        "styles",
        "is_personalizable",
        "personalization_is_required",
        "personalization_char_count_max",
        "personalization_instructions",
        "production_partner_ids",
        "image_ids",
        "is_supply",
        "is_customizable",
        "is_taxable",
        "item_length",
        "item_width",
        "item_height",
        "item_dimensions_unit",
        "item_weight",
        "item_weight_unit",
        "type",
    ]


class UpdateEtsySingleListing(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateListing
    """

    http_method = "PUT"
    resource_method = "shops/{shop_id}/listings/{listing_id}"
    required_params = ["shop_id", "listing_id"]
    allowed_params = [
        "quantity",
        "price",
        "title",
        "description",
        "materials",
        "should_auto_renew",
        "shipping_profile_id",
        "shop_section_id",
        "is_taxable",
        "taxonomy_id",
        "tags",
        "who_made",
        "when_made",
        "featured_rank",
        "is_personalizable",
        "personalization_is_required",
        "personalization_char_count_max",
        "personalization_instructions",
        "state",
        "is_supply",
        "production_partner_ids",
        "type",
        "item_length",
        "item_width",
        "item_height",
        "item_dimensions_unit",
        "item_weight",
        "item_weight_unit",
    ]


class DeleteListingFile(EtsyAPI):
    """
    Docs: https://developers.etsy.com/documentation/reference/#operation/getListingsByShopSectionId
    """

    http_method = "DELETE"
    resource_method = "shops/{shop_id}/listings/{listing_id}/files/{listing_file_id}"
    required_params = ["shop_id", "listing_id", "listing_file_id"]


class GetListingFile(EtsyAPI):
    """
    Docs: https://developers.etsy.com/documentation/reference/#operation/getListingFile
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/files/{listing_file_id}"
    required_params = ["shop_id", "listing_id", "listing_file_id"]


class GetAllListingFiles(EtsyAPI):
    """
    Docs: https://developers.etsy.com/documentation/reference/#operation/getAllListingFiles
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/files"
    required_params = ["shop_id", "listing_id"]


class UploadListingFile(EtsyAPI):
    """
    Docs: https://developers.etsy.com/documentation/reference/#operation/uploadListingFile
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/listings/{listing_id}/files"
    required_params = ["shop_id", "listing_id"]
    allowed_params = [
        "listing_file_id",
        "file",
        "name",
        "rank",
    ]

    @property
    def headers(self) -> dict:
        # При наличии файла будет автоматом подставлен multipart - что нам и нужно
        headers = super().headers
        headers.pop("Content-Type")
        return headers
