from zs_utils.api.ozon.base_api import OzonAPI


# --------------------------- FBO ---------------------------
# Отправления, которые обрабатывает Озон


class OzonGetFBOShipmentListAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_GetFboPostingList
    """

    resource_method = "v2/posting/fbo/list"
    required_params = [
        "limit",
    ]
    allowed_params = ["offset", "dir", "filter", "with"]


class OzonGetFBOShipmentAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_GetFboPosting
    """

    resource_method = "v2/posting/fbo/get"
    required_params = ["posting_number"]
    allowed_params = ["translit", "with"]


# --------------------------- FBS ---------------------------
# Отправления, которые обрабатывает пользователь


class OzonGetFBSShipmentListAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_GetFbsPostingListV3
    """

    resource_method = "v3/posting/fbs/list"
    required_params = [
        "limit",
    ]
    allowed_params = ["offset", "dir", "filter", "with"]


class OzonGetFBSShipmentAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_GetFbsPostingV3
    """

    resource_method = "v3/posting/fbs/get"
    required_params = [
        "posting_number",
    ]
    allowed_params = ["with"]


class OzonCreateFBSShipmentAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_ShipFbsPostingV3
    """

    resource_method = "v4/posting/fbs/ship"
    required_params = [
        "packages",
        "posting_number",
    ]
    allowed_params = ["with"]


class OzonGetLabelAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_PostingFBSPackageLabel
    """

    resource_method = "v2/posting/fbs/package-label"
    required_params = ["posting_number"]


class OzonShipmentDeliveringAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_FbsPostingDelivering
    """

    resource_method = "v2/fbs/posting/delivering"
    required_params = ["posting_number"]


class OzonShipmentDeliveredAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_FbsPostingDelivered
    """

    resource_method = "v2/fbs/posting/delivered"
    required_params = ["posting_number"]


class OzonShipmentLastMileAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_FbsPostingLastMile
    """

    resource_method = "v2/fbs/posting/last-mile"
    required_params = ["posting_number"]


class OzonSetShipmentTrackingNumberAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_FbsPostingTrackingNumberSet
    """

    resource_method = "v2/fbs/posting/tracking-number/set"
    required_params = ["tracking_numbers"]


class OzonCancelShipmentAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_CancelFbsPosting
    """

    resource_method = "v2/posting/fbs/cancel"
    required_params = [
        "posting_number",
        "cancel_reason_id",
    ]
    allowed_params = ["cancel_reason_message"]


class OzonGetShipmentCancelReasonsAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_GetPostingFbsCancelReasonList
    """

    resource_method = "v2/posting/fbs/cancel-reason/list"


class OzonGetShipmentCancelReasonAPI(OzonAPI):
    """
    Docs: https://docs.ozon.ru/api/seller/#operation/PostingAPI_GetPostingFbsCancelReasonV1
    """

    resource_method = "v1/posting/fbs/cancel-reason"
    required_params = ["related_posting_numbers"]
