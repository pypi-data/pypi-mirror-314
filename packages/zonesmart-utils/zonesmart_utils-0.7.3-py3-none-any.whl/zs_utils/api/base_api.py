import logging
import requests
import re
from abc import ABC


__all__ = [
    "BaseAPI",
]


class BaseAPI(ABC):
    required_params = []
    allowed_params = []

    # Тело запроса -- список, а не словарь
    array_payload = False

    # Отбрасывать параметры с пустым значением (None или "")
    drop_empty_params = False

    http_method = None
    resource_method = None
    production_api_url = None
    sandbox_api_url = None

    def __init__(
        self,
        logger=None,
        is_sandbox: bool = False,
        response_timeout: float = 30,
        **kwargs,
    ):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.is_sandbox = is_sandbox
        self.response_timeout = response_timeout

        self.validate_attrs()

    def validate_attrs(self) -> None:
        """
        Валидация обязательных атрибутов у дочерних классов
        """
        for attr in [
            "http_method",
            "resource_method",
            "production_api_url",
        ]:
            if not getattr(self, attr, None):
                raise ValueError(f"Необходимо определить атрибут '{attr}'.")

        if self.is_sandbox and (not self.sandbox_api_url):
            raise ValueError("Для использования тестового режима необходимо указать 'sandbox_api_url'")

        if self.array_payload:
            if (self.required_params and (self.required_params != ["array_payload"])) or self.allowed_params:
                raise ValueError(
                    "Если стоит флаг 'array_payload', то единственным возможным и обязательным параметром является параметр 'array_payload'."
                )
            self.required_params = ["array_payload"]

    @property
    def headers(self) -> dict:
        """
        Headers для запросов к API
        """
        return {}

    @property
    def path_params(self) -> list[str]:
        return re.findall(pattern=r"\{([^\}]+)\}", string=self.resource_method)

    def build_url(self, params: dict) -> str:
        """
        Составление url для запросов к API (подстановка эндпоинта и url-параметром в url)
        """
        url = self.sandbox_api_url if self.is_sandbox else self.production_api_url
        url += self.resource_method

        path_params = {}
        for param in self.path_params:
            if params.get(param):
                path_params[param] = params[param]
            else:
                raise ValueError(f"Отсутствует обязательный параметр '{param}'.")

        if path_params:
            url = url.format(**path_params)
            if url[-1] == "/":
                url = url[:-1]
        return url

    def get_clean_params(self, params: dict) -> dict:
        """
        Отчистка и валидация параметров запроса
        В итоговый запрос попадут только ключи из required_params и allowed_param
        """
        clean_params = {}
        files = {}

        for req_param in self.required_params:
            if req_param not in params:
                raise ValueError(f"Обязательный параметр запроса '{req_param}' не задан.")

            if isinstance(params[req_param], bytes):
                files[req_param] = params[req_param]
            else:
                clean_params[req_param] = params[req_param]

        for allowed_param in self.allowed_params:
            if allowed_param in params:
                if isinstance(params[allowed_param], bytes):
                    files[allowed_param] = params[allowed_param]
                else:
                    clean_params[allowed_param] = params[allowed_param]

        if self.drop_empty_params:
            clean_params = {k: v for k, v in clean_params.items() if ((v is not None) and (v != ""))}

        clean_params["files"] = files if files else None

        return clean_params

    def get_payload(self, params: dict) -> dict | list:
        """
        Получение body для POST запросов
        """

        if self.array_payload:
            return params["array_payload"]
        return params

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
        else:
            request_params["params"] = clean_params

        return request_params

    def make_request(self, **kwargs) -> requests.Response:
        """
        Непосредственный запрос к API
        """
        return requests.request(
            method=self.http_method,
            timeout=self.response_timeout,
            **self.get_request_params(**kwargs),
        )
