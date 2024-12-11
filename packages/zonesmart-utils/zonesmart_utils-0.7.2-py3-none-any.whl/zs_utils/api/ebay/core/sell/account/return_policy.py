from zs_utils.api.ebay.base_api import EbayAPI


class CreateReturnPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/return_policy/methods/createReturnPolicy
    """

    http_method = "POST"
    resource_method = "sell/account/v1/return_policy"


class DeleteReturnPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/return_policy/methods/deleteReturnPolicy
    """

    http_method = "DELETE"
    resource_method = "sell/account/v1/return_policy/{return_policy_id}"
    required_params = ["return_policy_id"]


class GetEbayReturnPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/return_policy/methods/getReturnPolicy
    """

    http_method = "GET"
    resource_method = "sell/account/v1/return_policy/{return_policy_id}"
    required_params = ["return_policy_id"]


class GetReturnPolicies(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/return_policy/methods/getReturnPolicies
    """

    http_method = "GET"
    resource_method = "sell/account/v1/return_policy"
    required_params = ["marketplace_id"]


class GetReturnPolicyByName(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/return_policy/methods/getReturnPolicyByName
    """

    http_method = "GET"
    resource_method = "sell/account/v1/return_policy/get_by_policy_name"
    required_params = ["marketplace_id", "name"]


class UpdateEbayReturnPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/return_policy/methods/updateReturnPolicy
    """

    http_method = "PUT"
    resource_method = "sell/account/v1/return_policy/{return_policy_id}"
    required_params = ["return_policy_id"]
