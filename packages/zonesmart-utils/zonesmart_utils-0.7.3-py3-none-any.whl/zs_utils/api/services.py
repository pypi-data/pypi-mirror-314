import requests
import simplejson
from urllib.parse import parse_qs, urlparse
from rest_framework import status

from django.apps import apps
from django.conf import settings

from zs_utils.api import models


__all__ = [
    "ApiRequestLogService",
]


class ApiRequestLogService:
    """
    Сервис для работы с моделью APIRequestLog
    """

    @classmethod
    def get_request_log_model(cls) -> type[models.AbstractAPIRequestLog] | None:
        if getattr(settings, "API_REQUEST_LOG_MODEL", None):
            app_label, model_name = settings.API_REQUEST_LOG_MODEL.split(".")
            return apps.get_model(app_label=app_label, model_name=model_name)
        else:
            return models.APIRequestLog

    @classmethod
    def save_api_request_log(
        cls,
        status_code: int,
        url: str,
        method: str,
        request_headers: dict = None,
        response_headers: dict = None,
        request_body: dict = None,
        response_body: dict = None,
        response_time: float = None,
        user: settings.AUTH_USER_MODEL = None,
        save_if_is_success: bool = True,
        **extra_fields,
    ) -> models.AbstractAPIRequestLog:
        """
        Создание экземпляра модели AbstractAPIRequestLog по переданным данным (сохранение данных)
        """
        if (not save_if_is_success) and status.is_success(status_code):
            return None

        request_log_model = cls.get_request_log_model()
        if not request_log_model:
            raise ValueError("Необходимо задать настройку API_REQUEST_LOG_MODEL (путь к модели).")

        return request_log_model.objects.create(
            user=user,
            # Данные запроса
            url=url,
            method=method,
            params=parse_qs(urlparse(url).query),
            request_headers=request_headers,
            request_body=request_body,
            # Данные ответа
            response_time=response_time,
            status_code=status_code,
            response_headers=response_headers,
            response_body=response_body,
            **extra_fields,
        )

    @classmethod
    def save_api_request_log_by_response(
        cls,
        response: requests.Response,
        user: settings.AUTH_USER_MODEL = None,
        save_if_is_success: bool = True,
        **extra_fields,
    ) -> models.AbstractAPIRequestLog:
        """
        Создание экземпляра модели AbstractAPIRequestLog по переданному requests.Response (сохранение данных)
        """
        request = response.request

        request_body = request.body

        if isinstance(request_body, bytes):
            try:
                request_body = request_body.decode()
            except UnicodeDecodeError:
                request_body = str(request_body)

        if isinstance(request_body, str):
            try:
                request_body = simplejson.loads(request_body)
            except simplejson.JSONDecodeError:
                pass

        try:
            response_body = response.json()
        except simplejson.JSONDecodeError:
            response_body = None

        return cls.save_api_request_log(
            user=user,
            status_code=response.status_code,
            url=request.url,
            method=request.method,
            request_headers=dict(request.headers),
            response_headers=dict(response.headers),
            request_body=request_body,
            response_body=response_body,
            response_time=response.elapsed.microseconds / 1000,
            save_if_is_success=save_if_is_success,
            **extra_fields,
        )
