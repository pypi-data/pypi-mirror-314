from django.utils import timezone
from django.db import transaction


from zs_utils.exceptions import CustomException
from zs_utils.base_support import constants, models, signals


__all__ = [
    "CommonSupportTicketService",
    "SupportTicketServiceException",
]


class SupportTicketServiceException(CustomException):
    pass


class CommonSupportTicketService:
    """
    Сервис для работы с тикетами (SupportTicket)
    """
    @classmethod
    def max_active_tickets_opened(cls, user) -> bool:
        """
        Проверка, что было открыто максимальное кол-во тикетов для пользователя user
        """
        return (
            constants.MAX_OPEN_TICKET
            <= models.SupportTicket.objects.filter(
                user=user, status__in=constants.SUPPORT_TICKET_ACTIVE_STATUSES_LIST
            ).count()
        )

    @classmethod
    def check_user_can_open_new_ticket(cls, user) -> None:
        """
        Проверка, что пользователь user может открыть новый тикет
        """
        if cls.max_active_tickets_opened(user=user):
            raise SupportTicketServiceException(message="Открыто максимальное количество заявок.")

    @classmethod
    def _generate_ticket_number(cls, user) -> str:
        """
        Генерация number для ticket
        """
        ticket_count = str(user.tickets.all().count() + 1)
        final_user_id = (4 - len(str(user.id))) * "0" + str(user.id)
        final_ticket_count = (3 - len(ticket_count)) * "0" + ticket_count
        return final_user_id + final_ticket_count

    @classmethod
    def create_ticket(
        cls,
        user,
        question_type: constants.SUPPORT_TICKET_QUESTION_TYPES,
        subject: str,
    ) -> models.SupportTicket:
        cls.check_user_can_open_new_ticket(user=user)

        return models.SupportTicket.objects.create(
            user=user,
            status=constants.SUPPORT_TICKET_STATUSES.PENDING,
            number=cls._generate_ticket_number(user=user),
            question_type=question_type,
            subject=subject,
        )

    @classmethod
    def create_ticket_message(
        cls,
        ticket: models.SupportTicket,
        sender,
        is_system: bool,
        text: str = None,
        files: list[models.SupportTicketMessageFile] = None,
    ) -> models.SupportTicketMessage:
        """
        Создание сообщения тикета и вложений
        """
        assert text or files, "Необходимо задать текст или файлы"
        if is_system:
            assert text and (not files), "Системное сообщение может быть только текстовым"
            assert not sender, "У системного сообщения не может быть отправителя"
        else:
            assert sender, "У пользовательского сообщения должен быть отправитель"

            if not ticket.is_active:
                raise SupportTicketServiceException(message="Заявка закрыта.")
            if sender not in [ticket.user, ticket.manager]:
                raise SupportTicketServiceException(message="Нельзя написать сообщение в чужую заявку.")

        signature = constants.SUPPORT_TICKET_MESSAGE_SIGNATURE
        if signature and text and (sender == ticket.manager):
            text += signature

        prev_ticket_client_status = ticket.client_status

        with transaction.atomic():
            ticket_message = models.SupportTicketMessage.objects.create(
                ticket=ticket,
                text=text,
                sender=sender,
                is_system=is_system,
                is_viewed=is_system,
            )
            if files:
                models.SupportTicketMessageFile.objects.filter(
                    id__in=[file.id for file in files]
                ).update(ticket_message=ticket_message)

        signals.support_ticket_message_created.send(
            sender=None, ticket_message=ticket_message, prev_ticket_client_status=prev_ticket_client_status
        )

        return ticket_message

    @classmethod
    def create_system_message_after_status_change(
        cls,
        ticket: models.SupportTicket,
        prev_status: constants.SUPPORT_TICKET_STATUSES,
    ) -> models.SupportTicketMessage:
        """
        Создание системного сообщения для тикета ticket после изменения его статуса
        """
        new_status = ticket.status
        text = None

        if prev_status in constants.SUPPORT_TICKET_ACTIVE_STATUSES:
            if new_status == constants.SUPPORT_TICKET_STATUSES.OPEN:
                text = dict(constants.SUPPORT_TICKET_MESSAGES).get("OPEN")
            elif new_status == constants.SUPPORT_TICKET_STATUSES.CLOSED_AUTO:
                text = dict(constants.SUPPORT_TICKET_MESSAGES).get("CLOSED_AUTO")
            elif new_status == constants.SUPPORT_TICKET_STATUSES.CLOSED_BY_USER:
                text = dict(constants.SUPPORT_TICKET_MESSAGES).get("CLOSED_BY_USER")
            elif new_status == constants.SUPPORT_TICKET_STATUSES.CLOSED_BY_MANAGER:
                text = dict(constants.SUPPORT_TICKET_MESSAGES).get("CLOSED_BY_MANAGER")
        else:
            if new_status == constants.SUPPORT_TICKET_STATUSES.OPEN:
                text = dict(constants.SUPPORT_TICKET_MESSAGES).get("REOPEN")

        if not text:
            raise NotImplementedError(f"Сообщение для смены статуса '{prev_status}' -> '{new_status}' неопределено.")

        return cls.create_ticket_message(ticket=ticket, text=text, sender=None, is_system=True)

    @classmethod
    def close_ticket(cls, user, ticket) -> None:
        if not ticket.is_active:
            raise SupportTicketServiceException(message="Заявка закрыта.")

        if ticket.user == user:
            status = constants.SUPPORT_TICKET_STATUSES.CLOSED_BY_USER
        elif ticket.manager == user:
            status = constants.SUPPORT_TICKET_STATUSES.CLOSED_BY_MANAGER
        else:
            raise SupportTicketServiceException(message="Нельзя закрыть чужую заявку.")

        cls.set_ticket_status(ticket=ticket, status=status)

    @classmethod
    def reopen_ticket(cls, user, ticket) -> None:
        cls.check_user_can_open_new_ticket(user=user)

        if ticket.is_active:
            raise SupportTicketServiceException(message="Заявка открыта.")

        cls.set_ticket_status(ticket=ticket, status=constants.SUPPORT_TICKET_STATUSES.OPEN)

    @classmethod
    def take_ticket(cls, manager, ticket) -> None:
        assert manager.is_staff

        if not ticket.is_active:
            raise SupportTicketServiceException(message="Заявка закрыта.")

        ticket.manager = manager
        ticket.save()

        cls.set_ticket_status(ticket=ticket, status=constants.SUPPORT_TICKET_STATUSES.OPEN)

    @classmethod
    def set_ticket_viewed(cls, user, ticket) -> None:
        ticket.messages.exclude(sender=user).update(is_viewed=True)

    @classmethod
    def set_ticket_status(cls, ticket, status: constants.SUPPORT_TICKET_STATUSES) -> None:
        """
        Установка нового статуса status для тикета ticket
        """

        if ticket.status != status:
            prev_status = ticket.status
            ticket.status = status
            ticket.save()

            signals.support_ticket_status_changed.send(sender=None, ticket=ticket, prev_status=prev_status)

    @classmethod
    def close_inactive_tickets(cls) -> None:
        """
        Закрытие всех неактивных обращений в поддержку после settings.AUTO_CLOSE_TICKET_AFTER
        """
        now = timezone.now()
        for ticket in models.SupportTicket.objects.filter(
                status=constants.SUPPORT_TICKET_ACTIVE_STATUSES.OPEN
        ):
            if ticket.manager:
                last_message = ticket.last_message
                # Последнее сообщение отправлено больше заданного кол-ва дней назад
                if (
                    last_message
                    and (last_message.sender == ticket.manager)
                    and (now > last_message.created + timezone.timedelta(days=constants.AUTO_CLOSE_TICKET_AFTER))
                ):
                    cls.set_ticket_status(ticket=ticket, status=constants.SUPPORT_TICKET_STATUSES.CLOSED_AUTO)
