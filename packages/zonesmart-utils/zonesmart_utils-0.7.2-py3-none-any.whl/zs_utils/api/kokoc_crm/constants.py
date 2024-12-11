from model_utils import Choices


CRM_LANDING_STAGES = Choices(
    ("C22:UC_GR0G8F", "NEW", "Обработка"),
    ("C22:UC_44PJ08", "IDENTIFY_NEEDS", "Выявление потребностей"),
    ("C22:NEW", "BRIEFING", "Брифинг"),
    ("C22:PREPARATION", "PREPARING", "Подготовка стратегии / КП"),
    ("C22:PREPAYMENT_INVOIC", "PRESENTED", "Стратегия / КП - отправлено (презентовано)"),
    ("C22:EXECUTING", "NEGOTIATION", "Переговоры по КП"),
    ("C22:FINAL_INVOICE", "DECISION_MAKING", "Принятие решения"),
    ("C22:UC_QP7BZQ", "CONTRACT_SIGNING", "Подписание договора"),
    ("C22:UC_XJPR5R", "CONTRACT_SIGNED", "Договор подписан"),
    ("C22:UC_4Z82CF", "ACCOUNTING", "Передача на аккаунтинг"),
    ("C22:UC_6ZM2Q5", "PREPARE_LAUNCH", "Подготовка к запуску"),
    ("C22:UC_Z9RIPX", "LAUNCHING", "Запуск"),
    ("C22:UC_8WBK1X", "LAUNCHED", "Запуск завершён"),
    ("C22:APOLOGY", "ARCHIVED", "Архив"),
    ("C22:WON", "SUPPORT", "Поддержка клиента"),
    ("C22:LOSE", "END", "Завершение сотрудничества"),
)

CRM_OBJECTS = Choices(
    ("CONTACT", "Контакт"),
    ("DEAL", "Сделка"),
    ("STATUS", "Статус"),
)

CRM_ACTIVITY_TYPES = Choices(
    (1, "MEETING", "Встреча"),
    (2, "CALL", "Звонок"),
    (3, "TASK", "Задача"),
    (4, "MESSAGE", "Письмо"),
    (5, "ACTION", "Действие"),
)
