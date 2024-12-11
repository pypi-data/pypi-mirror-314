from zs_utils.api.base_api import BaseAPI


class ShipstationAPI(BaseAPI):
    production_api_url = "https://ssapi.shipstation.com/"

    def __init__(self, access_token: str, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Basic {self.access_token}",
            "Content-Type": "application/json",
        }
