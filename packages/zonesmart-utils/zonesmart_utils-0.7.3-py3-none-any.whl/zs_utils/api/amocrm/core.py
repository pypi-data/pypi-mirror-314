from zs_utils.api.amocrm.base_api import AmocrmAPI


class ListAmocrmLeadsAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-list
    """

    http_method = "GET"
    resource_method = "api/v4/leads"
    required_params = []
    allowed_params = [
        "with",
        "page",
        "limit",
        "query",
        "filter",
        "order",
    ]


class GetAmocrmLeadAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/leads-api#lead-detail
    """

    http_method = "GET"
    resource_method = "api/v4/leads/{lead_id}"
    required_params = ["lead_id"]
    allowed_params = ["with"]


class CreateAmocrmLeadAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-add
    """

    http_method = "POST"
    resource_method = "api/v4/leads"
    array_payload = True


class UpdateAmocrmLeadAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/leads-api#leads-edit
    """

    http_method = "PATCH"
    resource_method = "api/v4/leads"
    array_payload = True


class ListAmocrmContactsAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-list
    """

    http_method = "GET"
    resource_method = "api/v4/contacts"
    required_params = []
    allowed_params = [
        "with",
        "page",
        "limit",
        "query",
        "filter",
        "order",
    ]


class CreateAmocrmContactAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/contacts-api#contacts-add
    """

    http_method = "POST"
    resource_method = "api/v4/contacts"
    array_payload = True


class CreateAmocrmTaskAPI(AmocrmAPI):
    """
    Docs: https://www.amocrm.ru/developers/content/crm_platform/tasks-api#tasks-add
    """

    http_method = "POST"
    resource_method = "api/v4/tasks"
    array_payload = True
