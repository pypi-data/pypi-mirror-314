from django.conf import settings
from django.dispatch import receiver

from zs_utils.base_support import constants, models, serializers, services, signals
from zs_utils.import_utils import get_email_service
from zs_utils.websocket.services import WebsocketService


EmailService = get_email_service()


@receiver(signal=signals.support_ticket_status_changed)
def create_system_message(ticket: models.SupportTicket, prev_status: constants.SUPPORT_TICKET_STATUSES, **kwargs):
    if not constants.CREATE_SYSTEM_MESSAGE:
        return

    services.CommonSupportTicketService.create_system_message_after_status_change(
        ticket=ticket,
        prev_status=prev_status,
    )


@receiver(signal=signals.support_ticket_message_created)
def send_message_to_websocket(ticket_message: models.SupportTicketMessage, **kwargs):
    """
    Отправка данных о новом сообщении в websocket для пользователя и менеджера
    """
    ticket: models.SupportTicket = ticket_message.ticket
    recipients = {ticket_message.sender, ticket.user}
    if ticket_message.is_system and ticket.manager:
        recipients.add(ticket.manager)
    for user in recipients:
        if not user:
            continue
        WebsocketService.send_data_to_notification_group(
            user_id=user.id,
            notification=settings.WEBSOCKET_NOTIFICATION_GROUPS.support_ticket,
            data=serializers.CommonSupportTicketMessageSerializer(instance=ticket_message).data,
        )


@receiver(signal=signals.support_ticket_message_created)
def send_email_to_admins(ticket_message: models.SupportTicketMessage, **kwargs):
    """
    Отправка email уведомления админам о новом сообщении в запросе в поддержку
    """
    if ticket_message.is_from_client:
        text = ticket_message.text
        if not text:
            text = "Прикрепленные файлы без сообщения"
        EmailService.send_new_user_ticket_message_email(
            user=ticket_message.ticket.user,
            emails=constants.SUPPORT_EMAIL_LIST,
            ticket_id=str(ticket_message.ticket_id),
            message_text=text,
            first_name=ticket_message.ticket.user.first_name,
            user_img_url=constants.EMAIL_DUMMY_IMAGE_URL,
        )


@receiver(signal=signals.support_ticket_message_created)
def send_email_by_subscription(ticket_message: models.SupportTicketMessage, **kwargs):
    if not constants.SEND_EMAIL_BY_SUBSCRIPTION:
        return

    if not (ticket_message.sender and ticket_message.is_from_manager):
        return

    user_has_subscription = EmailService.user_has_subscription(
        user=ticket_message.ticket.user,
        event_type=constants.EVENT_TYPE_SUPPORT_TICKET_MESSAGE_CREATED,
    )

    if not user_has_subscription:
        return

    manager = ticket_message.sender
    EmailService.send_new_manager_ticket_message_email(
        user=ticket_message.ticket.user,
        ticket_id=str(ticket_message.ticket.id),
        message_text=ticket_message.text,
        manager=manager.full_name,
        manager_img_url=manager.avatar if manager.avatar else settings.EMAIL_DUMMY_IMAGE_URL,
    )
