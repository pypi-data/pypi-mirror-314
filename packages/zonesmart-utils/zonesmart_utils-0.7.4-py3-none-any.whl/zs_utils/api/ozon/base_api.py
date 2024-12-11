from zs_utils.api.base_api import BaseAPI


class OzonAPI(BaseAPI):
    production_api_url = "https://api-seller.ozon.ru/"
    sandbox_api_url = "https://cb-api.ozonru.me/"
    http_method = "POST"

    def __init__(self, api_key: str, client_id: str, **kwargs):
        super().__init__(**kwargs)

        self.api_key = api_key
        self.client_id = client_id

    @property
    def headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "X-O3-App-Name": "zonesmart",
            "X-O3-App-Version": "zonesmart",
        }
        if self.is_sandbox:
            headers.update(
                {
                    "Api-Key": "0296d4f2-70a1-4c09-b507-904fd05567b9",
                    "Client-Id": "836",
                }
            )
        else:
            headers.update(
                {
                    "Api-Key": self.api_key,
                    "Client-Id": self.client_id,
                }
            )
        return headers
