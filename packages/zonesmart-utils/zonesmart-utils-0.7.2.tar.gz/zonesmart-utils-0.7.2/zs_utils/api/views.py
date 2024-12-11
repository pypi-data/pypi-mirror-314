from zs_utils.views import CustomModelViewSet
from zs_utils.api import serializers, filters


__all__ = [
    "APIRequestLogView",
]


class APIRequestLogView(CustomModelViewSet):
    """
    View для просмотра данных модели APIRequestLog
    """

    serializer_classes = {
        "default": serializers.APIRequestLogSerializer,
        "list": serializers.APIRequestLogListSerializer,
    }
    filterset_class = filters.APIRequestLogFilter
