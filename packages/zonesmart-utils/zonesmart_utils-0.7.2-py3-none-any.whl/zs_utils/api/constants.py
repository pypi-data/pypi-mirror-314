from model_utils import Choices

from django.utils.translation import gettext_lazy as _


HTTP_METHODS = Choices("GET", "POST", "DELETE", "PUT", "PATCH")

API_ERROR_REASONS = Choices(
    ("system", _("Системная ошибка")),
    ("invalid_token", _("Проблемы с валидацией токена")),
    ("data_validation", _("Проблема с валидацией данных")),
    ("unknown", _("Неизвестная ошибка")),
    ("account_deactivated", _("Аккаунт отключен")),
    ("request_limit", _("Превышен лимит запросов")),
    ("object_not_found", _("Запрашиваемый объект не найден")),
    ("object_already_exists", _("Объект уже существует")),
    ("timeout", _("Время ожидания ответа на запрос истекло")),
    ("account_token_expired", _("Требуется обновление токена аккаунта")),
)
