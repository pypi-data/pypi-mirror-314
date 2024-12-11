from zs_utils.api.amazon.base_api import AmazonAPI


class GetCategoryTreeAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v0-reference#listcatalogcategories
    """

    http_method = "GET"
    resource_method = "catalog/v0/categories"
    required_params = ["MarketplaceId"]
    allowed_params = [
        "ASIN",
        "SellerSKU",
    ]


class GetProductTypeDefinitionAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/product-type-definitions-api-v2020-09-01-reference#get-definitions2020-09-01producttypesproducttype
    """

    http_method = "GET"
    resource_method = "definitions/2020-09-01/productTypes/{productType}"
    required_params = ["productType", "marketplaceIds"]
    allowed_params = [
        "sellerId",
        "productTypeVersion",
        "requirements",
        "requirementsEnforced",
        "locale",
    ]
