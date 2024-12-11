from zs_utils.api.amazon.base_api import AmazonAPI


class GetOrderListAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#get-ordersv0orders
    """

    http_method = "GET"
    resource_method = "orders/v0/orders"
    required_params = ["MarketplaceIds"]
    allowed_params = [
        "CreatedAfter",
        "CreatedBefore",
        "LastUpdatedAfter",
        "LastUpdatedBefore",
        "OrderStatuses",
        "FulfillmentChannels",
        "PaymentMethods",
        "BuyerEmail",
        "SellerOrderId",
        "MaxResultsPerPage",
        "EasyShipShipmentStatuses",
        "ElectronicInvoiceStatuses",
        "NextToken",
        "AmazonOrderIds",
        "ActualFulfillmentSupplySourceId",
        "IsISPU",
        "StoreChainStoreId",
        "EarliestDeliveryDateBefore",
        "EarliestDeliveryDateAfter",
        "LatestDeliveryDateBefore",
        "LatestDeliveryDateAfter",
    ]


class GetOrderAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#get-ordersv0ordersorderid
    """

    http_method = "GET"
    resource_method = "orders/v0/orders/{orderId}"
    required_params = ["orderId"]


class GetOrderItemsAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#get-ordersv0ordersorderidorderitems
    """

    http_method = "GET"
    resource_method = "orders/v0/orders/{orderId}/orderItems"
    required_params = ["orderId"]


class GetOrderAddressAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#get-ordersv0ordersorderidaddress
    """

    http_method = "GET"
    resource_method = "orders/v0/orders/{orderId}/address"
    required_params = ["orderId"]


class UpdateShipmentAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#post-ordersv0ordersorderidshipment
    """

    http_method = "POST"
    resource_method = "orders/v0/orders/{orderId}/shipment"
    required_params = ["orderId", "payload"]
    # payload = {
    #     "marketplaceId": "",
    #     "shipmentStatus": "",  # ReadyForPickup, PickedUp, RefusedPickup
    #     "orderItems": [{
    #         "orderItemId": "",
    #         "quantity": 1,
    #     }],
    # }


class ConfirmShipmentAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#post-ordersv0ordersorderidshipmentconfirmation
    """

    http_method = "POST"
    resource_method = "orders/v0/orders/{orderId}/shipmentConfirmation"
    required_params = ["orderId", "payload"]
    # payload = {
    #     "marketplaceId": "",
    #     "packageDetail": {
    #         "packageReferenceId": None,  # r
    #         "carrierCode": None,  # r
    #         "carrierName": None,
    #         "shippingMethod": None,
    #         "trackingNumber": None,  # r
    #         "shipDate": None,  # r
    #         "shipFromSupplySourceId": None,
    #         "orderItems": [{}],  # r (see above)
    #     },
    #     "codCollectionMethod": "DirectPayment",  # JP only
    # }
