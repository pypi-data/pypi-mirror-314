from zs_utils.api.base_api import BaseAPI


class ApishipAPI(BaseAPI):
    production_api_url = "https://api.apiship.ru/v1/"
    sandbox_api_url = "http://api.dev.apiship.ru/v1/"

    def __init__(self, access_token: str = None, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token

    @property
    def headers(self) -> dict:
        header = {
            "Content-Type": "application/json",
        }
        if self.access_token:
            header["Authorization"] = self.access_token
        return header
