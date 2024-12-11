from zs_utils.api.ozon.base_api import OzonAPI


class OzonGetProductListAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetProductList
    """

    resource_method = "v2/product/list"
    allowed_params = [
        "filter",
        "last_id",
        "limit",
    ]


class OzonGetProductsInfoAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetProductInfoListV2
    """

    resource_method = "v2/product/info/list"
    allowed_params = ["offer_id", "product_id", "sku"]


class OzonGetProductsAttributeAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetProductAttributesV3
    """

    resource_method = "v3/products/info/attributes"
    required_params = ["limit"]
    allowed_params = [
        "filter",
        "last_id",
        "sort_by",
        "sort_dir",
    ]


class OzonGetProductsFBSStocksAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_ProductStocksByWarehouseFbs
    """

    resource_method = "v1/product/info/stocks-by-warehouse/fbs"
    required_params = ["fbs_sku"]


class OzonGetProductStatusAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_GetImportProductsInfo
    """

    resource_method = "v1/product/import/info"
    required_params = ["task_id"]


class OzonCreateProductAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_ImportProductsV3
    """

    resource_method = "v3/product/import"
    required_params = ["items"]


class OzonUpdateProductStocksAPI(OzonAPI):
    resource_method = "v1/product/import/stocks"
    required_params = ["stocks"]


class OzonUpdateProductWarehouseStocksAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_ProductsStocksV2
    """

    resource_method = "v2/products/stocks"
    required_params = ["stocks"]


class OzonArchiveProductAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_ProductArchive
    """

    resource_method = "v1/product/archive"
    required_params = ["product_id"]


class OzonDeleteProductFromArchiveAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_DeleteProducts
    """

    resource_method = "v2/products/delete"
    required_params = ["products"]


class OzonReturnProductFromArchiveAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_ProductUnarchive
    """

    resource_method = "v1/product/unarchive"
    required_params = ["product_id"]


class OzonUpdateProductPricesAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ProductAPI_ImportProductsPrices
    """

    resource_method = "v1/product/import/prices"
    required_params = ["prices"]
