import django.utils.timezone
import model_utils.fields
import uuid

from django.conf import settings
from django.db import migrations, models

from zs_utils.base_support import constants
from zs_utils.file_utils import get_support_file_upload_path


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SupportTicket",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "id",
                    model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                ("number", models.TextField(verbose_name="Номер обращения")),
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("PENDING", "Ожидает рассмотрения"),
                            ("OPEN", "Открыто"),
                            ("CLOSED_BY_USER", "Закрыто пользователем"),
                            ("CLOSED_BY_MANAGER", "Закрыто менеджером"),
                            ("CLOSED_AUTO", "Закрыто из-за отсутствия активности"),
                        ],
                        verbose_name="Статус",
                    ),
                ),
                ("question_type", models.TextField(verbose_name="Тип вопроса")),
                ("subject", models.CharField(max_length=300, verbose_name="Тема")),
                (
                    "manager",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Менеджер",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Создатель",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="SupportTicketMessage",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "id",
                    model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                (
                    "text",
                    models.TextField(
                        max_length=constants.MAX_TEXT_LENGTH, null=True, blank=True, verbose_name="Сообщение"
                    )
                ),
                ("is_system", models.BooleanField(blank=True, default=False, verbose_name="Системное сообщение")),
                ("is_viewed", models.BooleanField(blank=True, default=False, verbose_name="Просмотрено получателем")),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор сообщения",
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        related_query_name="message",
                        to="base_support.supportticket",
                        verbose_name="Тикет",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="SupportTicketMessageFile",
            fields=[
                (
                    "id",
                    model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=get_support_file_upload_path,
                        verbose_name="Приложенный файл",
                    ),
                ),
                (
                    "ticket_message",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        related_query_name="file",
                        to="base_support.supportticketmessage",
                        verbose_name="Сообщение",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Создатель",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
