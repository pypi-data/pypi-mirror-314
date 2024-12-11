from zs_utils.api.aliexpress.base_api import AliexpressAPI


class GetDropshippingProductInfo(AliexpressAPI):
    resource_method = "aliexpress.postproduct.redefining.findaeproductbyidfordropshipper"
    allowed_params = ["product_id", "local_country", "local_language"]


class DropshippingPlaceOrderAPI(AliexpressAPI):
    resource_method = "aliexpress.trade.buy.placeorder"
    required_params = ["param_place_order_request4_open_api_d_t_o"]


class GetDropshippingLogisticInfoAPI(AliexpressAPI):
    resource_method = "aliexpress.logistics.buyer.freight.calculate"
    required_params = ["param_aeop_freight_calculate_for_buyer_d_t_o"]


class GetDropshippingOrderInfoAPI(AliexpressAPI):
    resource_method = "aliexpress.trade.ds.order.get"
    required_params = ["single_order_query"]


class GetDropshippingSimpleProductInfoAPI(AliexpressAPI):
    resource_method = "aliexpress.offer.ds.product.simplequery"
    allowed_params = ["product_id", "local_country", "local_language"]


class GetDropshippingTrackingInfoAPI(AliexpressAPI):
    resource_method = "aliexpress.logistics.ds.trackinginfo.query"
    required_params = ["logistics_no", "origin", "out_ref", "service_name", "to_area"]


class SyncDropshippingSalesDataAPI(AliexpressAPI):
    resource_method = "aliexpress.member.ds.orderdata.save"
    required_params = ["dser_collect_data"]
