from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesNomenclatureList(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Prosmotr/paths/~1content~1v2~1get~1cards~1list/post
    """

    http_method = "POST"
    resource_method = "content/v2/get/cards/list"
    required_params = ["settings"]


class CreateWildberriesBarcodes(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Zagruzka/paths/~1content~1v2~1barcodes/post
    """

    http_method = "POST"
    resource_method = "content/v2/barcodes"
    required_params = ["count"]


class GetWildberriesFailedToUploadNomenclatureList(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Prosmotr/paths/~1content~1v2~1cards~1error~1list/get
    """

    http_method = "GET"
    resource_method = "content/v2/cards/error/list"


class CreateWildberriesNomenclature(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Zagruzka/paths/~1content~1v2~1cards~1upload/post
    """

    http_method = "POST"
    resource_method = "content/v2/cards/upload"
    required_params = ["subjectID", "variants"]


class UpdateWildberriesNomenclature(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Zagruzka/paths/~1content~1v2~1cards~1update/post
    """

    http_method = "POST"
    resource_method = "content/v2/cards/update"
    array_payload = True


class AddWildberriesNomenclaturesToCard(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Zagruzka/paths/~1content~1v2~1cards~1upload~1add/post
    """

    http_method = "POST"
    resource_method = "content/v2/cards/upload/add"
    required_params = [
        "imtID",
        "cardsToAdd",
    ]


class UpdateWildberriesNomenclatureImages(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Mediafajly/paths/~1content~1v3~1media~1save/post
    """

    http_method = "POST"
    resource_method = "content/v3/media/save"
    required_params = [
        "nmId",
        "data",
    ]


class GetWildberriesTrashListings(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Korzina/paths/~1content~1v2~1get~1cards~1trash/post
    """

    http_method = "POST"
    resource_method = "content/v2/get/cards/trash"
    allowed_params = ["settings"]


class DeleteWildberriesNomenclature(WildberriesAPI):
    """
    https://openapi.wb.ru/content/api/ru/#tag/Korzina/paths/~1content~1v2~1cards~1delete~1trash/post
    """

    http_method = "POST"
    resource_method = "content/v2/cards/delete/trash"
    allowed_params = ["nmIDs"]
