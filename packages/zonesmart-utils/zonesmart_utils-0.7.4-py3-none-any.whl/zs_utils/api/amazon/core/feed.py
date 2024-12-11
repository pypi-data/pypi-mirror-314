from zs_utils.api.amazon.base_api import AmazonAPI


class GetFeedAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference#post-feeds2021-06-30feeds
    """

    http_method = "GET"
    resource_method = "feeds/2021-06-30/feeds/{feedId}"
    required_params = ["feedId"]


class CreateFeedDocumentAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference#post-feeds2021-06-30documents
    """

    http_method = "POST"
    resource_method = "feeds/2021-06-30/documents"
    required_params = [
        "payload"
    ]  # POST_ORDER_ACKNOWLEDGEMENT_DATA - cancel order, POST_INVENTORY_AVAILABILITY_DATA - update stocks


class UploadFeedDataAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference#createfeeddocumentresponse
    """

    http_method = "PUT"
    required_params = ["payload"]


class CreateFeedAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference#post-feeds2021-06-30feeds
    """

    http_method = "POST"
    resource_method = "feeds/2021-06-30/feeds"
    required_params = ["payload"]
