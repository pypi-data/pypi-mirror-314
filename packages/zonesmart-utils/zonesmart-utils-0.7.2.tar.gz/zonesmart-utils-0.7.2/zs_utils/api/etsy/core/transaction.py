from zs_utils.api.etsy.base_api import EtsyAPI


class FindAllShopTransactions(EtsyAPI):
    """
    Retrieves a set of Transaction objects associated to a Shop.

    Docs:
    https://www.etsy.com/openapi/developers#operation/getShopReceiptTransactionsByShop
    """

    http_method = "GET"
    api_target = "transactions"


class FindAllShopReceiptTransactions(EtsyAPI):
    """
    Retrieves a set of Transaction objects associated to a Shop_Receipt2.

    Docs:
    https://www.etsy.com/openapi/developers#operation/getShopReceiptTransactionsByReceipt
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/receipts/{receipt_id}/transactions"
    required_params = ["shop_id", "receipt_id"]
