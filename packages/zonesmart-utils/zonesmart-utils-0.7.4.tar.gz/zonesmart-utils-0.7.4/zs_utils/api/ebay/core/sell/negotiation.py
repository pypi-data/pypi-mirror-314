from zs_utils.api.ebay.base_api import EbayAPI


class FindEligibleItems(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/negotiation/resources/offer/methods/findEligibleItems
    """

    http_method = "GET"
    resource_method = "sell/negotiation/v1/find_eligible_items"
    allowed_params = ["limit", "offset"]
    MAX_LIMIT = 200


class SendOfferToInterestedBuyers(EbayAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/negotiation/resources/offer/methods/sendOfferToInterestedBuyers
    """

    http_method = "POST"
    resource_method = "sell/negotiation/v1/send_offer_to_interested_buyers"
