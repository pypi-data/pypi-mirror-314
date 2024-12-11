from zs_utils.api.ozon.base_api import OzonAPI


class OzonGetCategoriesTreeAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/DescriptionCategoryAPI_GetTree
    """

    resource_method = "v1/description-category/tree"
    allowed_params = ["language"]


class OzonGetCategoryAttributeAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/DescriptionCategoryAPI_GetAttributes
    """

    resource_method = "v1/description-category/attribute"
    required_params = ["description_category_id", "type_id"]
    allowed_params = ["language"]


class OzonGetCategoryAttributeDictionaryAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/DescriptionCategoryAPI_GetAttributeValues
    """

    resource_method = "v1/description-category/attribute/values"
    required_params = ["attribute_id", "description_category_id", "limit", "type_id"]
    allowed_params = ["language", "last_value_id"]
