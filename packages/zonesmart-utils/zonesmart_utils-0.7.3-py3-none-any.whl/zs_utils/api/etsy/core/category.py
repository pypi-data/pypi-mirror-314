from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyCategories(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getSellerTaxonomyNodes
    """

    description = "Получение категорий товаров Etsy"
    http_method = "GET"
    resource_method = "seller-taxonomy/nodes"


class GetEtsyCategoryAspects(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getPropertiesByTaxonomyId
    """

    description = "Получение проперти для категории товаров Etsy"
    http_method = "GET"
    resource_method = "seller-taxonomy/nodes/{taxonomy_id}/properties"
    required_params = ["taxonomy_id"]
