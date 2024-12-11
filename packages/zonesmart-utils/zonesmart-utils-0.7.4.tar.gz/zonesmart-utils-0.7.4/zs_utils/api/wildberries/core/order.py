from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesOrders(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders/get
    """

    http_method = "GET"
    resource_method = "api/v3/orders"
    required_params = [
        "limit",  # 1000
        "next",  # offset, 0 for the first request
    ]
    allowed_params = [
        "dateFrom",
        "dateTo",
    ]


class GetWildberriesNewOrders(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1new/get
    """

    http_method = "GET"
    resource_method = "api/v3/orders/new"


class CancelWildberriesOrder(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1%7BorderId%7D~1cancel/patch
    """

    http_method = "PATCH"
    resource_method = "api/v3/orders/{order_id}/cancel"
    required_params = [
        "order_id",
    ]


class GetWildberriesOrdersStatus(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1status/post
    """

    http_method = "POST"
    resource_method = "api/v3/orders/status"
    required_params = [
        "orders",
    ]


class DeleteWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies~1%7BsupplyId%7D/delete
    """

    http_method = "DELETE"
    resource_method = "api/v3/supplies/{supply_id}"
    required_params = [
        "supply_id",
    ]


class GetWildberriesSupplies(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies/get
    """

    http_method = "GET"
    resource_method = "api/v3/supplies"
    required_params = [
        "limit",  # Up to 1000
        "next",  # offset, 0 for the first request
    ]


class GetWildberriesSupplyOrders(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies~1%7BsupplyId%7D~1orders/get
    """

    http_method = "GET"
    resource_method = "api/v3/supplies/{supply_id}/orders"
    required_params = [
        "supply_id",
    ]


class GetWildberriesSupplyBarcode(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies~1%7BsupplyId%7D~1barcode/get
    """

    http_method = "GET"
    resource_method = "api/v3/supplies/{supply_id}/barcode"
    required_params = [
        "supply_id",
        "type",
    ]


class GetWildberriesOrdersStickers(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1stickers/post
    """

    http_method = "POST"
    resource_method = "api/v3/orders/stickers"
    required_params = [
        "type",
        "width",
        "height",
        "orders",
    ]


class CreateWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies/post
    """

    http_method = "POST"
    resource_method = "api/v3/supplies"
    allowed_params = ["name"]


class AddOrdersToWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies~1%7BsupplyId%7D~1orders~1%7BorderId%7D/patch
    """

    http_method = "PATCH"
    resource_method = "api/v3/supplies/{supply_id}/orders/{order_id}"
    required_params = [
        "supply_id",
        "order_id",
    ]


class CloseWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1supplies~1%7BsupplyId%7D~1deliver/patch
    """

    http_method = "PATCH"
    resource_method = "api/v3/supplies/{supply_id}/deliver"
    required_params = [
        "supply_id",
    ]


class AddWildberriesSgtinToOrder(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Sborochnye-zadaniya/paths/~1api~1v3~1orders~1%7BorderId%7D~1meta~1sgtin/post
    """

    http_method = "POST"
    resource_method = "api/v3/orders/{order_id}/meta/sgtin"
    required_params = [
        "order_id",
        "sgtin",
    ]
