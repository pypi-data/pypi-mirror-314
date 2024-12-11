from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipGetPointsAPI(ApishipAPI):
    """
    Docs: https://docs.apiship.ru/docs/api/lists-points/
    """

    resource_method = "lists/points"
    http_method = "GET"
    allowed_params = [
        "limit",
        "offset",
        "filter",
        "fields",
        "stateCheckOff",
    ]
