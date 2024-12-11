from model_utils import Choices


ShippingOptionTypeEnum = Choices(
    ("DOMESTIC", "Внутренняя доставка"),
    ("INTERNATIONAL", "Международная доставка"),
)

ShippingCostTypeEnum = Choices(
    ("FLAT_RATE", "Flat rate"),
    ("CALCULATED", "Calculated"),
    ("NOT_SPECIFIED", "Not specified"),
)

CategoryTypeEnum = Choices(
    ("MOTORS_VEHICLES", "TRANSPORT", "Автотранспорт"),
    ("ALL_EXCLUDING_MOTORS_VEHICLES", "NOT_TRANSPORT", "Всё, кроме автотранспорта"),
)

RegionTypeEnum = Choices(
    ("COUNTRY", "Страна"),
    ("COUNTRY_REGION", "Страна или регион страны"),
    ("STATE_OR_PROVINCE", "Штат или процинция"),
    ("WORLD_REGION", "Регион мира"),
    ("WORLDWIDE", "Мир"),
)

PaymentInstrumentBrandEnum = Choices(
    ("AMERICAN_EXPRESS", "American Express"),
    ("DISCOVER", "Discover"),
    ("MASTERCARD", "MasterCard"),
    ("VISA", "Visa"),
)

FullPaymentDueInEnum = Choices(
    (3, "DAYS_3", "3 дня"),
    (7, "DAYS_7", "7 дней"),
    (10, "DAYS_10", "10 дней"),
    (14, "DAYS_14", "14 дней"),
)

ReturnMethodEnum = Choices(
    ("REPLACEMENT", "Замена"),
)

ReturnShippingCostPayerEnum = Choices(
    ("BUYER", "Покупатель"),
    ("SELLER", "Продавец"),
)

RecipientAccountReferenceTypeEnum = Choices(
    ("PAYPAL_EMAIL", "PayPal email"),
)

RefundMethodEnum = Choices(
    ("MERCHANDISE_CREDIT", "Продавец предлагает возврат кредитом"),
    ("MONEY_BACK", "Полный возврат продавцом"),
)

ReturnPeriodEnum = Choices(
    (14, "14 дней"),
    (30, "30 дней"),
    (60, "60 дней"),
)
