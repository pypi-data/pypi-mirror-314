from datetime import datetime
from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetEbayAccountBillingInfo",
    "GetEbaySellingInfo",
    "GetEbaySellingSummary",
]


class GetEbayAccountBillingInfo(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/GetAccount.html
    """

    method_name = "GetAccount"

    def get_params(
        self,
        account_history_selection: str,
        begin_date: datetime = None,  # 4 months ago -- ebay limit
        end_date: datetime = None,
        **kwargs,
    ):
        assert account_history_selection in [
            "BetweenSpecifiedDates",
            "LastInvoice",
        ], "Недопустимое значение 'account_history_selection'."

        if account_history_selection == "BetweenSpecifiedDates":
            assert begin_date and end_date, "Необходимо задать временной диапазон ('begin_date' и 'end_date')."

        return {
            "AccountHistorySelection": account_history_selection,
            # "AccountEntrySortType": "AccountEntryCreatedTimeDescending",
            "BeginDate": begin_date,
            "EndDate": end_date,
            "ExcludeBalance": False,
            "ExcludeSummary": False,
        }


class GetEbaySellingInfo(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/devzone/xml/docs/reference/ebay/GetMyeBaySelling.html
    """

    method_name = "GetMyeBaySelling"

    containers = [
        "ActiveList",
        "DeletedFromSoldList",
        "DeletedFromUnsoldList",
        "ScheduledList",
        "SoldList",
        "UnsoldList",
        "SellingSummary",
    ]

    def get_params(self, **kwargs):
        return {container: {"Include": kwargs.get(container, False)} for container in self.containers}


class GetEbaySellingSummary(GetEbaySellingInfo):
    def get_params(self, **kwargs):
        kwargs.update({container: False for container in self.containers})
        kwargs["SellingSummary"] = True
        return super().get_params(**kwargs)
