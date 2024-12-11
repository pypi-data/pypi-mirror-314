from zs_utils.api.base_api import BaseAPI
from zs_utils.api.ebay.utils import custom_quote


__all__ = [
    "EbayAPI",
]


class EbayAPI(BaseAPI):
    production_api_url = "https://api.ebay.com/"
    sandbox_api_url = "https://api.sandbox.ebay.com/"

    params_to_quote = [
        "sku",
        "inventoryItemGroupKey",
        "merchantLocationKey",
    ]

    # TODO: валидация?
    MAX_LIMIT = 100
    MAX_OFFSET = 99

    def __init__(self, access_token: str, marketplace_id: str = None, **kwargs):
        super().__init__(**kwargs)

        self.access_token = access_token
        self.marketplace_id = marketplace_id

    @property
    def headers(self):
        # DOCS: https://developer.ebay.com/api-docs/static/rest-request-components.html#marketpl
        DOMAIN_TO_LOCALE = {
            "EBAY_AT": "de-AT",
            "EBAY_AU": "en-AU",
            "EBAY_BE": "fr-BE",
            "EBAY_CA": "en-CA",
            "EBAY_CH": "de-CH",
            "EBAY_DE": "de-DE",
            "EBAY_ES": "es-ES",
            "EBAY_FR": "fr-FR",
            "EBAY_GB": "en-GB",
            "EBAY_HK": "zh-HK",
            "EBAY_IE": "en-IE",
            "EBAY_IN": "en-GB",
            "EBAY_IT": "it-IT",
            "EBAY_MY": "en-MY",
            "EBAY_NL": "nl-NL",
            "EBAY_PH": "en-PH",
            "EBAY_PL": "pl-PL",
            "EBAY_TH": "th-TH",
            "EBAY_TW": "zh-TW",
        }
        locale = DOMAIN_TO_LOCALE.get(self.marketplace_id)
        if not locale:
            locale = "en-US"
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Language": locale,
            "Content-Type": "application/json",
            "Accept-Language": locale,
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
            "Accept-Encoding": "application/gzip",
            "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
        }

    def build_url(self, params: dict):
        next_url = params.pop("next_url", None)
        if next_url:
            url = self.sandbox_api_url if self.is_sandbox else self.production_api_url
            if next_url.startswith("/"):
                url += next_url
            else:
                url = next_url
            return url
        else:
            return super().build_url(params=params)

    def get_path_params(self, params: dict):
        path_params = super().get_path_params(params)
        return {
            param: custom_quote(value)
            for param, value in path_params.items()
            if value and (param in self.params_to_quote)
        }

    def get_clean_params(self, params: dict) -> dict:
        clean_params = {
            "next_url": params.get("next_url"),
            "payload": params.get("payload"),
        }
        if not params.get("next_url"):
            clean_params.update(super().get_clean_params(params))

            for param in self.params_to_quote:
                if clean_params.get(param):
                    clean_params[param] = custom_quote(clean_params[param])

        return clean_params

    def get_payload(self, params: dict):
        return params.pop("payload", None)
