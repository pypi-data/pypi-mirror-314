"""
Docs: https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/types/NotificationEventTypeCodeType.html
"""
from model_utils import Choices


ClientAlertsEventTypeEnum = Choices(  # not compatible with PlatformNotifications
    "AccountSummary",
    "AccountSuspended",
    "EmailAddressChanged",
    "PasswordChanged",
    "PaymentDetailChanged",
)


PlatformNotificationEventTypeEnum = Choices(  # not compatible with ClientAlerts
    # BestOffers
    "BestOffer",
    # "BestOfferPlaced",
    # Feedbacks
    # "Feedback",
    # "FeedbackLeft",
    "FeedbackReceived",
    # Listings
    "FixedPriceTransaction",
    "ItemClosed",
    "ItemListed",
    "ItemOutOfStock",
    "ItemRevised",
    "ItemSuspended",
    # "ItemSold",
    # Messages
    "AskSellerQuestion",
    "M2MMessageStatusChange",
    "MyMessageseBayMessage",
    "MyMessageseBayMessageHeader",
    "MyMessagesHighPriorityMessage",
    "MyMessagesM2MMessage",
    "MyMessagesM2MMessageHeader",
    # Orders
    "ItemMarkedPaid",
    "ItemMarkedShipped",
    "BuyerResponseDispute",
    "BuyerCancelRequested",
    "OrderInquiryClosed",
    "OrderInquiryEscalatedToCase",
    "OrderInquiryOpened",
    "OrderInquiryProvideShipmentInformation",
    "OrderInquiryReminderForEscalation",
    "ReturnWaitingForSellerInfo",
    # Account
    "TokenRevocation",
    "UserIDChanged",
)


SupportedPlatformNotificationEventTypeEnum = Choices(
    "BestOffer",
    "FeedbackReceived",
    "ItemClosed",
    "ItemSuspended",
    "MyMessageseBayMessage",
    "MyMessagesM2MMessage",
    "UserIDChanged",
)
