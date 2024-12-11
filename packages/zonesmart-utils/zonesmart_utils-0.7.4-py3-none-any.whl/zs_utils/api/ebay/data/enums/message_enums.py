from model_utils import Choices


MessageStatusEnum = Choices(
    ("Answered", "Answered"),
    ("Unanswered", "Unanswered"),
)

MessageTypeEnum = Choices(
    ("All", "All"),
    ("AskSellerQuestion", "AskSellerQuestion"),
    ("ClassifiedsBestOffer", "ClassifiedsBestOffer"),
    ("ClassifiedsContactSeller", "ClassifiedsContactSeller"),
    ("ContactEbayMember", "ContactEbayMember"),
    ("ContacteBayMemberViaAnonymousEmail", "ContacteBayMemberViaAnonymousEmail"),
    ("ContacteBayMemberViaCommunityLink", "ContacteBayMemberViaCommunityLink"),
    ("ContactMyBidder", "ContactMyBidder"),
    ("ContactTransactionPartner", "ContactTransactionPartner"),
    ("ResponseToASQQuestion", "ResponseToASQQuestion"),
    ("ResponseToContacteBayMember", "ResponseToContacteBayMember"),
)

QuestionTypeEnum = Choices(
    ("CustomCode", "CustomCode"),
    ("CustomizedSubject", "CustomizedSubject"),
    ("General", "General"),
    ("MultipleItemShipping", "MultipleItemShipping"),
    ("None", "None"),
    ("Payment", "Payment"),
    ("Shipping", "Shipping"),
)
