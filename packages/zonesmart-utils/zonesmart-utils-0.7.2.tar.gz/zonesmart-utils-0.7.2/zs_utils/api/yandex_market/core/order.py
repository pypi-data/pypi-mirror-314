from zs_utils.api.yandex_market.base_api import YandexMarketAPI


class SendYandexMarketShipmentBoxesAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-marketplace-cd/doc/dg/reference/put-campaigns-id-orders-id-delivery-shipments-id-boxes.html
    """

    description = "Передача информации о грузовых местах в заказе Yandex Market"
    http_method = "PUT"
    resource_method = "campaigns/{shop_id}/orders/{order_id}/delivery/shipments/{shipment_id}/boxes"
    required_params = [
        "shop_id",
        "order_id",
        "shipment_id",
        "boxes",
    ]


class GetYandexMarketTransferActAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-marketplace-cd/doc/dg/reference/get-campaigns-id-shipments-reception-transfer-act.html
    """

    description = "Получение акта приема-передачи сегодняшних заказов Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/shipments/reception-transfer-act"
    required_params = [
        "shop_id",
    ]


class GetYandexMarketRegions(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-regions.html
    """

    description = "Поиск региона"
    http_method = "GET"
    resource_method = "regions"
    required_params = [
        "name",
    ]


class GetYandexMarketDeliveryServicesAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-delivery-services.html
    """

    description = "Получение служб доставки Yandex Market"
    http_method = "GET"
    resource_method = "delivery/services"


class GetYandexMarketOrderListAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id-orders.html
    """

    description = "Получение списка заказов Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/orders"
    allowed_params = [
        "shop_id",
        "fromDate",
        "toDate",
        "status",
        "substatus",
        "page",
        "pageSize",
    ]


class GetYandexMarketOrderAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/get-campaigns-id-orders-id.html
    """

    description = "Получения заказа Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/orders/{order_id}"
    required_params = [
        "shop_id",
        "order_id",
    ]


class ChangeYandexMarketOrderStatusAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/put-campaigns-id-orders-id-status.html
    """

    description = "Изменение статуса заказа Yandex Market"
    http_method = "PUT"
    resource_method = "campaigns/{shop_id}/orders/{order_id}/status"
    required_params = [
        "shop_id",
        "order_id",
        "order",
    ]


class ChangeYandexMarketDigitalOrderStatusAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/troubleshooting/general.html#general__digital
    """

    description = "Изменение статуса цифрового заказа Yandex Market"
    http_method = "POST"
    resource_method = "campaigns/{shop_id}/orders/{order_id}/deliverDigitalGoods"
    required_params = [
        "shop_id",
        "order_id",
    ]


class GetYandexMarketShipmentLabelsAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-marketplace-cd/doc/dg/reference/get-campaigns-id-orders-id-delivery-labels.html
    """

    description = "Получение ярлыков‑наклеек на все грузовые места в заказе Yandex Market"
    http_method = "GET"
    resource_method = "campaigns/{shop_id}/orders/{order_id}/delivery/labels"
    required_params = [
        "shop_id",
        "order_id",
    ]


class SetYandexMarketShipmentTrackAPI(YandexMarketAPI):
    """
    https://yandex.ru/dev/market/partner-dsbs/doc/dg/reference/post-campaigns-id-orders-id-delivery-track.html
    """

    description = "Передача трек-номера посылки"
    http_method = "POST"
    resource_method = "campaigns/{shop_id}/orders/{order_id}/delivery/track"
    required_params = [
        "shop_id",
        "order_id",
    ]
