from zs_utils.api.shopify.base_api import ShopifyAPI


class CreateShopifyVariantAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-variant#post-products-product-id-variants
    """

    http_method = "POST"
    resource_method = "products/{product_id}/variants.json"
    payload_key = "variant"
    required_params = ["product_id", "option1"]
    allowed_params = [
        "price",
        "image_id",
        "metafields",
        "inventory_policy",
        "compare_at_price",
        "fulfillment_service",
        "taxable",
        "barcode",
        "image",
        "id",
        "option2",
        "option3",
        "weight",
        "weight_unit",
    ]


class DeleteShopifyVariantAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-variant#delete-products-product-id-variants-variant-id
    """

    http_method = "DELETE"
    resource_method = "products/{product_id}/variants/{variant_id}.json"
    required_params = ["product_id", "variant_id"]


class UpdateShopifyVariantAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-variant#put-variants-variant-id
    """

    http_method = "PUT"
    resource_method = "variants/{variant_id}.json"
    payload_key = "variant"
    required_params = ["variant_id"]
    allowed_params = [
        "option1",
        "price",
        "image_id",
        "metafields",
        "inventory_policy",
        "compare_at_price",
        "fulfillment_service",
        "taxable",
        "barcode",
        "image",
        "id",
        "option2",
        "option3",
        "weight",
        "weight_unit",
    ]
