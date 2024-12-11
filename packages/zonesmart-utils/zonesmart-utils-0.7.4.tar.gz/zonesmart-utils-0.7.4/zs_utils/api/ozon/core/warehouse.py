from zs_utils.api.ozon.base_api import OzonAPI


class OzonGetWarehouseListAPI(OzonAPI):
    resource_method = "v1/warehouse/list"


class OzonGetWarehouseMethodListAPI(OzonAPI):
    resource_method = "v1/delivery-method/list"
    required_params = ["limit"]
    allowed_params = ["filter", "offset"]
