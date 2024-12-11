from zs_utils.api.base_api import BaseAPI


class InsalesAPI(BaseAPI):
    def __init__(self, domain: str, token: str, **kwargs):
        super().__init__(**kwargs)

        self.url = f"https://{domain}"
        self.token = token

    def validate_attrs(self) -> None:
        pass

    @property
    def production_api_url(self) -> str:
        return f"{self.url}/admin/"

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Basic {self.token}",
            "Content-Type": "application/json",
        }
