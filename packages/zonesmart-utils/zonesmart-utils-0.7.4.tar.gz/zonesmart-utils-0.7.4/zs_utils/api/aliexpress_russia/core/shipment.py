from zs_utils.api.aliexpress_russia.base_api import AliexpressRussiaAPI


class CreateAliexpressShipmentAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-logistic-orders#heading-sozdat-otpravlenie
    """

    resource_method = "/seller-api/v1/logistic-order/create"
    required_params = ["orders"]


class DeleteAliexpressShipmentAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-logistic-orders#heading-udalit-otpravlenie
    """

    resource_method = "/seller-api/v1/logistic-order/delete"
    required_params = ["logistic_order_ids"]


class GetAliexpressLabelAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-logistic-orders#heading-napechatat-etiketki-dlya-otpravlenii
    """

    resource_method = "/seller-api/v1/labels/orders/get"
    required_params = ["logistic_order_ids"]


# Лист передач (накладная)


class GetAliexpressHandoverListsAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-handover-list#heading-poluchit-spisok-listov-peredachi
    """

    resource_method = "/seller-api/v1/handover-list/get-by-filter"
    required_params = ["page_size", "page_number"]
    allowed_params = [
        "statuses",
        "handover_list_ids",
        "logistic_order_ids",
        "gmt_create_from",
        "gmt_create_to",
        "arrival_date_sort",
        "gmt_create_sort",
    ]


class CreateAliexpressHandoverListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-handover-list#heading-sozdat-list-peredachi
    """

    resource_method = "/seller-api/v1/handover-list/create"
    required_params = ["logistic_order_ids"]


class CloseAliexpressHandoverListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-handover-list#heading-zakrit-list-peredachi
    """

    resource_method = "/seller-api/v1/handover-list/transfer"
    required_params = ["handover_list_id"]


class AddAliexpressShipmentToHandoverListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-handover-list#heading-dobavit-otpravlenie-v-list-peredachi
    """

    resource_method = "/seller-api/v1/handover-list/add-logistic-orders"
    required_params = ["handover_list_id", "order_ids"]


class DeleteAliexpressShipmentFromHandoverListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-handover-list#heading-udalit-otpravlenie-iz-lista-peredachi
    """

    resource_method = "/seller-api/v1/handover-list/remove-logistic-orders"
    required_params = ["handover_list_id", "order_ids"]


class GetAliexpressHandoverListLabelAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/local-handover-list#heading-napechatat-list-peredachi
    """

    resource_method = "/seller-api/v1/labels/handover-lists/get"
    required_params = ["handover_list_id"]
