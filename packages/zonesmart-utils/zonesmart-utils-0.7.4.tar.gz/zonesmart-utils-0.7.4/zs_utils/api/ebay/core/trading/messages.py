import datetime

from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "GetMessagesInfo",
    "GetMessageSummary",
    "GetMessageHeaderList",
    "GetMessageList",
    "SendMessage",
    "GetMemberMessageList",
    "AnswerOrderMessage",
    "MarkMessageRead",
    "MarkMessageUnread",
    "DeleteMessageList",
]


class GetMessagesInfo(EbayTradingAPI):
    """
    GetMyMessages:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/GetMyMessages.html
    """

    method_name = "GetMyMessages"

    def get_params(
        self,
        detail_level: str,
        folder_id: int = None,
        message_ids: list = [],
        days_ago: int = None,
        **kwargs,
    ):
        assert detail_level in ["ReturnHeaders", "ReturnMessages", "ReturnSummary"]
        assert folder_id in [None, "0", "1", "2", 0, 1, 2]

        if message_ids:
            assert len(message_ids) <= 10, 'Размер "message_ids" не должен превышать 10.'
            folder_id = None
            days_ago = None
        elif detail_level == "ReturnMessages":
            raise AttributeError('Необходимо задать "message_ids".')

        if days_ago:
            EndTime = datetime.datetime.now() + datetime.timedelta(minutes=1)
            StartTime = EndTime - datetime.timedelta(days=int(days_ago))
        else:
            StartTime = None
            EndTime = None

        return {
            "DetailLevel": detail_level,
            "FolderID": folder_id,
            "MessageIDs": {"MessageID": message_ids},
            "EndTime": EndTime,
            "StartTime": StartTime,
        }


class GetMessageSummary(GetMessagesInfo):
    def get_params(self, **kwargs):
        kwargs["detail_level"] = "ReturnSummary"
        kwargs["folder_id"] = None
        kwargs["message_ids"] = None
        return super().get_params(**kwargs)


class GetMessageHeaderList(GetMessagesInfo):
    def get_params(self, full_messages=False, **kwargs):
        kwargs["detail_level"] = "ReturnHeaders"
        return super().get_params(**kwargs)


class GetMessageList(GetMessagesInfo):
    def get_params(self, **kwargs):
        kwargs["detail_level"] = "ReturnMessages"
        return super().get_params(**kwargs)


class AbstractSendMessage(EbayTradingAPI):
    """
    Abstract class.
    """

    def get_params(
        self,
        message_body: str,
        parent_message_id: str,
        message_media_url: str = None,
        item_id: str = None,
        recipient_id: str = None,
        email_copy_to_sender: bool = False,
        **kwargs,
    ):
        params = {
            "MemberMessage": {
                "Body": message_body,
                "EmailCopyToSender": email_copy_to_sender,
                "ParentMessageID": parent_message_id,
                "RecipientID": recipient_id,
            },
            "ItemID": item_id,
        }

        if message_media_url:
            params["MemberMessage"]["MessageMedia"] = {
                "MediaName": "Attached media",
                "MediaURL": message_media_url,
            }

        return params


class SendMessage(AbstractSendMessage):
    """
    AddMemberMessageRTQ:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/AddMemberMessageRTQ.html
    """

    method_name = "AddMemberMessageRTQ"

    def get_params(self, display_to_public=False, **kwargs):
        if not kwargs.get("item_id", None):
            display_to_public = False
            if not kwargs.get("recipient_id", None):
                raise AttributeError('Необходимо задать "recipient_id" или "item_id"')

        params = super().get_params(**kwargs)

        params["MemberMessage"].update({"DisplayToPublic": display_to_public})
        return params


class GetMemberMessageList(EbayTradingAPI):
    """
    GetMemberMessages:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/GetMemberMessages.html
    """

    method_name = "GetMemberMessages"

    def get_params(
        self,
        message_type="All",
        message_status=None,
        item_id=None,
        sender_id=None,
        days_ago: int = None,
        **kwargs,
    ):
        if message_type not in ["All", "AskSellerQuestion"]:
            raise AttributeError('Недопустимое значение параметра "message_type"')

        params = {"MailMessageType": message_type}

        if message_status:
            if not (message_status in ["Answered", "Unanswered"]):
                raise AttributeError('Недопустимое значение параметра "message_status"')
            params.update({"MessageStatus": message_status})

        if item_id:
            params.update({"ItemID": item_id})
        elif sender_id:
            params.update({"SenderID": sender_id})
        else:
            end_creation_time = datetime.datetime.now()
            start_creation_time = end_creation_time - datetime.timedelta(days=days_ago)

            params.update(
                {
                    "EndCreationTime": end_creation_time,
                    "StartCreationTime": start_creation_time,
                }
            )

        return params


class AnswerOrderMessage(AbstractSendMessage):
    """
    AddMemberMessageAAQToPartner:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/AddMemberMessageAAQToPartner.html
    HINT: item needs to be a part of an offer
    """

    method_name = "AddMemberMessageAAQToPartner"

    question_type_enum = [
        "CustomizedSubject",
        "General",
        "MultipleItemShipping",
        "None",
        "Payment",
        "Shipping",
    ]

    def get_params(self, item_id, recipient_id, subject, question_type="None", **kwargs):
        if not (question_type in self.question_type_enum):
            raise AttributeError('Недопустимое значение параметра "question_type"')

        params = super().get_params(**kwargs)
        params["MemberMessage"].update(
            {
                "QuestionType": question_type,
                "Subject": subject,
            }
        )
        return params


class ReviseMessages(EbayTradingAPI):
    """
    ReviseMyMessages:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/ReviseMyMessages.html
    """

    method_name = "ReviseMyMessages"

    def get_params(self, message_ids: list, read: bool = None, folder_id: int = None, **kwargs):
        if read:
            folder_id = None

        return {
            "MessageIDs": {
                "MessageID": message_ids,
            },
            "Read": read,
            "FolderID": folder_id,
        }


class MarkMessageRead(ReviseMessages):
    def get_params(self, **kwargs):
        kwargs["read"] = True
        return super().get_params(**kwargs)


class MarkMessageUnread(ReviseMessages):
    def get_params(self, **kwargs):
        kwargs["read"] = False
        return super().get_params(**kwargs)


class DeleteMessageList(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/DeleteMyMessages.html
    """

    method_name = "DeleteMyMessages"

    def get_params(self, message_ids: list, **kwargs):
        return {
            "MessageIDs": {"MessageID": message_ids},
        }
