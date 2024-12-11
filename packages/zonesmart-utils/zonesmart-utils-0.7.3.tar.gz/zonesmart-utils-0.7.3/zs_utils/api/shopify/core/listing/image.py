from zs_utils.api.shopify.base_api import ShopifyAPI


class CreateShopifyImageAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-image#post-products-product-id-images
    """

    http_method = "POST"
    resource_method = "products/{product_id}/images.json"
    payload_key = "image"
    required_params = ["product_id", "attachment"]
    allowed_params = [
        "position",
        "variant_ids",
        "metafields",
        "alt",
    ]


class DeleteShopifyImageAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-image#delete-products-product-id-images-image-id
    """

    http_method = "DELETE"
    resource_method = "products/{product_id}/images/{image_id}.json"
    required_params = ["product_id", "image_id"]


class UpdateShopifyImageAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-image#put-products-product-id-images-image-id
    """

    http_method = "PUT"
    resource_method = "products/{product_id}/images/{image_id}.json"
    payload_key = "image"
    required_params = ["product_id", "image_id"]
    allowed_params = [
        "position",
        "alt",
        "variant_ids",
        "metafields",
    ]


class GetShopifyProductImageListAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-image#get-products-product-id-images
    """

    http_method = "GET"
    resource_method = "products/{product_id}/images.json"
    required_params = ["product_id"]
    allowed_params = [
        "fields",
        "since_id",
    ]


class GetShopifyProductImageAPI(ShopifyAPI):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product-image#get-products-product-id-images-image-id
    """

    http_method = "GET"
    resource_method = "products/{product_id}/images/{image_id}.json"
    required_params = ["product_id", "image_id"]
    allowed_params = ["fields"]
