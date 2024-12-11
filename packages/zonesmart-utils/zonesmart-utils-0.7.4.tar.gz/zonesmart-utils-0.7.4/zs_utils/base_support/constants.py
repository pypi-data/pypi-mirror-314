from model_utils import Choices

from django.conf import settings
from django.utils.translation import gettext_lazy as _


SUPPORT_TICKET_QUESTION_TYPES = getattr(
    settings,
    "SUPPORT_TICKET_QUESTION_TYPES",
    Choices(
        ("BASIC", _("Общий вопрос")),
        ("INTERFACE", _("Интерфейс")),
        ("TECHNICAL", _("Технический")),
        ("BILLING", _("Счет")),
    )
)

SUPPORT_TICKET_STATUSES = Choices(
    ("PENDING", _("Ожидает рассмотрения")),
    ("OPEN", _("Открыто")),
    ("CLOSED_BY_USER", _("Закрыто пользователем")),
    ("CLOSED_BY_MANAGER", _("Закрыто менеджером")),
    ("CLOSED_AUTO", _("Закрыто из-за отсутствия активности")),
)

SUPPORT_TICKET_ACTIVE_STATUSES = SUPPORT_TICKET_STATUSES.subset("PENDING", "OPEN")

SUPPORT_TICKET_ACTIVE_STATUSES_LIST = [item[0] for item in SUPPORT_TICKET_ACTIVE_STATUSES]

SUPPORT_TICKET_CLIENT_STATUSES = Choices(
    ("PENDING", _("В работе")),
    ("RESPONDED", _("Получен ответ")),
    ("CLOSED", _("Закрыто")),
)

SUPPORT_TICKET_MESSAGES = Choices(
    ("OPEN", _("Заявка взята в обработку оператором.")),
    ("CLOSED_AUTO", _("Заявка автоматически закрыта после длительного отсутствия активности.")),
    ("CLOSED_BY_USER", _("Заявка закрыта пользователем.")),
    ("CLOSED_BY_MANAGER", _("Заявка закрыта оператором.")),
    ("REOPEN", _("Заявка повторно открыта.")),
)

SUPPORT_TICKET_MESSAGE_SIGNATURE = getattr(settings, "SUPPORT_TICKET_MESSAGE_SIGNATURE", "")

TICKET_WITH_MESSAGES = getattr(settings, "TICKET_WITH_MESSAGES", False)
CREATE_SYSTEM_MESSAGE = getattr(settings, "CREATE_SYSTEM_MESSAGE", False)
SEND_EMAIL_BY_SUBSCRIPTION = getattr(settings, "SEND_EMAIL_BY_SUBSCRIPTION", False)
EVENT_TYPE_SUPPORT_TICKET_MESSAGE_CREATED = getattr(settings, "EVENT_TYPE_SUPPORT_TICKET_MESSAGE_CREATED", "")
SUPPORT_EMAIL_LIST = getattr(settings, "SUPPORT_EMAIL_LIST", [])
EMAIL_DUMMY_IMAGE_URL = getattr(settings, "EMAIL_DUMMY_IMAGE_URL", "")

MAX_OPEN_TICKET = getattr(settings, "MAX_OPEN_TICKET", 10)
MAX_TEXT_LENGTH = getattr(settings, "MAX_TEXT_LENGTH", 1500)
MAX_TICKET_MESSAGE_FILES = getattr(settings, "MAX_TICKET_MESSAGE_FILES", 100)
AUTO_CLOSE_TICKET_AFTER = getattr(settings, "AUTO_CLOSE_TICKET_AFTER", 2)
