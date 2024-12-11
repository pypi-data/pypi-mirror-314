from zs_utils.api.insales.base_api import InsalesAPI


class GetInsalesCategoryList(InsalesAPI):
    """
    https://api.insales.ru/#category
    """

    resource_method = "categories.json"
    http_method = "GET"
