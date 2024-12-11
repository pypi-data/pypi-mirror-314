from zs_utils.api.aliexpress.base_api import AliexpressAPI


class OrderFulfillAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=42269&docType=2
    """

    resource_method = "aliexpress.solution.order.fulfill"
    required_params = ["service_name", "out_ref", "send_type", "logistics_no"]
    allowed_params = ["tracking_website", "description"]


class GetOrderListAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=42270&docType=2
    """

    resource_method = "aliexpress.solution.order.get"
    allowed_params = ["param0"]


class GetOrderInfoAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=42707&docType=2
    """

    resource_method = "aliexpress.solution.order.info.get"
    allowed_params = ["param1"]


class GetOrderReceiptInfoAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=42369&docType=2
    """

    resource_method = "aliexpress.solution.order.receiptinfo.get"
    allowed_params = ["param1"]
