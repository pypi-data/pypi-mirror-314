from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipGetConnectionSchemasApi(ApishipAPI):
    resource_method = "connections/schemas"
    http_method = "GET"
    allowed_params = ["offset", "limit", "providerKey"]


class ApishipGetConnectionListApi(ApishipAPI):
    resource_method = "connections"
    http_method = "GET"
    allowed_params = ["offset", "limit", "filter"]


class ApishipCreateConnectionAPI(ApishipAPI):
    resource_method = "connections"
    http_method = "POST"
    required_params = [
        "providerKey",
        "name",
        "insuranceRate",
        "cashServiceRate",
        "connectParams",
        "isUseBaseConnect",
    ]


class ApishipGetConnectionAPI(ApishipAPI):
    resource_method = "connections/{connection_id}"
    http_method = "GET"
    required_params = ["connection_id"]


class ApishipUpdateConnectionAPI(ApishipAPI):
    resource_method = "connections/{connection_id}"
    http_method = "PUT"
    required_params = [
        "connection_id",
        "providerKey",
        "name",
        "insuranceRate",
        "cashServiceRate",
        "connectParams",
        "isUseBaseConnect",
    ]


class ApishipDeleteConnectionAPI(ApishipAPI):
    resource_method = "connections/{connection_id}"
    http_method = "DELETE"
    required_params = ["connection_id"]
