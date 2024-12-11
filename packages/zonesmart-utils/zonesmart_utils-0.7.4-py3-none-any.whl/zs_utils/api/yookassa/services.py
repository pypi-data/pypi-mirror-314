from zs_utils.api.yookassa import constants, core
from zs_utils.data.enums import CURRENCIES
from zs_utils.exceptions import CustomException
from zs_utils.user.models import AbstractZonesmartUser


__all__ = [
    "YooKassaException",
    "BaseYooKassaService",
]


class YooKassaException(CustomException):
    pass


class BaseYooKassaService:
    YOOKASSA_CREDENTIALS = None
    YOOKASSA_TEST_MODE = None

    @staticmethod
    def validate_amount(amount: float) -> None:
        """
        Валидация суммы amount (должна быть положительной)
        """
        if amount <= 0:
            raise YooKassaException("Значение 'amount' должно быть положительным.")

    @classmethod
    def convert_currency(cls, amount: float, from_currency: str) -> float:
        # TODO?
        # Always into CURRENCIES.RUB
        return amount

    @classmethod
    def get_receipt_template(
        cls,
        product_description: str,
        product_price: float,
        product_price_currency: CURRENCIES,
        user: AbstractZonesmartUser = None,
        inn: str = None,
        email: str = None,
        phone: str = None,
    ) -> dict:
        if user:
            email = user.email
            phone = getattr(user, "phone", None)
            organization = getattr(user, "user_organization", None)
            if organization:
                inn = organization.itn
            else:
                inn = None

        if product_price_currency != CURRENCIES.RUB:
            product_price = cls.convert_currency(amount=product_price, from_currency=product_price_currency)

        data = {
            "customer": {
                "inn": inn,
                "email": email,
                "phone": phone,
            },
            "items": [
                {
                    "description": product_description,
                    "quantity": 1,
                    "amount": {"value": product_price, "currency": "RUB"},
                    "vat_code": constants.YOOKASSA_VAT_CODES.n1,
                    "payment_subject": constants.YOOKASSA_PAYMENT_SUBJECTS.service,
                    "payment_mode": constants.YOOKASSA_PAYMENT_MODES.full_prepayment,
                    "agent_type": constants.YOOKASSA_AGENT_TYPES.payment_agent,
                },
            ],
            "tax_system_code": constants.YOOKASSA_TAX_SYSTEM_CODES.n3,
        }
        return data

    @classmethod
    def remote_setup_card(cls, user: AbstractZonesmartUser, return_url: str, extra_metadata: dict = None) -> tuple:
        """
        Создание платежа для подключения карты
        """
        call_params = {
            "user": user,
            "amount": 1,
            "description": "Подключение банковской карты.",
            "purpose": constants.YOOKASSA_PURPOSE.CARD_SETUP,
            "return_url": return_url,
            "extra_metadata": extra_metadata,
        }
        return cls.remote_create_payment(**call_params)

    @classmethod
    def remote_create_payment(
        cls,
        user: AbstractZonesmartUser,
        amount: float,
        return_url: str,
        purpose: str,
        description: str,
        payment_method_id: str = None,
        extra_metadata: dict = None,
    ) -> tuple:
        """
        Создание платежа через YooKassa
        """

        cls.validate_amount(amount)

        if not extra_metadata:
            extra_metadata = {}
        extra_metadata["purpose"] = purpose

        call_params = {
            "payment_method_id": payment_method_id,
            "amount": amount,
            "currency": "RUB",
            "description": description,
            "extra_metadata": extra_metadata,
            "return_url": return_url,
        }
        return core.RemoteCreateYooKassaPayment(
            credentials=cls.YOOKASSA_CREDENTIALS, test_mode=cls.YOOKASSA_TEST_MODE, user=user, propagate_exception=True
        )(**call_params)

    @classmethod
    def remote_create_refund(cls, user: AbstractZonesmartUser, payment_id: str, amount: float) -> tuple:
        """
        Запрос на возврат средств через YooKassa
        """

        cls.validate_amount(amount)

        return core.RemoteCreateYooKassaRefund(
            credentials=cls.YOOKASSA_CREDENTIALS, test_mode=cls.YOOKASSA_TEST_MODE, user=user, propagate_exception=True
        )(payment_id=payment_id, amount=amount)

    # Process webhook events
    @classmethod
    def process_webhook(cls, user: AbstractZonesmartUser, event_type: str, event_data: dict) -> None:
        """
        Обработка вебхук-уведомления от YooKassa
        """
        is_card_setup = False
        if event_data.get("metadata"):
            is_card_setup = event_data["metadata"].get("purpose") == constants.YOOKASSA_PURPOSE.CARD_SETUP

        if is_card_setup and event_type == "payment.canceled":
            action = cls.card_setup_canceled
        elif is_card_setup and event_type == "payment.succeeded":
            action = cls.card_setup_succeeded
        elif event_type == "payment.canceled":
            action = cls.payment_canceled
        elif event_type == "payment.succeeded":
            action = cls.payment_succeeded
        elif event_type == "refund.succeeded":
            action = cls.payment_refunded
        else:
            raise YooKassaException("Для данного события обработчик не найден.")

        action(user=user, raw_data=event_data)

    @classmethod
    def card_setup_succeeded(cls, user: AbstractZonesmartUser, raw_data: dict):
        return cls.create_or_update_payment_instance(user=user, raw_data=raw_data)

    @classmethod
    def payment_canceled(cls, user: AbstractZonesmartUser, raw_data: dict):
        return cls.create_or_update_payment_instance(user=user, raw_data=raw_data)

    @classmethod
    def payment_succeeded(cls, user: AbstractZonesmartUser, raw_data: dict):
        return cls.create_or_update_payment_instance(user=user, raw_data=raw_data)

    @classmethod
    def card_setup_canceled(cls, user: AbstractZonesmartUser, raw_data: dict):
        raise NotImplementedError("Необходимо определить метод обработки неудачной попытки подключить карту.")

    @classmethod
    def create_or_update_card_instance(cls, user: AbstractZonesmartUser, raw_data: dict):
        raise NotImplementedError("Необходимо определить метод создания и обновления банковской карты.")

    @classmethod
    def create_or_update_payment_instance(cls, user: AbstractZonesmartUser, raw_data: dict):
        raise NotImplementedError("Необходимо определить метод создания и обновления объекта платежа.")

    @classmethod
    def payment_refunded(cls, user: AbstractZonesmartUser, raw_data: dict):
        raise NotImplementedError("Необходимо определить метод обработки удачного возврата платежа.")
