import logging
import os

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import QueryDict
from django.utils.translation import gettext as _
from django.contrib.gis.geoip2 import GeoIP2

from zs_utils.data.enums import COUNTRIES
from zs_utils.permissions import UserHasAccess
from zs_utils.views import mixins
from zs_utils.captcha import validate_captcha


__all__ = [
    "CustomAPIView",
    "CustomModelViewSet",
    "get_client_ip",
    "is_russian_ip",
    "get_country_by_ip",
]


logger = logging.getLogger()


def get_client_ip(request):
    """
    Получение IP адреса клиента
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def is_russian_ip(ip_address: str):
    return get_country_by_ip(ip_address=ip_address) == COUNTRIES.RU


def get_country_by_ip(ip_address: str) -> COUNTRIES:
    geo = GeoIP2(path=os.path.dirname(os.path.realpath(__file__)))
    country_data = geo.country(ip_address)
    return country_data["country_code"]


class CustomAPIView(mixins.DataValidationViewMixin, mixins.ResponseShortcutsViewMixin, APIView):
    permission_classes = [AllowAny]


class CustomModelViewSet(
    mixins.AdminModeViewMixin,
    mixins.DataValidationViewMixin,
    mixins.ResponseShortcutsViewMixin,
    ModelViewSet,
):
    lookup_field = "id"
    default_permission = UserHasAccess
    ignore_has_access = False
    allow_partial_update = True

    not_allowed_actions = []
    extra_allowed_actions = []

    required_filters = []
    actions_for_filterset_class = [
        "retrieve",
    ]

    serializer_classes = {}
    serializer_class = None

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        if (self.action in self.not_allowed_actions) and (self.action not in self.extra_allowed_actions):
            return self.http_method_not_allowed(request, *args, **kwargs)

        return request

    def get_permissions(self):
        """
        Проверка прав пользователя
        """
        return super().get_permissions() + [self.default_permission()]

    def get_exception_handler_context(self) -> dict:
        """
        Формирование данных для контекста ошибки.
        """

        context = super().get_exception_handler_context()

        try:
            context["user"] = self.get_user()
        except Exception as error:
            logger.error(msg=str(error))

        return context

    def get_serializer_class(self):
        """
        Получение класса сериализатора
        """

        # Маппинг между экшенами и сериализаторами
        return self.serializer_classes.get(self.action, self.serializer_classes.get("default", self.serializer_class))

    def get_serializer(self, *args, **kwargs):
        """
        Получение сериализатора
        """
        # Если данные передаются на прямую из request.data, то это объект QueryDict, он не изменяем, нужно копировать
        if ("data" in kwargs) and isinstance(kwargs["data"], QueryDict):
            kwargs["data"] = kwargs["data"].copy()

        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        return serializer_class(*args, **kwargs)

    def validate_filters(self) -> None:
        """
        Валидация фильтров запросов
        """
        for key in self.required_filters:
            if not self.request.GET.get(key):
                raise ValidationError({key: _("Обязательный фильтр")})

        if self.request.GET.get("limit") and (int(self.request.GET["limit"]) > settings.DRF_LIMIT_FILTER_MAX_VALUE):
            raise ValidationError(
                {"limit": _("Максимальное значение: {max_value}").format(max_value=settings.DRF_LIMIT_FILTER_MAX_VALUE)}
            )

    def get_queryset_filter_kwargs(self) -> dict:
        return {}

    def limit_queryset(self, queryset):
        """
        Валидация фильтров при получении списка объектов
        """
        if self.action == "list":
            self.validate_filters()

        return queryset.filter(**self.get_queryset_filter_kwargs())

    def get_queryset(self, manager: str = "objects"):
        """
        Получение Queryset
        """
        if getattr(self, "filterset_class", None) and hasattr(self.filterset_class, "Meta"):
            model = self.filterset_class.Meta.model
        else:
            model = self.get_serializer_class().Meta.model

        queryset = getattr(model, manager).all()

        if (self.actions_for_filterset_class == "__all__") or (self.action in self.actions_for_filterset_class):
            queryset = self.filter_queryset(queryset=queryset)

        if not self.no_limit:
            # Обязательная фильтрация результатов для рядовых пользователей
            queryset = self.limit_queryset(queryset=queryset)

        return queryset

    @action(detail=False, methods=["GET"])
    def count(self, request, *args, **kwargs):
        """
        Получение кол-во объектов
        """
        return self.build_response(data={"count": self.filter_queryset(self.get_queryset()).count()})

    def partial_update(self, request, *args, **kwargs):
        """
        Запрет на частичное обновление
        """
        if not getattr(self, "allow_partial_update", True):
            raise MethodNotAllowed(self)
        return super().partial_update(request, *args, **kwargs)

    def get_client_ip(self):
        """
        Получение IP адреса клиента
        """

        return get_client_ip(request=self.request)

    def validate_captcha(self, token: str, ip: str = None) -> None:
        if not ip:
            ip = self.get_client_ip()

        validate_captcha(token=token, ip=ip)
