from rest_framework import serializers

from zs_utils.api import models


__all__ = [
    "APIRequestLogSerializer",
    "APIRequestLogListSerializer",
]


class APIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APIRequestLog
        fields = [
            "id",
            "created",
            "user",
            "is_success",
            "url",
            "method",
            "params",
            "request_headers",
            "request_body",
            "status_code",
            "response_time",
            "response_headers",
            "response_body",
        ]


class APIRequestLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APIRequestLog
        fields = [
            "id",
            "created",
            "user",
            "is_success",
            "url",
            "method",
            "status_code",
            "response_time",
        ]
