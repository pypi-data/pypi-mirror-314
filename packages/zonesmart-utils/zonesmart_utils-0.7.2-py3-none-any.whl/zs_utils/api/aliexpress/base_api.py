import json
from datetime import datetime
from hashlib import md5
from zs_utils.api.base_api import BaseAPI


class AliexpressAPI(BaseAPI):
    production_api_url = "http://gw.api.taobao.com/router/rest"
    sandbox_url = "http://gw.api.tbsandbox.com/router/rest"
    http_method = "POST"

    def __init__(self, app_key: str, app_secret: str, access_token: str, **kwargs):
        super().__init__(**kwargs)

        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token

    def build_url(self, params: dict) -> str:
        return self.sandbox_api_url if self.is_sandbox else self.production_api_url

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def add_sign(self, params):
        params.update(
            {
                "session": self.access_token,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "app_key": self.app_key,
                "format": "json",
                "v": "2.0",
                "sign_method": "md5",
                "method": self.resource_method,
            }
        )
        params = dict(sorted(params.items()))
        for_sign = self.app_secret + str().join([key + value for key, value in params.items()]) + self.app_secret
        sign = md5(for_sign.encode("utf-8")).hexdigest().upper()
        params["sign"] = sign
        return params

    def get_clean_params(self, params):
        clean_params = super().get_clean_params(params=params)

        for key, value in clean_params.items():
            if (not isinstance(value, str)) and (value is not None):
                clean_params[key] = json.dumps(value)

        files = clean_params.pop("files", None)
        params_with_sign = self.add_sign(clean_params)
        params_with_sign["files"] = files  # TODO: это нужно?
        return params_with_sign

    def get_request_params(self, **kwargs) -> dict:
        clean_params = self.get_clean_params(kwargs)
        return dict(
            url=self.build_url(kwargs),
            headers=self.headers,
            data=clean_params,
        )
