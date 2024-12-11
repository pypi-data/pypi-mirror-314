from model_utils import Choices

from django.utils.translation import gettext_lazy as _


YOOKASSA_PAYMENT_STATUSES = Choices(
    ("pending", _("Ожидание подтверждения")),
    ("succeeded", _("Успешно выполнено")),
    ("canceled", _("Отменено")),
    ("waiting_for_capture", _("Ожидание списания")),
)

YOOKASSA_PAYMENT_CANCELLATION_PARTIES = Choices(
    ("yandex_checkout", _("Яндекс.Касса")),
    ("payment_network", _("Внешние участники платежного процесса")),
    ("merchant", _("Продавец товаров и услуг")),
)

YOOKASSA_CANCELLATION_REASONS = Choices(
    ("3d_secure_failed", _("Не пройдена аутентификация по 3-D Secure")),
    ("call_issuer", _("Оплата данным платежным средством отклонена по неизвестным причинам")),
    ("canceled_by_merchant", _("Платеж отменен по API при оплате в две стадии")),
    ("card_expired", _("Истек срок действия банковской карты")),
    ("country_forbidden", _("Нельзя заплатить банковской картой, выпущенной в этой стране")),
    ("expired_on_capture", _("Истек срок списания оплаты у двухстадийного платежа")),
    (
        "expired_on_confirmation",
        _("Истек срок оплаты: пользователь не подтвердил платеж за время, отведенное на оплату выбранным способом"),
    ),
    ("fraud_suspected", _("Платеж заблокирован из-за подозрения в мошенничестве")),
    ("general_decline", _("Причина не детализирована")),
    ("identification_required", _("Превышены ограничения на платежи для кошелька в Яндекс.Деньгах")),
    ("insufficient_funds", _("Не хватает денег для оплаты")),
    (
        "internal_timeout",
        _("Технические неполадки на стороне Яндекс.Кассы: не удалось обработать запрос в течение 30 секунд"),
    ),
    ("invalid_card_number", _("Неправильно указан номер карты")),
    ("invalid_csc", _("Неправильно указан код CVV2 (CVC2, CID)")),
    ("issuer_unavailable", _("Организация, выпустившая платежное средство, недоступна")),
    ("payment_method_limit_exceeded", _("Исчерпан лимит платежей для данного платежного средства или магазина")),
    ("payment_method_restricted", _("Запрещены операции данным платежным средством")),
    ("permission_revoked", _("Нельзя провести безакцептное списание: пользователь отозвал разрешение на автоплатежи")),
)

YOOKASSA_RECEIPT_REGISTRATION_STATUSES = Choices(
    ("pending", _("Ожидание")),
    ("succeeded", _("Успешно выполнено")),
    ("canceled", _("Отменено")),
)

YOOKASSA_RECEIPT_TYPES = Choices("payment", "refund")

YOOKASSA_TAX_SYSTEM_CODES = Choices(
    (1, "n1", "Общая система налогообложения"),
    (2, "n2", "Упрощенная (УСН, доходы)"),
    (3, "n3", "Упрощенная (УСН, доходы минус расходы)"),
    (4, "n4", "Единый налог на вмененный доход (ЕНВД)"),
    (5, "n5", "Единый сельскохозяйственный налог (ЕСН)"),
    (6, "n6", "Патентная система налогообложения"),
)

YOOKASSA_VAT_CODES = Choices(
    (1, "n1", "Без НДС"),
    (2, "n2", "НДС по ставке 0%"),
    (3, "n3", "НДС по ставке 10%"),
    (4, "n4", "НДС чека по ставке 20%"),
    (5, "n5", "НДС чека по расчетной ставке 10/110"),
    (6, "n6", "НДС чека по расчетной ставке 20/120"),
)

YOOKASSA_PAYMENT_SUBJECTS = Choices(
    ("service", "Услуга"),
)

YOOKASSA_PAYMENT_MODES = Choices(
    ("full_prepayment", "Полная предоплата"),
    ("partial_prepayment", "Частичная предоплата"),
    ("advance", "Аванс"),
    ("full_payment", "Полный расчет"),
    ("partial_payment", "Частичный расчет и кредит"),
    ("credit", "Кредит"),
    ("credit_payment", "Выплата по кредиту"),
)

YOOKASSA_SETTLEMENT_TYPES = Choices(
    ("cashless", "Безналичный расчет"),
    ("prepayment", "Предоплата (аванс)"),
    ("postpayment", "Постоплата (кредит)"),
    ("consideration", "Встречное предоставление"),
)

YOOKASSA_AGENT_TYPES = Choices(
    ("banking_payment_agent", "Банковский платежный агент"),
    ("banking_payment_subagent", "Банковский платежный субагент"),
    ("payment_agent", "Платежный агент"),
    ("payment_subagent", "Платежный субагент"),
    ("attorney", "Поверенный"),
    ("commissioner", "Комиссионер"),
    ("agent", "Агент"),
)

YOOKASSA_PURPOSE = Choices(
    ("CARD_SETUP", "Подключение карты"),
)
