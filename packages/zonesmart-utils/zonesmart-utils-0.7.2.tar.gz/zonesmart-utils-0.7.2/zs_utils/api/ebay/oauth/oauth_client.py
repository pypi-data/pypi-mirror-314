import base64
import simplejson
import logging
import urllib
import requests
from zs_utils.exceptions import CustomException

from django.utils.translation import gettext as _

from .model import environment, oAuth_token


class EbayOAuthClientError(CustomException):
    pass


class EbayOAuthClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        is_sandbox: bool,
        user_scopes: list = None,
        app_scopes: list = None,
        logger=None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        if is_sandbox:
            self.env_type = environment.SANDBOX
        else:
            self.env_type = environment.PRODUCTION

        self.user_scopes = user_scopes
        self.app_scopes = app_scopes

        self.headers = self._generate_request_headers()
        self.logger = logger or logging.getLogger(__name__)

    def _generate_request_headers(self) -> dict:
        b64_string = f"{self.client_id}:{self.client_secret}".encode()
        b64_encoded_credential = base64.b64encode(b64_string).decode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64_encoded_credential}",
        }
        return headers

    def generate_user_authorization_url(self, state: str = None) -> str:
        param = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "prompt": "login",
            "scope": " ".join(self.user_scopes),
        }

        if state is not None:
            param.update({"state": state})

        query = urllib.parse.urlencode(param)
        return f"{self.env_type.web_endpoint}?{query}"

    def _get_token(self, data: dict) -> oAuth_token:
        response = requests.post(self.env_type.api_endpoint, data=data, headers=self.headers)
        content = simplejson.loads(response.content)

        status = response.status_code
        if status != requests.codes.ok:
            raise EbayOAuthClientError(
                message=_("Не удалось получить токен: {error}").format(error=content["error_description"])
            )

        return oAuth_token(**content)

    def get_application_access_token(self) -> oAuth_token:
        body = {
            "grant_type": "client_credentials",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.app_scopes),
        }
        return self._get_token(data=body)

    def exchange_code_for_access_token(self, code: str) -> oAuth_token:
        body = {
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        return self._get_token(data=body)

    def get_user_access_token(self, refresh_token: str) -> oAuth_token:
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": " ".join(self.user_scopes),
        }
        return self._get_token(data=body)
