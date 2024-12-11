from zs_utils.api.base_api import BaseAPI


__all__ = [
    "YandexMarketAPI",
]


class YandexMarketAPI(BaseAPI):
    production_api_url = "https://api.partner.market.yandex.ru/v2/"

    def __init__(self, access_token: str, api_key: str, **kwargs):
        super().__init__(**kwargs)

        self.api_key = api_key
        self.access_token = access_token

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"OAuth oauth_token={self.access_token}, oauth_client_id={self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
            "Accept-Encoding": "application/gzip",
        }

    def build_url(self, params: dict) -> str:
        return super().build_url(params) + ".json"
