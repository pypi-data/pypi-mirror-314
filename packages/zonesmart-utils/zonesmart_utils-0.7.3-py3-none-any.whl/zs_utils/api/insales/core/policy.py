from zs_utils.api.insales.base_api import InsalesAPI


class GetInsalesPaymentPolicyList(InsalesAPI):
    """
    https://api.insales.ru/#paymentgateway-get-payment-gateways-json
    """

    resource_method = "payment_gateways.json"
    http_method = "GET"


class GetInsalesDeliveryPolicyList(InsalesAPI):
    """
    https://api.insales.ru/#deliveryvariant-get-delivery-variants-json
    """

    resource_method = "delivery_variants.json"
    http_method = "GET"
