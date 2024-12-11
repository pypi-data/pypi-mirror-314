import datetime
from dateutil.parser import parse

from zs_utils.api.ebay.base_api import EbayAPI


class PaymentDisputeAPI(EbayAPI):
    production_api_url = "https://apiz.ebay.com/"
    sandbox_api_url = "https://apiz.sandbox.ebay.com/"


class GetPaymentDispute(PaymentDisputeAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/payment_dispute/methods/getPaymentDispute
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/payment_dispute/{payment_dispute_id}"
    required_params = ["payment_dispute_id"]


class FetchEvidenceContent(PaymentDisputeAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/payment_dispute/methods/fetchEvidenceContent
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/payment_dispute/{payment_dispute_id}/fetch_evidence_content"
    required_params = ["payment_dispute_id", "evidence_id", "file_id"]


class GetActivities(PaymentDisputeAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/payment_dispute/methods/getActivities
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/payment_dispute/{payment_dispute_id}/activity"
    required_params = ["payment_dispute_id"]


class GetPaymentDisputeSummaries(PaymentDisputeAPI):
    """
    Docs:
    https://developer.ebay.com/api-docs/sell/fulfillment/resources/payment_dispute/methods/getPaymentDisputeSummaries
    """

    http_method = "GET"
    resource_method = "sell/fulfillment/v1/payment_dispute/payment_dispute_summary"
    allowed_params = [
        "order_id",
        "buyer_username",
        "open_date_from",
        "open_date_to",
        "payment_dispute_status",
        "limit",
        "offset",
    ]
    MAX_LIMIT = 200

    def get_clean_params(self, params: dict) -> dict:
        clean_params = super().get_clean_params(params)

        if clean_params.get("open_date_to"):
            clean_params["open_date_to"] = self.clean_open_date_to(value=clean_params["open_date_to"])

        if clean_params.get("open_date_from"):
            clean_params["open_date_from"] = self.clean_open_date_from(value=clean_params["open_date_from"])

        return clean_params

    def clean_open_date_to(self, value):
        value = parse(value)

        now = datetime.datetime.now()
        if now < value:
            value = now
        elif (now - value).days >= 18 * 30:
            raise self.exception_class(
                'Разница между датой "open_date_to" и настоящим моментом не должна превышать 18 месяцев.'
            )

        return value

    def clean_open_date_from(self, value):
        value = parse(value)

        now = datetime.datetime.now()
        if now <= value:
            raise self.exception_class('Дата "open_date_from" должна быть более ранней, чем сегодняшняя дата.')
        elif (now - value).days >= 18 * 30:
            raise self.exception_class(
                'Разница между датой "open_date_from" и настоящим моментом не должна превышать 18 месяцев.'
            )

        return value
