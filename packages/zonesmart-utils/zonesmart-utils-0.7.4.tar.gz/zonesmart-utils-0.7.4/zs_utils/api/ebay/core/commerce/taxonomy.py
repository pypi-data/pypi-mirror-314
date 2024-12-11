from zs_utils.api.ebay.base_api import EbayAPI


class TaxonomyAPI(EbayAPI):
    @property
    def headers(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Encoding": "application/gzip",
        }
        return headers


class GetDefaultCategoryTreeId(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getDefaultCategoryTreeId
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/get_default_category_tree_id"
    required_params = ["marketplace_id"]


class GetCategoryTree(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getCategoryTree
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/category_tree/{category_tree_id}"
    required_params = ["category_tree_id"]


class GetCategorySubtree(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getCategorySubtree
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/category_tree/{category_tree_id}/get_category_subtree"
    required_params = ["category_tree_id", "category_id"]


class GetCategorySuggestions(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getCategorySuggestions
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/category_tree/{category_tree_id}/get_category_suggestions"
    required_params = ["category_tree_id", "q"]


class GetItemAspectsForCategory(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getItemAspectsForCategory
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/category_tree/{category_tree_id}/get_item_aspects_for_category"
    required_params = ["category_tree_id", "category_id"]


class GetCompatibilityProperties(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getCompatibilityProperties
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/category_tree/{category_tree_id}/get_compatibility_properties"
    required_params = ["category_tree_id", "category_id"]


class GetCompatibilityPropertyValues(TaxonomyAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getCompatibilityPropertyValues
    """

    http_method = "GET"
    resource_method = "commerce/taxonomy/v1/category_tree/{category_tree_id}/get_compatibility_property_values"
    required_params = ["category_tree_id", "compatibility_property", "category_id"]
    allowed_params = ["filter"]
