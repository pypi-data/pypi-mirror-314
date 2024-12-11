from zs_utils.api.ebay.base_api import EbayAPI


class CreateFulfillmentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/fulfillment_policy/methods/createFulfillmentPolicy
    """

    http_method = "POST"
    resource_method = "sell/account/v1/fulfillment_policy"


class DeleteFulfillmentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/fulfillment_policy/methods/deleteFulfillmentPolicy
    """

    http_method = "DELETE"
    resource_method = "sell/account/v1/fulfillment_policy/{fulfillment_policy_id}"
    required_params = ["fulfillment_policy_id"]


class GetEbayFulfillmentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/fulfillment_policy/methods/getFulfillmentPolicy
    """

    http_method = "GET"
    resource_method = "sell/account/v1/fulfillment_policy/{fulfillment_policy_id}"
    required_params = ["fulfillment_policy_id"]


class GetFulfillmentPolicies(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/fulfillment_policy/methods/getFulfillmentPolicies
    """

    http_method = "GET"
    resource_method = "sell/account/v1/fulfillment_policy"
    required_params = ["marketplace_id"]


class GetFulfillmentPolicyByName(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/fulfillment_policy/methods/getFulfillmentPolicyByName
    """

    http_method = "GET"
    resource_method = "sell/account/v1/fulfillment_policy/get_by_policy_name"
    required_params = ["marketplace_id", "name"]


class UpdateEbayFulfillmentPolicy(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/account/resources/fulfillment_policy/methods/updateFulfillmentPolicy
    """

    http_method = "PUT"
    resource_method = "sell/account/v1/fulfillment_policy/{fulfillment_policy_id}"
    required_params = ["fulfillment_policy_id"]
