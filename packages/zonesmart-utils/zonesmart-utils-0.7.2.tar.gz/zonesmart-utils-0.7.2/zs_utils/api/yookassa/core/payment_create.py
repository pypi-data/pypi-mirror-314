from yookassa import Payment

from zs_utils.api.yookassa.base_action import YooKassaAction
from zs_utils.api.yookassa import services


__all__ = [
    "RemoteCreateYooKassaPayment",
]


class RemoteCreateYooKassaPayment(YooKassaAction):
    description = "Создание платежа в Яндекс.Кассе"
    USER_REQUIRED = True
    api_method = Payment.create
    required_params = ["params"]

    def get_params(
        self,
        amount: float,
        currency: str,
        description: str = None,
        payment_method_id: str = None,
        receipt: dict = None,
        extra_metadata: dict = None,
        return_url: str = None,
        **kwargs,
    ):
        # Описание платежа
        if description and (len(description) > 128):
            description = description[:125] + "..."

        # Метаданные
        metadata = {
            "user_id": self.user.id,
        }
        if extra_metadata:
            metadata.update(extra_metadata)
        if len(metadata.keys()) > 16:
            raise self.exception_class("Словарь 'metadata' должен содержать не более 16 ключей.")

        kwargs["params"] = {
            "amount": {"value": amount, "currency": currency},
            "description": description,
            "capture": True,
            "metadata": metadata,
            "confirmation": {
                "type": "redirect",  # или "embedded"
                "return_url": return_url,
                "enforce": False,
            },
        }

        if payment_method_id:
            # Автоплатеж
            kwargs["params"]["payment_method_id"] = payment_method_id
        else:
            # Подключение карты
            kwargs["params"].update(
                {
                    "save_payment_method": True,
                    "payment_method_data": {"type": "bank_card"},
                }
            )

        if not receipt:
            kwargs["params"]["receipt"] = services.BaseYooKassaService.get_receipt_template(
                product_description=description,
                product_price=amount,
                product_price_currency=currency,
                user=self.user,
            )

        return super().get_params(**kwargs)

    def success_callback(self, objects: dict, **kwargs) -> None:
        super().success_callback(objects, **kwargs)

        data = objects["results"]
        objects["results"] = {
            "backend": "yandex_checkout",
            "status": data["status"],
            "confirmation_token": None,
            "redirect_to_url": None,
        }
        if data.get("confirmation"):
            if data["confirmation"]["type"] == "redirect":
                objects["results"]["redirect_to_url"] = data["confirmation"]["confirmation_url"]
            elif data["confirmation"]["type"] == "embedded":
                objects["results"]["confirmation_token"] = data["confirmation"]["confirmation_token"]
