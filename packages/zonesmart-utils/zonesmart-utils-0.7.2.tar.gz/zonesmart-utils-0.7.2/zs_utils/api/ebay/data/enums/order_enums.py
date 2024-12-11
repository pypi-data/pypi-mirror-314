from model_utils import Choices


CancelStateEnum = Choices(
    ("CANCELED", "Заказ отменён"),
    ("IN_PROGRESS", "Сделан хотя бы один запрос на отмену заказа"),
    ("NONE_REQUESTED", "Запросов на отмену заказа нет"),
)

CancelRequestStateEnum = Choices(
    ("COMPLETED", "Продавец подтвердил отмену заказа"),
    ("REJECTED", "Продавец отказал в отмене заказа"),
    ("REQUESTED", "Запрос на отмену заказа ожидает ответа от продавца"),
)

FulfillmentInstructionsType = Choices(
    ("DIGITAL", "Цифровой вид"),
    ("PREPARE_FOR_PICKUP", "Готовится к In-Store Pickup"),
    ("SELLER_DEFINED", "Определяется продавцом"),
    ("SHIP_TO", "Отправляется продавцом"),
)

LineItemFulfillmentStatusEnum = Choices(
    ("FULFILLED", "Фулфилмент завершен"),
    ("IN_PROGRESS", "Фулфилмент в процессе"),
    ("NOT_STARTED", "Фулфилмент не начат"),
)

SoldFormatEnum = Choices(
    ("AUCTION", "Аукцион"),
    ("FIXED_PRICE", "Фиксированная цена"),
    ("OTHER", "Другое"),
    ("SECOND_CHANCE_OFFER", "Second chance offer"),
)

OrderFulfillmentStatus = Choices(
    ("FULFILLED", "Фулфилмент завершен"),
    ("IN_PROGRESS", "Фулфилмент в процессе"),
    ("NOT_STARTED", "Фулфилмент не начат"),
)

OrderPaymentStatusEnum = Choices(
    ("FAILED", "Неудача"),
    ("FULLY_REFUNDED", "Деньги в полном объеме возвращены покупателю"),
    ("PAID", "Оплачено"),
    ("PARTIALLY_REFUNDED", "Деньги частично возвращены покупателю"),
    ("PENDING", "Ожидание"),
)

PaymentMethodTypeEnum = Choices(("CREDIT_CARD", "Банковская карта"), ("PAYPAL", "Paypal"))

PaymentStatusEnum = Choices(
    ("FAILED", "Неудача"),
    ("PAID", "Оплачено"),
    ("PENDING", "Ожидание"),
)

PaymentHoldStateEnum = Choices(
    ("HELD", "Заморожено"),
    ("HELD_PENDING", "Ожидается заморозка"),
    ("NOT_HELD", "Не заморожено"),
    ("RELEASE_CONFIRMED", "Подтверждено размораживание"),
    ("RELEASE_FAILED", "Неудачное размораживание"),
    ("RELEASE_PENDING", "Ожидается размораживание"),
    ("RELEASED", "Разморожено"),
)

RefundStatusEnum = Choices(
    ("FAILED", "Неудача"),
    ("PENDING", "Ожидание"),
    ("REFUNDED", "Деньги возвращены"),
)

TaxTypeEnum = Choices(
    ("GST", "Goods and Services import tax"),
    ("PROVINCE_SALES_TAX", "Provincial sales tax"),
    ("REGION", "Regional sales tax"),
    ("STATE_SALES_TAX", "State sales tax"),
    ("VAT", "Value-Added tax (VAT)"),
)

DisputeStateEnum = Choices(
    ("OPEN", "Открыто"),
    ("ACTION_NEEDED", "Требуется действие"),
    ("CLOSED", "Закрыто"),
)
