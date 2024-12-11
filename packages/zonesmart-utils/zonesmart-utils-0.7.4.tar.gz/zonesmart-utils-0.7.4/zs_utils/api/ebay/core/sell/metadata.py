from zs_utils.api.ebay.base_api import EbayAPI


class GetListingStructurePolicies(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/metadata/resources/marketplace/methods/getListingStructurePolicies
    """

    http_method = "GET"
    resource_method = "sell/metadata/v1/marketplace/{marketplace_id}/get_listing_structure_policies"
    required_params = ["marketplace_id"]
    allowed_params = ["filter"]


class GetItemConditionPolicies(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/metadata/resources/marketplace/methods/getItemConditionPolicies
    """

    http_method = "GET"
    resource_method = "sell/metadata/v1/marketplace/{marketplace_id}/get_item_condition_policies"
    required_params = ["marketplace_id"]
    allowed_params = ["filter"]


class GetAutomotivePartsCompatibilityPolicies(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/metadata/resources/marketplace/methods/getAutomotivePartsCompatibilityPolicies
    """  # noqa

    http_method = "GET"
    resource_method = "sell/metadata/v1/marketplace/{marketplace_id}/get_automotive_parts_compatibility_policies"
    required_params = ["marketplace_id"]
    allowed_params = ["filter"]
