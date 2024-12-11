from zs_utils.api.etsy.base_api import EtsyAPI


class GetReceipt(EtsyAPI):
    """
    Requests a Shop Receipt with a specific receipt id from a Shop.

    Docs:
    https://www.etsy.com/openapi/developers#operation/getShopReceipt
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/receipts/{receipt_id}"
    required_params = ["shop_id", "receipt_id"]


class FindAllShopReceipts(EtsyAPI):
    """
    Retrieves a set of Receipt objects associated to a Shop.

    Docs:
    https://www.etsy.com/openapi/developers#operation/getShopReceipts
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/receipts"
    required_params = ["shop_id"]
    allowed_params = [
        "min_created",
        "max_created",
        "min_last_modified",
        "max_last_modified",
        "limit",
        "offset",
        "was_paid",
        "was_shipped",
    ]


class SubmitTracking(EtsyAPI):
    """
    Submits tracking information and sends a shipping notification email to the buyer.
    If send_bcc is true, the shipping notification will be sent to the seller as well.

    Docs:
    https://www.etsy.com/openapi/developers#operation/createReceiptShipment
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/receipts/{receipt_id}/tracking"
    required_params = [
        "shop_id",
        "receipt_id",
    ]
    allowed_params = [
        "tracking_code",
        "carrier_name",
        "send_bcc",
    ]
