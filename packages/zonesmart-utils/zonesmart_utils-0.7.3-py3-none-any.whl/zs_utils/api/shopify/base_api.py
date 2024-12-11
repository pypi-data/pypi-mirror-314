from django.conf import settings

from zs_utils.api.base_api import BaseAPI


class ShopifyAPI(BaseAPI):
    payload_key = None

    def __init__(self, access_token: str, shop_url: str, **kwargs):
        self.access_token = access_token
        self.shop_url = shop_url

        super().__init__(**kwargs)

    @property
    def production_api_url(self):
        return f"https://{self.shop_url}/admin/api/{settings.SHOPIFY_API_VERSION}/"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

    def get_payload(self, params: dict):
        return {self.payload_key: params} if self.payload_key else params
