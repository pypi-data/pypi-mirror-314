from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesCategoryList(WildberriesAPI):
    """
    Docs: https://openapi.wb.ru/content/api/ru/#tag/Konfigurator/paths/~1content~1v2~1object~1all/get
    """

    http_method = "GET"
    resource_method = "content/v2/object/all"
    allowed_params = ["name", "limit", "offset", "parentID"]


class GetWildberriesCategoryParentList(WildberriesAPI):
    """
    Docs: https://openapi.wb.ru/content/api/ru/#tag/Konfigurator/paths/~1content~1v2~1object~1parent~1all/get
    """

    http_method = "GET"
    resource_method = "content/v2/object/parent/all"


class GetWildberriesCategoryAttributes(WildberriesAPI):
    """
    Docs: https://openapi.wb.ru/content/api/ru/#tag/Konfigurator/paths/~1content~1v2~1object~1charcs~1%7BsubjectId%7D/get
    """

    http_method = "GET"
    resource_method = "content/v2/object/charcs/{subjectId}"
    required_params = ["subjectId"]


class GetWildberriesAttributeValues(WildberriesAPI):
    """
    Docs: https://openapi.wildberries.ru/#tag/Kontent-Konfigurator/paths/~1content~1v1~1directory~1colors/get
    Значения dictionary_name:
    - colors (Цвет)
    - kinds (Пол)
    - countries (Страна производства)
    - seasons (Сезон)
    - tnved (ТНВЭД)
    """

    http_method = "GET"
    resource_method = "content/v2/directory/{dictionary_name}"
    required_params = []
    allowed_params = [
        "search",  # только tnved
        "subjectID",  # только tnved
    ]
