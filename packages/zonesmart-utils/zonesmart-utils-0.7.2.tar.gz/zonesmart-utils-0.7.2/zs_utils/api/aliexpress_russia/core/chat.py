from zs_utils.api.aliexpress_russia.base_api import AliexpressRussiaAPI


class GetAliexpressMessageListAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/manage-instant-messages#heading-poluchit-soobscheniya
    """

    http_method = "GET"
    resource_method = "/api/v2/seller/chat-messages"
    allowed_params = [
        "from_message_id",
        "limit",  # max 50
    ]


class SendAliexpressMessageAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/manage-instant-messages#heading-otpravit-soobschenie
    """

    resource_method = "/api/v2/seller/new-messages"
    required_params = [
        "to_user_login_id",
        "created_at",
        "type",
        "payload",
    ]


class MarkAsReadAliexpressMessageAPI(AliexpressRussiaAPI):
    """
    https://business.aliexpress.ru/docs/manage-instant-messages#heading-prochitat-soobschenie
    """

    resource_method = "/api/v2/seller/read-messages"
    required_params = [
        "to_user_login_id",
        "created_at",
    ]
