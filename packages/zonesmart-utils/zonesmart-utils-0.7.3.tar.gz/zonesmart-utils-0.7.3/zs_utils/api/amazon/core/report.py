from zs_utils.api.amazon.base_api import AmazonAPI


class CreateReportAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference#post-reports2021-06-30reports
    """

    http_method = "POST"
    resource_method = "reports/2021-06-30/reports"
    required_params = ["payload"]


class GetReportAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference#get-reports2021-06-30reportsreportid
    """

    http_method = "GET"
    resource_method = "reports/2021-06-30/reports/{reportId}"
    required_params = ["reportId"]


class GetReportDocumentAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference#get-reports2021-06-30documentsreportdocumentid
    """

    http_method = "GET"
    resource_method = "reports/2021-06-30/documents/{reportDocumentId}"
    required_params = ["reportDocumentId"]
