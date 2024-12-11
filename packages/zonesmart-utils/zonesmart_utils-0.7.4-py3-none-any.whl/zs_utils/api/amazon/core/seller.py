from zs_utils.api.amazon.base_api import AmazonAPI


class GetSellerMarketplaceIdsAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/sellers-api-v1-reference#get-sellersv1marketplaceparticipations
    """

    http_method = "GET"
    resource_method = "sellers/v1/marketplaceParticipations"
