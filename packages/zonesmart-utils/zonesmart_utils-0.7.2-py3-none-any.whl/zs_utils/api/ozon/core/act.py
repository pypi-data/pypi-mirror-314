from zs_utils.api.ozon.base_api import OzonAPI


class OzonCreateActAPI(OzonAPI):
    resource_method = "v2/posting/fbs/act/create"
    required_params = ["delivery_method_id"]
    allowed_params = ["containers_count"]


class OzonCheckActStatusAPI(OzonAPI):
    resource_method = "v2/posting/fbs/act/check-status"
    required_params = ["id"]


class OzonGetActAPI(OzonAPI):
    resource_method = "v2/posting/fbs/act/get-pdf"
    required_params = ["id"]


class OzonGetContainerLabelsAPI(OzonAPI):
    resource_method = "v2/posting/fbs/act/get-container-labels"
    required_params = ["id"]
