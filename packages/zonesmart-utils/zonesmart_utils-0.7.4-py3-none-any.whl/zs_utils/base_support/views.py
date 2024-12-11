from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from zs_utils.permissions import StaffPermission
from zs_utils.base_support import constants, filters, models, serializers, services
from zs_utils.views import CustomModelViewSet


__all__ = [
    "BaseSupportTicketView",
    "BaseSupportTicketMessageView",
    "BaseSupportTicketMessageFileView",
]


class BaseSupportTicketView(CustomModelViewSet):
    """
    View для создания и просмотра тикетов (SupportTicket)
    """
    serializer_class = (
        serializers.CommonSupportTicketWithMessagesSerializer
        if constants.TICKET_WITH_MESSAGES
        else serializers.CommonSupportTicketSerializer
    )
    filterset_class = filters.SupportTicketFilter
    not_allowed_actions = [
        "destroy",
        "update",
        "partial_update",
    ]

    @classmethod
    def get_support_ticket_service(cls):
        return services.CommonSupportTicketService

    @action(detail=True, methods=["POST"])
    def close(self, request, *args, **kwargs):
        """
        Закрытие тикета
        """
        self.get_support_ticket_service().close_ticket(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    def create(self, request, *args, **kwargs):
        data = self.get_validated_data(serializer_class=serializers.CommonCreateSupportTicketSerializer)
        message = data.pop("message") if "message" in data else None
        user = self.get_user()
        with transaction.atomic():
            instance = self.get_support_ticket_service().create_ticket(user=user, **data)
            if message:
                self.get_support_ticket_service().create_ticket_message(
                    ticket=instance, sender=user, is_system=False, **message
                )
        return self.build_response(data=self.get_serializer_class()(instance).data, status_code=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], permission_classes=[StaffPermission])
    def take_to_work(self, request, *args, **kwargs):
        """
        Взятие тикета в работу (для staff пользователей)
        """
        self.get_support_ticket_service().take_ticket(manager=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=True, methods=["POST"])
    def reopen(self, request, *args, **kwargs):
        """
        Открыть закрытый тикет
        """
        self.get_support_ticket_service().reopen_ticket(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=True, methods=["POST"])
    def set_viewed(self, request, *args, **kwargs):
        self.get_support_ticket_service().set_ticket_viewed(user=self.get_user(), ticket=self.get_object())
        return self.build_response()

    @action(detail=False, methods=["GET"])
    def get_metadata(self, request, *args, **kwargs):
        """
        Получение метаданных тикета (возможные статусы и тип вопроса)
        """
        data = {
            "status": constants.SUPPORT_TICKET_STATUSES,
            "question_type": constants.SUPPORT_TICKET_QUESTION_TYPES,
        }
        return self.build_response(data=data)


class BaseSupportTicketMessageView(CustomModelViewSet):
    """
    View для создания/удаления/обновления/просмотра сообщений тикета (SupportTicketMessage)
    """
    serializer_class = serializers.CommonSupportTicketMessageSerializer
    not_allowed_actions = [
        "update",
        "partial_update",
        "destroy",
    ]

    @classmethod
    def get_support_ticket_service(cls):
        return services.CommonSupportTicketService

    def get_queryset_filter_kwargs(self) -> dict:
        return {"ticket": self.kwargs["ticket_id"]}

    def create(self, request, *args, **kwargs):
        """
        Подстановка тикета SupportTicket.id и пользователя (отправителя) при создании нового сообщения
        """
        data = self.get_validated_data(serializer_class=serializers.CommonCreateSupportTicketMessageSerializer)
        ticket = models.SupportTicket.objects.get(id=kwargs["ticket_id"])
        sender = self.get_user()

        instance = self.get_support_ticket_service().create_ticket_message(
            ticket=ticket, sender=sender, is_system=False, **data,
        )
        return self.build_response(data=self.serializer_class(instance).data, status_code=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def set_viewed(self, request, *args, **kwargs):
        """
        Пометить сообщения тикета как просмотренные пользователем
        """
        message_id = self.kwargs.get("pk")
        if message_id:
            message = self.get_object()
            message.set_viewed()
        else:
            self.get_queryset().update(is_viewed=True)
        return Response(data={"message": "viewed_message"})


class BaseSupportTicketMessageFileView(CustomModelViewSet):
    """
    View для создания/удаления/обновления/просмотра файлов сообщений (SupportTicketMessageFile)
    """
    serializer_class = serializers.CommonSupportTicketMessageFileSerializer
    parser_classes = (MultiPartParser,)
    not_allowed_actions = [
        "update",
        "partial_update",
        "destroy",
    ]
