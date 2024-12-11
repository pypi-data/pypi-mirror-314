from zs_utils.api.base_api import BaseAPI


class FedexAPI(BaseAPI):
    production_api_url = "https://apis.fedex.com"
    sandbox_api_url = "https://apis-sandbox.fedex.com"

    def __init__(self, access_token: str, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "X-locale": "en_US",
            "Authorization": f"Bearer {self.access_token}",
        }
