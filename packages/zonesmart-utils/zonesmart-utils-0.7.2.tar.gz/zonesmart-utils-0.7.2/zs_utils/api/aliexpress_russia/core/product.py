from zs_utils.api.aliexpress_russia.base_api import AliexpressRussiaAPI


class GetAliexpressListingListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/product-list#heading-poluchit-otfiltrovannii-spisok-tovarov
    """

    resource_method = "/api/v1/scroll-short-product-by-filter"
    required_params = ["limit"]  # 50
    allowed_params = [
        "filter",
        "last_product_id",
    ]


class GetAliexpressListingAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/product-list#heading-poluchit-informatsiyu-o-tovare
    """

    resource_method = "/api/v1/product/get-seller-product"
    required_params = ["product_id"]


class CreateAliexpressListingAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-create-products
    """

    resource_method = "/api/v1/product/create"
    required_params = ["products"]


class UpdateAliexpressListingAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/post-products#heading-obnovit-vse-polya-tovara
    """

    resource_method = "/api/v1/product/edit"
    required_params = ["products"]


class SetPublishedAliexpressListingAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/post-products#heading-vernut-tovari-v-prodazhu
    """

    resource_method = "/api/v1/product/online"
    required_params = ["productIds"]  # 20


class SetUnpublishedAliexpressListingAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/post-products#heading-snyat-tovari-s-prodazhi
    """

    resource_method = "/api/v1/product/offline"
    required_params = ["productIds"]  # 20


class GetAliexpressListingStatusAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/post-products#heading-poluchit-statusi-zagruzkiobnovleniya-tovara
    """

    http_method = "GET"
    resource_method = "/api/v1/tasks"
    required_params = ["group_id"]


class GetAliexpressProductStocksAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/manage-stocks#heading-poluchit-ostatki-tovara
    """

    resource_method = "/api/v1/stocks"
    required_params = ["stocks"]


class UpdateAliexpressProductStocksAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/manage-stocks#heading-obnovit-ostatki-tovara-po-sku-kodu
    """

    resource_method = "/api/v1/product/update-sku-stock"
    required_params = ["products"]


class UpdateAliexpressProductPriceAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/manage-stocks#heading-obnovit-tsenu-tovara-po-sku-kodu
    """

    resource_method = "/api/v1/product/update-sku-price"
    required_params = ["products"]


class GetAliexpressShippingTemplatesAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-get-shipping-templates
    """

    http_method = "GET"
    resource_method = "/api/v1/sellercenter/get-count-product-on-onboarding-template"
