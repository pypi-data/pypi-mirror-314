from django.contrib.postgres.fields import ArrayField
from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

from zs_utils.data.enums import LANGUAGES
from zs_utils.file_utils import get_email_notification_file_upload_path
from zs_utils.json_utils import CustomJSONEncoder


class EmailNotification(UUIDModel, TimeStampedModel):
    """
    Модель email-уведомления (письма)
    """

    sender = models.CharField(max_length=64, verbose_name="Отправитель")
    receivers = ArrayField(models.CharField(max_length=64), verbose_name="Получатели")
    language = models.CharField(max_length=2, choices=LANGUAGES, verbose_name="Язык")
    template_name = models.CharField(max_length=64, verbose_name="Шаблон")
    template_params = models.JSONField(
        blank=True,
        default=dict,
        encoder=CustomJSONEncoder,
        verbose_name="Параметры шаблона",
    )

    is_urgent = models.BooleanField(default=False, verbose_name="Уведомление срочное")
    is_sent = models.BooleanField(default=False, verbose_name="Уведомление отправлено")

    class Meta:
        ordering = ["-created"]


class EmailNotificationFile(UUIDModel):
    """
    Вложения для email-уведомлений
    """

    email_notification = models.ForeignKey(
        EmailNotification,
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
        verbose_name="Уведомление",
    )
    name = models.CharField(max_length=255, verbose_name="Имя файла", default="")
    file = models.FileField(upload_to=get_email_notification_file_upload_path, verbose_name="Файл")

    class Meta:
        ordering = ["name"]
