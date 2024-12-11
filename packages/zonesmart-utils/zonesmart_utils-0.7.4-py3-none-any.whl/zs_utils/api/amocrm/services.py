import requests

from django.db import transaction
from django.db.models import QuerySet
from django.apps import apps
from django.conf import settings
from django.utils import timezone

from zs_utils.api.amocrm import models


__all__ = [
    "AmocrmService",
]


class AmocrmService:
    @classmethod
    def get_amocrm_app_model(cls, raise_exception: bool = True) -> type[models.AbstractAmocrmApp] | None:
        if getattr(settings, "AMOCRM_APP_MODEL", None):
            app_label, model_name = settings.AMOCRM_APP_MODEL.split(".")
            model = apps.get_model(app_label=app_label, model_name=model_name)
        else:
            model = models.AmocrmApp

        if (not model) and raise_exception:
            raise ValueError("Необходимо задать настройку 'AMOCRM_APP_MODEL'.")

        return model

    @classmethod
    def get_amocrm_app(cls, app_id: str) -> models.AbstractAmocrmApp:
        return cls.get_amocrm_app_model(raise_exception=True).objects.get(id=app_id)

    @classmethod
    def get_default_amocrm_app(cls) -> models.AbstractAmocrmApp:
        return cls.get_amocrm_app_model(raise_exception=True).objects.get(is_default=True)

    @classmethod
    def retrieve_amocrm_tokens(
        cls,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        refresh_token: str = None,
        code: str = None,
    ) -> dict:
        """
        Получение новых токенов доступа и обновления либос помощью текущего токена обновления,
        либо с помощью одноразового кода.
        Docs: https://www.amocrm.ru/developers/content/oauth/step-by-step#get_access_token
        """

        assert bool(refresh_token) != bool(code), "Необходимо задать либо 'refresh_token', либо 'code'."

        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        if refresh_token:
            payload.update({"grant_type": "refresh_token", "refresh_token": refresh_token})
        else:
            payload.update({"grant_type": "authorization_code", "code": code})

        response = requests.post(url=settings.AMOCRM_API_URL + "oauth2/access_token", json=payload)
        response.raise_for_status()

        return response.json()

    @classmethod
    @transaction.atomic()
    def refresh_amocrm_access_token(cls, app_id: str = None) -> str:
        """
        Получение токена доступа amoCRM
        """

        app_qs: QuerySet[models.AbstractAmocrmApp] = cls.get_amocrm_app_model(
            raise_exception=True
        ).objects.select_for_update()
        if app_id:
            app = app_qs.get(id=app_id)
        else:
            app = app_qs.get(is_default=True)
        if not app.refresh_token:
            raise ValueError("Отсутствует токен обновления AmoCRM.")

        # Получение новых токенов
        response_data: dict = cls.retrieve_amocrm_tokens(
            client_id=app.client_id,
            client_secret=app.client_secret,
            redirect_uri=app.redirect_uri,
            refresh_token=app.refresh_token,
        )

        # Сохранение нового refresh_token
        app.access_token = response_data["access_token"]
        app.access_token_expiry = timezone.now() + timezone.timedelta(seconds=response_data["expires_in"])
        app.refresh_token = response_data["refresh_token"]
        app.refresh_token_expiry = timezone.now() + timezone.timedelta(days=90)
        app.save()

        return app.access_token

    @classmethod
    def refresh_amocrm_apps(cls) -> None:
        if not settings.AMOCRM_APPS:
            return None

        for app_config in settings.AMOCRM_APPS:
            for key in [
                "name",
                "is_default",
                "client_id",
                "client_secret",
                "redirect_uri",
            ]:
                if app_config.get(key) is None:
                    raise ValueError(f"У конфига приложения amoCRM не задан ключ '{key}'.")

        if sum(int(app_config["is_default"]) for app_config in settings.AMOCRM_APPS) != 1:
            raise ValueError("Среди приложений amoCRM ровно одно должно быть приложением по умолчанию.")

        app_model = cls.get_amocrm_app_model(raise_exception=True)

        for app_config in settings.AMOCRM_APPS:
            app_model.objects.update_or_create(name=app_config["name"], defaults=app_config)
