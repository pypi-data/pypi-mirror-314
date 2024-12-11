from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesWarehouseList(WildberriesAPI):
    """
    https://openapi.wildberries.ru/?ysclid=ljzow9j5e0958977292#tag/Marketplace-Sklady/paths/~1api~1v3~1warehouses/get
    """

    http_method = "GET"
    resource_method = "api/v3/warehouses"


class GetWildberriesWarehouseStock(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Ostatki/paths/~1api~1v3~1stocks~1%7BwarehouseId%7D/post
    """

    http_method = "POST"
    resource_method = "api/v3/stocks/{warehouseId}"
    required_params = ["skus"]


class DeleteWildberriesStocks(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Ostatki/paths/~1api~1v3~1stocks~1%7BwarehouseId%7D/delete
    """

    http_method = "DELETE"
    resource_method = "api/v3/stocks/{warehouseId}"
    required_params = ["skus"]


class UpdateWildberriesStocks(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace-Ostatki/paths/~1api~1v3~1stocks~1%7BwarehouseId%7D/put
    """

    http_method = "PUT"
    resource_method = "api/v3/stocks/{warehouseId}"
    required_params = ["stocks"]
