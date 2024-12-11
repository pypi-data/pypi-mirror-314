from model_utils.models import TimeStampedModel, UUIDModel
from django.db import models
from django.contrib.auth import get_user_model

from zs_utils.file_utils import get_support_file_upload_path
from zs_utils.base_support import constants


__all__ = [
    "SupportTicket",
    "SupportTicketMessage",
    "SupportTicketMessageFile",
]

User = get_user_model()


class SupportTicket(TimeStampedModel, UUIDModel):
    """
    Данные тикета (запросов в поддержку)
    """
    number = models.TextField(verbose_name="Номер обращения")
    subject = models.CharField(max_length=300, verbose_name="Тема")
    status = models.TextField(choices=constants.SUPPORT_TICKET_STATUSES, verbose_name="Статус")
    question_type = models.TextField(verbose_name="Тип вопроса")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets", verbose_name="Создатель")
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Менеджер")

    class Meta:
        ordering = ["-created"]

    @property
    def client_status(self) -> constants.SUPPORT_TICKET_CLIENT_STATUSES:
        if self.status in constants.SUPPORT_TICKET_ACTIVE_STATUSES:
            if self.manager:
                last_message = self.last_message
                if last_message and (last_message.sender == self.manager):
                    return constants.SUPPORT_TICKET_CLIENT_STATUSES.RESPONDED
            return constants.SUPPORT_TICKET_CLIENT_STATUSES.PENDING
        else:
            return constants.SUPPORT_TICKET_CLIENT_STATUSES.CLOSED

    @property
    def is_active(self):
        """
        Тикет активный
        """
        return self.status in constants.SUPPORT_TICKET_ACTIVE_STATUSES

    @property
    def unread_messages(self) -> dict:
        """
        Не прочтённые сообщения
        """
        unread = self.messages.filter(is_system=False, is_viewed=False)
        return {
            "user": unread.exclude(sender=self.user).count(),
            "manager": unread.filter(sender=self.user).count(),
        }

    @property
    def last_message(self):
        """
        Последнее сообщение в данном обращении
        """
        return self.messages.filter(is_system=False).order_by("-created").first()


class SupportTicketMessage(TimeStampedModel, UUIDModel):
    """
    Данные сообщения тикета
    """
    text = models.TextField(max_length=constants.MAX_TEXT_LENGTH, null=True, blank=True, verbose_name="Сообщение")
    is_system = models.BooleanField(blank=True, default=False, verbose_name="Системное сообщение")
    is_viewed = models.BooleanField(blank=True, default=False, verbose_name="Просмотрено получателем")
    ticket = models.ForeignKey(
        "SupportTicket",
        on_delete=models.CASCADE,
        related_name="messages",
        related_query_name="message",
        verbose_name="Тикет",
    )
    sender = models.ForeignKey(
        to=User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор сообщения",
    )

    class Meta:
        ordering = ["-created"]

    @property
    def is_from_manager(self) -> bool:
        """
        Сообщение от менеджера
        """
        return self.ticket.manager and (self.sender == self.ticket.manager)

    @property
    def is_from_client(self) -> bool:
        """
        Сообщение от пользователя
        """
        return self.sender == self.ticket.user

    @property
    def recipient(self):
        """
        Получатель сообщения
        """
        if self.sender == self.ticket.user:
            return self.ticket.manager
        else:
            return self.ticket.user

    def set_viewed(self):
        """
        Пометить объект как просмотренный пользователем (is_viewed=True)
        """
        self.is_viewed = True
        self.save()


class SupportTicketMessageFile(UUIDModel):
    """
    Данные прикреплённого файла к сообщению тикета
    """
    file = models.FileField(upload_to=get_support_file_upload_path, verbose_name="Приложенный файл")
    ticket_message = models.ForeignKey(
        "SupportTicketMessage",
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
        verbose_name="Сообщение",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Создатель",
        null=True,
        blank=True,
    )

    @property
    def is_used(self) -> bool:
        if not self.ticket_message:
            raise NotImplemented
        return bool(self.ticket_message_id)

    @property
    def name(self) -> str:
        return self.file.name.split("/")[-1]
