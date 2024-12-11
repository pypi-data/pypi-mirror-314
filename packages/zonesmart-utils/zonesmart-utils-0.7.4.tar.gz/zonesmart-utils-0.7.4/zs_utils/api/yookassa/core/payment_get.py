from yookassa import Payment

from zs_utils.api.yookassa.base_action import YooKassaAction


__all__ = [
    "RemoteGetYooKassaPayment",
    "RemoteGetYooKassaPaymentList",
]


class RemoteGetYooKassaPayment(YooKassaAction):
    description = "Получение платежа в Яндекс.Кассе"
    api_method = Payment.find_one
    required_params = ["payment_id"]


class RemoteGetYooKassaPaymentList(YooKassaAction):
    description = "Получение списка платежей в Яндекс.Кассе"
    api_method = Payment.list
    required_params = ["params"]
