from zs_utils.api.base_api import BaseAPI
from zs_utils.api.yandex_market.base_api import YandexMarketAPI


class GetYandexMarketShopListAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns.html
    """

    description = "Получение списка магазинов Yandex Market"
    http_method = "GET"
    resource_method = "campaigns"
    allowed_params = ["page", "pageSize"]


class GetYandexMarketShopAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id.html
    """

    description = "Получение информации о магазине Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}"
    required_params = [
        "shop_id",
    ]


class GetYandexMarketShopLoginListAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id-logins.html
    """

    description = "Получение списка логинов, у которых есть доступ к магазину Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/logins"
    required_params = [
        "shop_id",
    ]


class GetYandexMarketShopListByLoginAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-by-login.html
    """

    description = "Получение списка магазинов, к которым есть доступ по данному логину. Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/by_login/{login}"
    required_params = [
        "login",
    ]


class GetYandexMarketShopSettingsAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id-settings.html
    """

    description = "Получение настроек магазина Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/settings"
    required_params = [
        "shop_id",
    ]


class GetYandexMarketShopCategoriesAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id-feeds-categories.html
    """

    description = "Получение категорий магазина Яндекс.Маркета"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/feeds/categories"
    required_params = [
        "shop_id",
    ]


class GetYandexMarketOutletsAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id-outlets.html
    """

    description = "Получение точек продаж магазина Яндекс.Маркета"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/outlets"
    required_params = [
        "shop_id",
    ]


class GetYandexMarketAccountInfo(BaseAPI):
    http_method = "GET"

    def __init__(self, access_token: str, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token

    def build_url(self, params: dict) -> str:
        return f"https://login.yandex.ru/info?format=json&oauth_token={self.access_token}"

    def validate_attrs(self) -> None:
        pass
