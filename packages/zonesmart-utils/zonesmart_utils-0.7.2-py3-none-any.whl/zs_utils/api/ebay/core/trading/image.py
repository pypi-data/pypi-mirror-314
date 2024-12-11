from zs_utils.api.ebay.base_api import EbayTradingAPI


__all__ = [
    "UploadImageToEbayByURL",
]


class UploadImageToEbayByURL(EbayTradingAPI):
    """
    Загрузка на хостинг eBay изображения по его ссылке.
    Документация: https://developer.ebay.com/devzone/xml/docs/reference/ebay/UploadSiteHostedPictures.html
    """

    method_name = "UploadSiteHostedPictures"

    def get_params(self, picture_url: str, days_to_expire: int = 5, replace_all: bool = False, **kwargs):
        assert 0 < days_to_expire < 30

        if replace_all:
            policy = "ClearAndAdd"
        else:
            policy = "Add"

        return {
            "ExternalPictureURL": picture_url,
            "ExtensionInDays": days_to_expire,
            "PictureUploadPolicy": policy,
        }
