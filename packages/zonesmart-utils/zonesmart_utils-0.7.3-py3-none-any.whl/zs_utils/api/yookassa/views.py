from yookassa.domain.notification import WebhookNotification

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from zs_utils.api.yookassa.services import BaseYooKassaService
from zs_utils.views import CustomAPIView


__all__ = [
    "BaseYooKassaWebhookView",
]


class BaseYooKassaWebhookView(CustomAPIView):
    """
    View для получения уведомлений от YooKassa.
    """

    IP_VALIDATION = False
    YOOKASSA_WEBHOOK_IP_WHITELIST = []
    YOOKASSA_SERVICE = BaseYooKassaService

    @staticmethod
    def validation(event_type: str, event_data: dict, metadata: dict):
        pass

    @property
    def request_ip(self) -> str:
        return None

    def get_user(self, user_id: str = None, payment_id: str = None):
        raise NotImplementedError("Необходимо определить метод получения пользователя.")

    def post(self, request: Request, *args, **kwargs):
        # IP validation
        if self.IP_VALIDATION and self.request_ip not in self.YOOKASSA_WEBHOOK_IP_WHITELIST:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Валидация ключей
        for key in ["event", "object"]:
            if not request.data.get(key):
                raise ValidationError({key: "Это поле обязательно."})

        # Разбор данных
        notification = WebhookNotification(request.data)
        event_type = notification.event
        event_data = dict(notification.object)
        metadata = event_data.get("metadata", {})

        self.validation(event_type=event_type, event_data=event_data, metadata=metadata)

        # Определяем пользователя
        user_id = metadata.get("user_id")
        payment_id = request.data["object"].get("payment_id", event_data.get("id"))
        event_data["payment_id"] = payment_id
        user = self.get_user(user_id=user_id, payment_id=payment_id)
        if not user:
            return Response({"detail": "Не удалось определить пользователя"}, status.HTTP_400_BAD_REQUEST)

        # Обработка данных
        self.YOOKASSA_SERVICE.process_webhook(user=user, event_type=event_type, event_data=event_data)

        return Response(status=status.HTTP_200_OK)
