from zs_utils.api.ebay.base_api import EbayAPI


class CreatePaymentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/payment_policy/methods/createPaymentPolicy
    """

    http_method = "POST"
    resource_method = "sell/account/v1/payment_policy"


class DeletePaymentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/payment_policy/methods/deletePaymentPolicy
    """

    http_method = "DELETE"
    resource_method = "sell/account/v1/payment_policy/{payment_policy_id}"
    required_params = ["payment_policy_id"]


class GetEbayPaymentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/payment_policy/methods/getPaymentPolicy
    """

    http_method = "GET"
    resource_method = "sell/account/v1/payment_policy/{payment_policy_id}"
    required_params = ["payment_policy_id"]


class GetPaymentPolicies(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/payment_policy/methods/getPaymentPolicies
    """

    http_method = "GET"
    resource_method = "sell/account/v1/payment_policy"
    required_params = ["marketplace_id"]


class GetPaymentPolicyByName(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/payment_policy/methods/getPaymentPolicyByName
    """

    http_method = "GET"
    resource_method = "sell/account/v1/payment_policy/get_by_policy_name"
    required_params = ["marketplace_id", "name"]


class UpdateEbayPaymentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/payment_policy/methods/updatePaymentPolicy
    """

    http_method = "PUT"
    resource_method = "sell/account/v1/payment_policy/{payment_policy_id}"
    required_params = ["payment_policy_id"]
