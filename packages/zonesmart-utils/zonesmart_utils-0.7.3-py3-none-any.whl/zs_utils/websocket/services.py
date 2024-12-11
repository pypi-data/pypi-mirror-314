from channels import layers
from asgiref.sync import async_to_sync

from django.conf import settings

from zs_utils.json_utils import custom_json_dumps
from zs_utils.websocket import consumer


__all__ = [
    "WebsocketService",
]


class WebsocketService:
    """
    Сервис для отправки сообщений в вебсокет.
    """

    @classmethod
    def send_data_to_consumer_group(cls, *, group_name: str, content: dict) -> None:
        """
        Отправить данные content в websocket
        """
        layer = layers.get_channel_layer()
        async_to_sync(layer.group_send)(
            group_name,
            {
                "type": "send.message",
                "content": custom_json_dumps(content, ensure_ascii=True),
            },
        )

    @classmethod
    def send_data_to_user(cls, *, user_id: int, content: dict) -> None:
        """
        Отправить сообщение пользователю.
        """

        group_name = consumer.BaseChannelsConsumer.get_user_group_name(user_id=user_id)
        cls.send_data_to_consumer_group(group_name=group_name, content=content)

    @classmethod
    def send_page_refresh_required_message(cls, user_id: int, page_path: str) -> None:
        """
        Отправление пользователю сообщения о необходимости обновить страницу.
        """

        group_name = consumer.BaseChannelsConsumer.get_user_group_name(user_id=user_id)
        cls.send_data_to_consumer_group(
            group_name=group_name,
            content={"event_type": "page_refresh_required", "page": page_path},
        )

    @classmethod
    def send_data_to_notification_group(cls, *, user_id: int, notification: str, data: dict) -> None:
        """
        Отправить сообщение пользователю, если он подписан на группу событий.
        """

        if notification not in getattr(settings, "WEBSOCKET_NOTIFICATION_GROUPS", []):
            raise ValueError("Недопустимая группа событий.")

        group_name = consumer.BaseChannelsConsumer.get_user_notification_group_name(
            user_id=user_id,
            notification=notification,
        )
        cls.send_data_to_consumer_group(group_name=group_name, content={"notification": notification, "data": data})
