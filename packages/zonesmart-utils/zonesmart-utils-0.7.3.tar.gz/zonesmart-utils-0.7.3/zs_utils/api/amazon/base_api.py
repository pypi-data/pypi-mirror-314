from zs_utils.api.base_api import BaseAPI


class AmazonAPI(BaseAPI):
    production_api_url = "https://sellingpartnerapi-{region}.amazon.com/"
    region_to_marketplace_ids = {
        "na": [
            "A2EUQ1WTGCTBG2",
            "ATVPDKIKX0DER",
            "A1AM78C64UM0Y8",
            "A2Q3Y263D00KWC",
        ],
        "eu": [
            "A1RKKUPIHCS9HS",
            "A1F83G8C2ARO7P",
            "A13V1IB3VIYZZH",
            "AMEN7PMS3EDWL",
            "A1805IZSGTT6HS",
            "A1PA6795UKMFR9",
            "APJ6JRA9NG5V4",
            "A2NODRKZP88ZB9",
            "AE08WJ6YKNBMC",
            "A1C3SOZRARQ6R3",
            "ARBP9OOSHTCHU",
            "A33AVAJ2PDY3EV",
            "A17E79C6D8DWNP",
            "A2VIGQ35RCS4UG",
            "A21TJRUUN4KGV",
        ],
        "fe": [
            "A19VAU5U5O7RUS",
            "A39IBJ37TRP1C6",
            "A1VC38T7YXB528",
        ],
    }

    def __init__(self, access_token: str, marketplace_id: str, url: str = None, **kwargs):
        super().__init__(**kwargs)

        for region, marketplace_ids in self.region_to_marketplace_ids.items():
            if marketplace_id in marketplace_ids:
                self.region = region
                break
        else:
            all_marketplace_ids = [
                item for marketplace_ids in self.region_to_marketplace_ids.values() for item in marketplace_ids
            ]
            raise ValueError("Доступные значения для 'marketplace_id': " + ", ".join(all_marketplace_ids))

        self.production_api_url = url if url else self.production_api_url.format(region=region)
        self.access_token = access_token

    @property
    def headers(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "x-amz-access-token": self.access_token,
        }
        return headers

    def get_payload(self, params: dict) -> dict | list:
        return params.pop("payload", {})

    def get_request_params(self, **kwargs) -> dict:
        """
        Получение всех параметров, необходимых для запроса (url, headers, params, json, files)
        """

        request_params = {
            "url": self.build_url(kwargs),
            "headers": self.headers,
        }

        clean_params = self.get_clean_params(kwargs)

        files = clean_params.pop("files", None)
        if files:
            request_params["files"] = files

        if self.http_method in ["POST", "PUT", "PATCH"]:
            request_params["json"] = self.get_payload(params=clean_params)
        request_params["params"] = clean_params
        return request_params
