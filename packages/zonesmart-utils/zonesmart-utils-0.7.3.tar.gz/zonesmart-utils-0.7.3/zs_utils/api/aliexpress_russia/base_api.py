from zs_utils.api.base_api import BaseAPI


class AliexpressRussiaAPI(BaseAPI):
    production_api_url = "https://openapi.aliexpress.ru"
    http_method = "POST"

    def __init__(self, access_token: str, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token

    @property
    def headers(self) -> dict:
        return {
            "x-auth-token": self.access_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
