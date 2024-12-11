from model_utils.models import UUIDModel

from django.db import models
from django.utils import timezone


__all__ = [
    "AbstractAmocrmApp",
    "AmocrmApp",
]


class AbstractAmocrmApp(UUIDModel):
    client_id = models.TextField(verbose_name="ID приложения")
    client_secret = models.TextField(verbose_name="Секретный ключ приложения")
    redirect_uri = models.TextField(verbose_name="Redirect URI приложения")

    name = models.CharField(max_length=64, verbose_name="Локальный идентификатор")
    access_token = models.TextField(null=True, verbose_name="Токен доступа")
    access_token_expiry = models.DateTimeField(null=True, verbose_name="Дата истечения токена доступа")
    refresh_token = models.TextField(null=True, verbose_name="Токен для обновления токена доступа")
    refresh_token_expiry = models.DateTimeField(null=True, verbose_name="Дата истечения токена обновления")
    is_default = models.BooleanField(default=False, verbose_name="Приложение по умолчанию")

    class Meta:
        abstract = True

    @property
    def access_token_expired(self) -> bool:
        if self.access_token_expiry:
            return self.access_token_expiry < timezone.now() + timezone.timedelta(minutes=10)
        return False

    @property
    def refresh_token_expired(self) -> bool:
        if self.refresh_token_expiry:
            return self.refresh_token_expiry < timezone.now() + timezone.timedelta(minutes=10)
        return False


class AmocrmApp(AbstractAmocrmApp):
    pass
