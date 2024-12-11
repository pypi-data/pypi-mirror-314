from zs_utils.api.shopify.base_api import ShopifyAPI


class GetShopifyProductListAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#get-products
    """

    http_method = "GET"
    resource_method = "products.json"
    allowed_params = [
        "collection_id",
        "created_at_max",
        "created_at_min",
        "fields",
        "handle",
        "ids",
        "limit",  # <= 250
        "presentment_currencies",
        "product_type",
        "published_at_max",
        "published_at_min",
        "published_status",
        "since_id",
        "status",
        "title",
        "updated_at_max",
        "updated_at_min",
        "vendor",
        "page_info",
    ]


class GetShopifyProductCountAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#get-products-count
    """

    http_method = "GET"
    resource_method = "products/count.json"
    allowed_params = [
        "collection_id",
        "created_at_max",
        "created_at_min",
        "product_type",
        "published_at_max",
        "published_at_min",
        "published_status",
        "updated_at_max",
        "updated_at_min",
        "vendor",
    ]


class GetShopifyProductAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#get-products-product-id
    """

    http_method = "GET"
    resource_method = "products/{product_id}.json"
    required_params = ["product_id"]
    allowed_params = ["fields"]


class DeleteShopifyProductAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#delete-products-product-id
    """

    http_method = "DELETE"
    resource_method = "products/{product_id}.json"
    required_params = ["product_id"]


class UpdateShopifyProductAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#put-products-product-id
    """

    http_method = "PUT"
    resource_method = "products/{product_id}.json"
    payload_key = "product"
    required_params = ["product_id"]
    allowed_params = [
        "title",
        "status",
        "tags",
        "images",
        "variants",
        "metafields_global_title_tag",
        "metafields_global_description_tag",
        "published",
        "metafields",
    ]


class CreateShopifyProductAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#post-products
    """

    http_method = "POST"
    resource_method = "products.json"
    payload_key = "product"
    required_params = [
        "title",
    ]
    allowed_params = [
        "body_html",
        "vendor",
        "product_type",
        "tags",
        "status",
        "variants",
        "options",
        "handle",
        "images",
        "template_suffix",
        "metafields_global_title_tag",
        "metafields_global_description_tag",
        "metafields",
    ]
