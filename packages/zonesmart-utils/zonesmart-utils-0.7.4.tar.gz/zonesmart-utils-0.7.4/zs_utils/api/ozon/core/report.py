from zs_utils.api.ozon.base_api import OzonAPI


class GetReportInfoAPI(OzonAPI):
    resource_method = "v1/report/info"
    required_params = ["code"]


class CreateStockReportAPI(OzonAPI):
    resource_method = "v1/report/stock/create"
