from zs_utils.api.aliexpress.base_api import AliexpressAPI


class GetLogisticsServiceListAPI(AliexpressAPI):
    resource_method = "aliexpress.logistics.redefining.listlogisticsservice"


class GetOnlineLogisticsServiceByOrderIdAPI(AliexpressAPI):
    resource_method = "aliexpress.logistics.redefining.getonlinelogisticsservicelistbyorderid"
    required_params = ["order_id"]
    allowed_params = ["goods_width", "goods_height", "goods_weight", "goods_length"]


class CreateWarehouseOrderAPI(AliexpressAPI):
    resource_method = "logistics.createwarehouseorder"
    required_params = [
        "address_d_t_os",
        "declare_product_d_t_os",
        "domestic_logistics_company_id",
        "domestic_tracking_no",
        "trade_order_from",
        "trade_order_id",
        "warehouse_carrier_service",
    ]
    allowed_params = [
        "domestic_logistics_company",
        "package_num",
        "undeliverable_decision",
        "invoice_number",
        "top_user_key",
    ]
