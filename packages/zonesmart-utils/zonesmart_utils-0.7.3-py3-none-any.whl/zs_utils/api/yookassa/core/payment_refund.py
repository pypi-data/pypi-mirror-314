from yookassa import Refund

from .payment_get import RemoteGetYooKassaPayment
from zs_utils.api.yookassa.base_action import YooKassaAction
from zs_utils.api.yookassa import services


__all__ = [
    "RemoteGetYooKassaRefund",
    "RemoteGetYooKassaRefundList",
    "RemoteCreateYooKassaRefund",
]


class RemoteGetYooKassaRefund(YooKassaAction):
    description = "Получение возврата платежа в Яндекс.Кассе"
    api_method = Refund.find_one
    required_params = ["refund_id"]


class RemoteGetYooKassaRefundList(YooKassaAction):
    description = "Получение всех возвратов платежей в Яндекс.Кассе"
    api_method = Refund.list
    required_params = ["params"]


class RemoteCreateYooKassaRefund(YooKassaAction):
    description = "Создание возврата платежа в Яндекс.Кассе"
    USER_REQUIRED = True
    api_method = Refund.create
    required_params = ["params"]

    def set_used_actions(self) -> None:
        self.remote_get_payment = self.set_used_action(action_class=RemoteGetYooKassaPayment)

    def get_params(
        self,
        payment_id: str,
        amount: float = None,
        description: str = None,
        receipt: dict = None,
        extra_metadata: dict = None,
        **kwargs,
    ):
        # Получение информации из сервиса
        payment_data = self.remote_get_payment(payment_id=payment_id)[2]["results"]

        currency = payment_data["amount"]["currency"]
        if not description:
            description = payment_data["description"]
        if not amount:
            amount = payment_data["amount"]["value"]

        if not receipt:
            receipt = services.BaseYooKassaService.get_receipt_template(
                product_description=description,
                product_price=amount,
                product_price_currency=currency,
                user=self.user,
            )

        kwargs["params"] = {
            "amount": {"value": amount, "currency": currency},
            "payment_id": payment_id,
            "receipt": receipt,
            "metadata": extra_metadata,
        }

        return super().get_params(**kwargs)
