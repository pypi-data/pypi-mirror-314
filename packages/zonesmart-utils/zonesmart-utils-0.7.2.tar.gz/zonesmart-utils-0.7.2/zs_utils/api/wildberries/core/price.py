from zs_utils.api.wildberries.base_api import WildberriesAPI


class WildberriesPriceAPI(WildberriesAPI):
    production_api_url = "https://discounts-prices-api.wb.ru/"


class GetWildberriesPrices(WildberriesPriceAPI):
    """
    https://openapi.wb.ru/prices/api/ru/#tag/Spiski-tovarov/paths/~1api~1v2~1list~1goods~1filter/get
    """

    http_method = "GET"
    resource_method = "api/v2/list/goods/filter"
    required_params = ["limit"]
    allowed_params = ["offset", "filterNmID"]


class UpdateWildberriesPrices(WildberriesPriceAPI):
    """
    https://openapi.wb.ru/prices/api/ru/#tag/Ustanovka-cen-i-skidok/paths/~1api~1v2~1upload~1task/post
    """

    http_method = "POST"
    resource_method = "api/v2/upload/task"
    required_params = ["data"]
