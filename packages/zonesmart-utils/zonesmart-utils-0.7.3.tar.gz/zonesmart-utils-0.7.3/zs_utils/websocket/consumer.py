from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from django.conf import settings
from django.contrib.auth import get_user_model

from zs_utils.json_utils import custom_json_dumps, custom_json_loads


class BaseChannelsConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, user_id: int):
        return get_user_model().objects.get(id=user_id)

    async def connect(self):
        if self.scope["user"]:
            self.user = self.scope["user"]
        else:
            if self.scope["token"]:
                # Соединение отвергается, если был передан невалидный токен
                if getattr(settings, "REQUIRE_JWT_FOR_WEBSOCKET", True):
                    await self.close(code=403)
                    return None
                # В режиме отладки используется тестовый пользователь
                self.user = await self.get_user(user_id=1)
            else:
                self.user = None

        if self.user:
            # Для каждого пользователя создается своя группа
            await self.add_to_group(self.get_user_group_name(user_id=self.user.id))
        elif self.scope.get("connection_id"):
            # Создание группы для анонимного подключения
            await self.add_to_group(self.get_anon_group_name(connection_id=self.scope["connection_id"]))

        self.pretenders = {}

        await self.accept()

    async def disconnect(self, code):
        for group_name in self.groups:
            await self.remove_from_group(group_name=group_name)
        await self.close(code=code)

    async def add_to_group(self, group_name: str):
        await self.channel_layer.group_add(group_name, self.channel_name)
        if group_name not in self.groups:
            self.groups.append(group_name)

    async def remove_from_group(self, group_name: str):
        await self.channel_layer.group_discard(group_name, self.channel_name)
        if group_name in self.groups:
            self.groups.remove(group_name)

    @staticmethod
    def get_user_group_name(user_id: int):
        return f"user_group_{user_id}"

    @staticmethod
    def get_anon_group_name(connection_id: str):
        return f"anon_group_{connection_id}"

    @staticmethod
    def get_user_notification_group_name(user_id: int, notification: str):
        return f"notification_{notification}_group_{user_id}"

    @classmethod
    async def encode_json(cls, content: dict):
        return custom_json_dumps(content, ensure_ascii=False)

    @classmethod
    async def decode_json(cls, text_data: str):
        return custom_json_loads(text_data)

    async def send_message(self, event: dict):
        await self.send(text_data=event["content"])

    async def send_error_message(self, message: str = None, errors: dict = None):
        await self.send_json(content={"is_success": False, "message": message, "errors": errors})

    async def send_success_message(self, message: str = None):
        await self.send_json(content={"is_success": True, "message": message})

    async def ping_action_processor(self, content: dict, **kwargs):
        await self.send_success_message(message="pong")

    async def disconnect_action_processor(self, content: dict, **kwargs):
        await self.disconnect(None)

    def subscribe_action_validator(self, content: dict, **kwargs):
        errors = {}

        for key in ["notification"]:
            if not content.get(key):
                errors[key] = "Обязательное поле."

        return errors

    async def subscribe_action_processor(self, content: dict, **kwargs):
        if self.user:
            if self.user.id in self.pretenders:
                user_id = self.pretenders[self.user.id]
            else:
                user_id = self.user.id
            group_name = self.get_user_notification_group_name(
                user_id=user_id,
                notification=content["notification"],
            )
        else:
            group_name = content["notification"]

        await self.add_to_group(group_name=group_name)
        await self.send_success_message(message="Подписка создана.")

    def unsubscribe_action_validator(self, content: dict, **kwargs):
        return self.subscribe_action_validator(content=content, **kwargs)

    async def unsubscribe_action_processor(self, content: dict, **kwargs):
        if self.user:
            if self.user.id in self.pretenders:
                user_id = self.pretenders[self.user.id]
            else:
                user_id = self.user.id
            group_name = self.get_user_notification_group_name(
                user_id=user_id,
                notification=content["notification"],
            )
        else:
            group_name = content["notification"]

        await self.remove_from_group(group_name=group_name)
        await self.send_success_message(message="Подписка удалена.")

    def pretend_on_action_validator(self, content: dict, **kwargs):
        errors = {}

        for key in ["user_id"]:
            if not content.get(key):
                errors[key] = "Обязательное поле."

        return errors

    async def pretend_on_action_processor(self, content: dict, **kwargs):
        if self.user and self.user.is_staff:
            await self.add_to_group(group_name=self.get_user_group_name(user_id=content["user_id"]))
            await self.remove_from_group(group_name=self.get_user_group_name(user_id=self.user.id))
            self.pretenders[self.user.id] = content["user_id"]
            await self.send_success_message(message="Режим получения сообщений другого пользователя включен.")

    def pretend_off_action_validator(self, content: dict, **kwargs):
        return self.pretend_on_action_validator(content=content, **kwargs)

    async def pretend_off_action_processor(self, content: dict, **kwargs):
        if self.user and self.user.is_staff:
            await self.add_to_group(group_name=self.get_user_group_name(user_id=self.user.id))
            await self.remove_from_group(group_name=self.get_user_group_name(user_id=content["user_id"]))
            if self.user.id in self.pretenders:
                self.pretenders.pop(self.user.id)
            await self.send_success_message(message="Режим получения сообщений другого пользователя отключен.")

    async def receive_json(self, content: dict, **kwargs):
        action: str = content.get("action")
        if action and getattr(settings, "WEBSOCKET_ACTIONS", None):
            if action not in settings.WEBSOCKET_ACTIONS:
                return await self.send_error_message(message="Недопустимое действие.")

            validator = getattr(self, f"{action}_action_validator", None)
            if validator:
                errors: dict = validator(content=content)
                if errors:
                    return await self.send_error_message(message="Ошибка валидации", errors=errors)

            processor = getattr(self, f"{action}_action_processor")
            if processor:
                await processor(content=content, **kwargs)
