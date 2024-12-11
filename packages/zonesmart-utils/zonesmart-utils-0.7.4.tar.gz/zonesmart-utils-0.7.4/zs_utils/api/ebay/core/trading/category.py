from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetEbayCategoryFeatures",
    "GetCategorySpecifics",
    "GetTransportCategoryAspectsVS",
]


class GetEbayCategoryFeatures(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetCategoryFeatures.html
    """

    method_name = "GetCategoryFeatures"

    def get_params(self, category_id=None, feature_ids=None, **kwargs):
        return {
            "AllFeaturesForCategory": False,
            "CategoryID": category_id,
            "FeatureID": feature_ids,
            "ViewAllNodes": True,
            "DetailLevel": "ReturnAll",
        }


class GetCategorySpecifics(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetCategorySpecifics.html
    """

    method_name = "GetCategorySpecifics"

    def get_params(self, category_id, **kwargs):
        return {
            "CategoryID": category_id,
        }


class GetTransportCategoryAspectsVS(GetCategorySpecifics):
    def __init__(self, *args, **kwargs):
        kwargs["domain_code"] = "EBAY_MOTORS_US"
        return super().__init__(*args, **kwargs)
