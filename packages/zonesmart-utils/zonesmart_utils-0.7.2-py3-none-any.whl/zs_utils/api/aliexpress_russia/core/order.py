from zs_utils.api.aliexpress_russia.base_api import AliexpressRussiaAPI


class GetAliexpressOrderListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-get-orders-list
    """

    resource_method = "/seller-api/v1/order/get-order-list"
    required_params = ["page_size", "page"]
    allowed_params = [
        "date_start",
        "date_end",
        "order_statuses",
        "payment_statuses",
        "delivery_statuses",
        "antifraud_statuses",
        "order_ids",
        "sorting_order",
        "sorting_field",
        "tracking_numbers",
        "update_at_from",
        "update_at_to",
        "shipping_day_from",
        "shipping_day_to",
        "trade_order_info",
    ]


class SetAliexpressOrderInTransitAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/change-status#heading-prisvoit-zakazu-status-otpravlen
    """

    resource_method = "/api/v1/offline-ship/to-in-transit"
    required_params = [
        "trade_order_id",
        "tracking_number",
        "provider_name",
    ]
    allowed_params = [
        "tracking_url",
        "support_phone_number",
    ]


class SetAliexpressOrderReadyForPickupAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/change-status#heading-prisvoit-zakazu-status-ozhidaet-polucheniya
    """

    resource_method = "/api/v1/offline-ship/to-ready-for-pickup"
    required_params = ["trade_order_id"]


class SetAliexpressOrderDeliveredAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/change-status#heading-prisvoit-zakazu-status-dostavlen
    """

    resource_method = "/api/v1/offline-ship/to-delivered"
    required_params = ["trade_order_id"]
