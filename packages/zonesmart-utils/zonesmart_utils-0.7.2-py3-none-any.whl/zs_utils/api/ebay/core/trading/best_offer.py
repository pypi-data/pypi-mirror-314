"""
Docs:
https://developer.ebay.com/DevZone/guides/features-guide/default.html#development/feature-bestoffer.html
"""

from zs_utils.api.ebay.base_api import EbayTradingAPI
from .category import GetEbayCategoryFeatures
from .messages import AbstractSendMessage


__all__ = [
    "GetCategoryBestOfferFeatures",
    "GetListingBestOffers",
    "RespondToListingBestOffer",
    "SendBestOfferMessage",
]


class GetCategoryBestOfferFeatures(GetEbayCategoryFeatures):
    def get_params(self, category_id: int, **kwargs):
        kwargs["feature_ids"] = [
            "BestOfferEnabled",
            "BestOfferAutoDeclineEnabled",
            "BestOfferAutoAcceptEnabled",
        ]
        return super().get_params(category_id=category_id, **kwargs)


class GetListingBestOffers(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/DevZone/XML/docs/Reference/eBay/GetBestOffers.html
    """

    method_name = "GetBestOffers"

    def get_params(
        self,
        best_offer_id: int = None,
        item_id: int = None,
        active_only: bool = True,
        **kwargs,
    ):
        if active_only:
            best_offer_status = "Active"
        else:
            best_offer_status = "All"

        return {
            "BestOfferID": best_offer_id,
            "BestOfferStatus": best_offer_status,
            "ItemID": item_id,
            "DetailLevel": "ReturnAll",
        }


class RespondToListingBestOffer(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/RespondToBestOffer.html
    """

    method_name = "RespondToBestOffer"

    def get_params(
        self,
        action: str,
        best_offer_id: int,
        item_id: int,
        counter_offer_price: float = None,
        counter_offer_quantity: int = None,
        seller_response: str = None,
        **kwargs,
    ):
        if not (action in ["Accept", "Counter", "Decline"]):
            raise AttributeError('Недопустимое значение параметра "action".')
        if best_offer_id and (not item_id):
            raise ValueError("Если задан 'best_offer_id', то должен быть задан 'item_id'.")

        return {
            "Action": action,
            "BestOfferID": best_offer_id,
            "ItemID": item_id,
            "CounterOfferPrice": counter_offer_price,
            "currencyID": "USD",
            "CounterOfferQuantity": counter_offer_quantity,
            "SellerResponse": seller_response,
        }


class SendBestOfferMessage(AbstractSendMessage):
    """
    AddMemberMessagesAAQToBidder:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/AddMemberMessagesAAQToBidder.html
    HINT: item needs to be tested
    """

    method_name = "AddMemberMessagesAAQToBidder"

    def get_params(self, **kwargs):
        params = super().get_params(**kwargs)
        params.update({"CorrelationID": "1"})
        return params
