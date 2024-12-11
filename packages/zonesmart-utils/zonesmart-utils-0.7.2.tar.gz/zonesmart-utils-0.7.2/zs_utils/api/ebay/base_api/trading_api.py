from abc import abstractmethod
from ebaysdk.exception import ConnectionError as BaseEbayTradingAPIError
from ebaysdk.trading import Connection as BaseEbayTradingAPI
from ebaysdk.response import Response as EbaySDKResponse

from zs_utils.api.base_api import BaseAPI
from zs_utils.api.ebay.data.marketplace.marketplace_to_site import (
    EbayDomainCodeToSiteID,
)


__all__ = [
    "EbayTradingAPI",
]


class EbayTradingAPI(BaseAPI):
    def __init__(
        self,
        access_token: str,
        client_id: str,
        client_secret: str,
        dev_id: str,
        site_id: str = None,
        domain_code: str = None,
        debug: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.dev_id = dev_id
        self.site_id = site_id
        self.domain_code = domain_code
        self.debug = debug

    def validate_attrs(self) -> None:
        pass

    @property
    @abstractmethod
    def method_name(self) -> str:
        pass

    @abstractmethod
    def get_params(self, **kwargs) -> dict:
        pass

    def _clean_data(self, data: dict) -> dict:
        cleaned_data = {}
        for key, value in data.items():
            if value or type(value) in [bool, int]:
                if isinstance(value, dict):
                    cleaned_data.update({key: self._clean_data(value)})
                else:
                    cleaned_data.update({key: value})
        return cleaned_data

    def get_site_id(self, site_id: str = None, domain_code: str = None) -> str:
        if site_id:
            if site_id not in EbayDomainCodeToSiteID.values():
                raise BaseEbayTradingAPIError(msg=f"Неизвестный 'site_id'={site_id}")
        elif domain_code:
            if domain_code not in EbayDomainCodeToSiteID.keys():
                raise BaseEbayTradingAPIError(msg=f"Маркетплейс '{domain_code}' не поддерживается Trading API.")
            else:
                site_id = EbayDomainCodeToSiteID[domain_code]
        else:
            site_id = EbayDomainCodeToSiteID["default"]

        return site_id

    def make_request(self, **kwargs) -> EbaySDKResponse:
        params = self.get_params(**kwargs)
        cleaned_params = self._clean_data(params)

        api = BaseEbayTradingAPI(
            iaf_token=self.access_token,
            appid=self.client_id,
            devid=self.dev_id,
            certid=self.client_secret,
            siteid=self.get_site_id(site_id=self.site_id, domain_code=self.domain_code),
            config_file=None,
            debug=self.debug,
        )
        return api.execute(
            verb=self.method_name,
            data=cleaned_params,
        )
