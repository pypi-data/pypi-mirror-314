from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers


__all__ = [
    "UserLightSerializer",
]

User = get_user_model()


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = getattr(
            settings,
            "USER_LIGHT_SERIALIZER_FIELDS",
            [
                "id",
                "email",
                "is_staff",
                "first_name",
                "last_name",
                "full_name",
            ]
        )
