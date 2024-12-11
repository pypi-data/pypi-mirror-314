import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from zs_utils.base_support import constants, models
from zs_utils.user.serializers import UserLightSerializer


__all__ = [
    "CommonSupportTicketSerializer",
    "CommonCreateSupportTicketSerializer",
    "CommonSupportTicketMessageSerializer",
    "CommonCreateSupportTicketMessageSerializer",
    "CommonSupportTicketMessageFileSerializer",
]


class CommonSupportTicketSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    manager = UserLightSerializer(read_only=True)

    class Meta:
        model = models.SupportTicket
        fields = [
            "id",
            "number",
            "created",
            "user",
            "manager",
            "status",
            "question_type",
            "subject",
            "unread_messages",
            "client_status"
        ]


class CommonSupportTicketMessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupportTicketMessageFile
        fields = [
            "id",
            "ticket_message",
            "file",
            "user",
            "name",
        ]


class CommonSupportTicketMessageSerializer(serializers.ModelSerializer):
    sender = UserLightSerializer(read_only=True)
    files = CommonSupportTicketMessageFileSerializer(many=True)

    class Meta:
        model = models.SupportTicketMessage
        fields = [
            "id",
            "created",
            "ticket",
            "sender",
            "text",
            "files",
            "is_system",
            "is_viewed",
        ]


class CommonSupportTicketWithMessagesSerializer(CommonSupportTicketSerializer):
    messages = CommonSupportTicketMessageSerializer(many=True, read_only=True)

    class Meta(CommonSupportTicketSerializer.Meta):
        model = models.SupportTicket
        fields = CommonSupportTicketSerializer.Meta.fields + ["messages"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["user"] = UserLightSerializer(instance.user).data
        data["user"]["phone"] = instance.user.phone

        return data


class CommonCreateSupportTicketMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_null=True)
    files = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=models.SupportTicketMessageFile.objects.all()),
        required=False,
        max_length=constants.MAX_TICKET_MESSAGE_FILES,
    )

    def to_internal_value(self, data):
        files = data.get("files")
        file_uuids = []
        if files:
            for file in files:
                if isinstance(file, models.SupportTicketMessageFile):
                    file_uuids.append(file.id)
                else:
                    try:
                        file_uuids.append(uuid.UUID(str(file)))
                    except ValueError:
                        raise ValidationError(f"Неверный формат UUID. {file}")
        if file_uuids:
            data["files"] = file_uuids
        data = super().to_internal_value(data)

        if not (data.get("text") or data.get("files")):
            raise ValidationError({"text": "Обязательное поле, если не задано поле 'files'."})

        return data


class CommonCreateSupportTicketSerializer(serializers.ModelSerializer):
    message = CommonCreateSupportTicketMessageSerializer(required=False)

    class Meta:
        model = models.SupportTicket
        fields = [
            "question_type",
            "subject",
            "message",
        ]

    def to_internal_value(self, data):
        if "message" in data and data["message"] is not None:
            message_serializer = self.fields["message"]
            message_internal = message_serializer.to_internal_value(data["message"])
            data["message"] = message_internal
        elif "message" in data and data["message"] is None:
            del data["message"]

        return super().to_internal_value(data)
