from zs_utils.api.insales.base_api import InsalesAPI


class GetInsalesProductList(InsalesAPI):
    """
    https://api.insales.ru/#product-get-products-json
    """

    resource_method = "products.json"
    http_method = "GET"
    allowed_params = [
        "updated_since",
        "from_id",
        "per_page",
        "with_deleted",
        "deleted",
    ]


class GetInsalesProductsCount(InsalesAPI):
    """
    https://api.insales.ru/#product-get-products-count-json
    """

    resource_method = "products/count.json"
    http_method = "GET"
