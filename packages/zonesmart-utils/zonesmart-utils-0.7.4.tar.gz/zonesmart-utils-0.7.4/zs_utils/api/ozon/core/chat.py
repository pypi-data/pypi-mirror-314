from zs_utils.api.ozon.base_api import OzonAPI


class OzonGetChatListAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ChatAPI_ChatListV2
    """

    resource_method = "v2/chat/list"
    allowed_params = [
        "filters",
        "limit",
        "offset",
    ]


class OzonGetMessageListAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ChatAPI_ChatHistoryV2
    """

    resource_method = "v2/chat/history"
    required_params = [
        "chat_id",
    ]
    allowed_params = [
        "direction",
        "from_message_id",
        "limit",
    ]


class OzonSendFileAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ChatAPI_ChatSendFile
    """

    resource_method = "v1/chat/send/file"
    required_params = ["base64_content", "chat_id", "name"]


class OzonSendMessageAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ChatAPI_ChatSendMessage
    """

    resource_method = "v1/chat/send/message"
    required_params = [
        "chat_id",
        "text",
    ]


class OzonCreateChatAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ChatAPI_ChatStart
    """

    resource_method = "v1/chat/start"
    required_params = [
        "posting_number",
    ]


class OzonMarkAsReadAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/ChatAPI_ChatReadV2
    """

    resource_method = "v2/chat/read"
    required_params = [
        "chat_id",
        "from_message_id",
    ]
