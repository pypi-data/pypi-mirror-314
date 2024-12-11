import datetime

from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetListingList",
    "GetListing",
]


class GetListingList(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetSellerList.html
    """

    method_name = "GetSellerList"

    def get_params(
        self, PageNumber: int, EntriesPerPage: int = 200, EndTimeFrom=None, EndTimeTo=None, CategoryID=None, **kwargs
    ):
        if isinstance(EndTimeTo, str):
            EndTimeTo = datetime.datetime.fromisoformat(EndTimeTo)
        if isinstance(EndTimeFrom, str):
            EndTimeFrom = datetime.datetime.fromisoformat(EndTimeFrom)
        if not EndTimeFrom:
            EndTimeFrom = datetime.datetime.now()
        if (not EndTimeTo) or ((EndTimeTo - EndTimeFrom).days > 120):
            EndTimeTo = EndTimeFrom + datetime.timedelta(days=120)

        params = {
            "CategoryID": CategoryID,
            "EndTimeFrom": EndTimeFrom.isoformat(),
            "EndTimeTo": EndTimeTo.isoformat(),
            "GranularityLevel": "Medium",
            "IncludeVariations": True,
            "DetailLevel": "ItemReturnDescription",
            "WarningLevel": "High",
            "Pagination": {
                "PageNumber": PageNumber,
                "EntriesPerPage": EntriesPerPage,
            },
        }

        return params


class GetListing(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/Reference/eBay/GetItem.html
    """

    method_name = "GetItem"

    def get_params(self, remote_id: str, detail_level="ReturnAll", **kwargs):
        return {
            "ItemID": remote_id,
            "IncludeItemCompatibilityList": True,
            "IncludeItemSpecifics": True,
            "DetailLevel": detail_level,
        }
