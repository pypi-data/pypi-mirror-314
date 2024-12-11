from zs_utils.api.base_api import BaseAPI


class EtsyAPI(BaseAPI):
    production_api_url = "https://openapi.etsy.com/v3/application/"

    def __init__(self, access_token: str, api_key: str, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token
        self.api_key = api_key

    @property
    def headers(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "x-api-key": self.api_key,
        }
        if self.http_method in ["POST", "PUT", "PATCH"]:
            headers.update(
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Accept-Charset": "utf-8",
                    "Accept-Encoding": "application/gzip",
                }
            )
        return headers

    @staticmethod
    def get_user_id(access_token: str):
        return int(access_token.split(".")[0])

    def build_url(self, params: dict) -> str:
        if "user_id" in self.path_params:
            params["user_id"] = self.get_user_id(access_token=self.access_token)
        return super().build_url(params)
