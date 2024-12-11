from zs_utils.api.aliexpress_russia.base_api import AliexpressRussiaAPI


class GetAliexpressCategoryTreeAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/categories#heading-poluchit-kategorii-verhnego-urovnya
    """

    resource_method = "/api/v1/categories/top"


class GetAliexpressCategoryInfoAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/categories#heading-poluchit-atributi-kategorii
    """

    resource_method = "/api/v1/categories/get"
    required_params = ["ids"]


class GetAliexpressAttributeValuesAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/categories#heading-poluchit-informatsiyu-o-znacheniyah-atributa
    """

    resource_method = "/api/v1/categories/values-dictionary"
    required_params = ["category_id", "property_id", "is_sku_property"]


class GetAliexpressBrandsAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/brand
    """

    resource_method = "/api/v1/brand/get-brand-list"
    required_params = ["offset", "limit"]
    allowed_params = ["filters", "sort"]
