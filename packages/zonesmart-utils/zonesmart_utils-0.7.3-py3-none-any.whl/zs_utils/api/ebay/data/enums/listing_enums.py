from model_utils import Choices


AvailabilityTypeEnum = Choices(
    ("IN_STOCK", "В наличии"),
    ("OUT_OF_STOCK", "Нет в наличии"),
    ("SHIP_TO_STORE", "Ожидается пополнение"),
)

PackageTypeEnum = Choices(
    ("LETTER", "Бумага"),
    ("BULKY_GOODS", "Bulky good"),
    ("CARAVAN", "Caravan"),
    ("CARS", "Автомобиль"),
    ("EUROPALLET", "Euro pallet"),
    ("EXPANDABLE_TOUGH_BAGS", "Expandable tough bag"),
    ("EXTRA_LARGE_PACK", "Extra large pack"),
    ("FURNITURE", "Мебель"),
    ("INDUSTRY_VEHICLES", "Industry vehicle"),
    ("LARGE_CANADA_POSTBOX", "A Canada Post large box"),
    ("LARGE_CANADA_POST_BUBBLE_MAILER", "Canada Post large bubble mailer"),
    ("LARGE_ENVELOPE", "Большой конверт"),
    ("MAILING_BOX", "Mailing box"),
    ("MEDIUM_CANADA_POST_BOX", "Medium Canada Post box"),
    ("MEDIUM_CANADA_POST_BUBBLE_MAILER", "Medium Canada Post bubble mailer"),
    ("MOTORBIKES", "Мотоцикл"),
    ("ONE_WAY_PALLET", "One-way pallet"),
    ("PACKAGE_THICK_ENVELOPE", "Толстый конверт"),
    ("PADDED_BAGS", "Padded bag"),
    ("PARCEL_OR_PADDED_ENVELOPE", "Посылка или мягкий конверт"),
    ("ROLL", "Roll"),
    ("SMALL_CANADA_POST_BOX", "Small Canada Post box"),
    ("SMALL_CANADA_POST_BUBBLE_MAILER", "Small Canada Post bubble mailer"),
    ("TOUGH_BAGS", "Tough bag"),
    ("UPS_LETTER", "Письмо UPS"),
    ("USPS_FLAT_RATE_ENVELOPE", "USPS flat-rate envelope"),
    ("USPS_LARGE_PACK", "USPS large pack"),
    ("VERY_LARGE_PACK", "USPS very large pack"),
    ("WINE_PAK", "Wine pak"),
)

ShippingServiceTypeEnum = Choices(
    ("DOMESTIC", "Внутренняя доставка"),
    ("INTERNATIONAL", "Международная доставка"),
)

SoldOnEnum = Choices(
    ("ON_EBAY", "Товар продавался по указанной цене на сайте eBay"),
    ("OFF_EBAY", "Товар продавался по указанной цене на сторонних сайтах"),
    (
        "ON_AND_OFF_EBAY",
        "Товар продавался по указанной цене как на сайте eBay, так и на сторонних сайтах",
    ),
)

MinimumAdvertisedPriceHandlingEnum = Choices(
    ("NONE", "Не использовать"),
    ("PRE_CHECKOUT", "До оформления заказа"),
    ("DURING_CHECKOUT", "После оформления заказа"),
)

# https://developer.ebay.com/api-docs/sell/inventory/types/slr:ListingStatusEnum
ListingStatusEnum = Choices(
    ("ACTIVE", "ACTIVE"),
    ("OUT_OF_STOCK", "OUT_OF_STOCK"),
    ("INACTIVE", "INACTIVE"),
    ("ENDED", "ENDED"),
    ("EBAY_ENDED", "EBAY_ENDED"),
    ("NOT_LISTED", "NOT_LISTED"),
)
