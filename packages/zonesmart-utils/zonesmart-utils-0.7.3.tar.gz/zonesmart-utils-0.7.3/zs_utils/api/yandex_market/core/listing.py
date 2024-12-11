from zs_utils.api.yandex_market.base_api import YandexMarketAPI


class UpdateYandexOfferPriceAPI(YandexMarketAPI):
    description = "Обновление цен предложений Yandex Market"
    http_method = "POST"
    resource_method = "campaigns/{shop_id}/offer-prices/updates"
    required_params = [
        "shop_id",
    ]
