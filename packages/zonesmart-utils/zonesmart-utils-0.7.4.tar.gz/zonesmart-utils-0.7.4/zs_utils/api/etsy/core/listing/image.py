from zs_utils.api.etsy.base_api import EtsyAPI


class GetEtsyListingImageList(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingImages
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/images"
    required_params = ["shop_id", "listing_id"]


class GetEtsyListingImage(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingImage
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/images/{listing_image_id}"
    required_params = ["shop_id", "listing_id", "listing_image_id"]


class DeleteEtsyListingImage(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/deleteListingImage
    """

    http_method = "DELETE"
    resource_method = "shops/{shop_id}/listings/{listing_id}/images/{listing_image_id}"
    required_params = ["shop_id", "listing_id", "listing_image_id"]


class UploadEtsyListingImage(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/uploadListingImage
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/listings/{listing_id}/images"
    required_params = ["shop_id", "listing_id"]
    allowed_params = [
        "image",
        "listing_image_id",
        "rank",
        "overwrite",
        "is_watermarked",
    ]

    @property
    def headers(self) -> dict:
        # При наличии файла будет автоматом подставлен multipart - что нам и нужно
        headers = super().headers
        headers.pop("Content-Type")
        return headers


class GetVariationImages(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/getListingVariationImages
    """

    http_method = "GET"
    resource_method = "shops/{shop_id}/listings/{listing_id}/variation-images"
    required_params = ["shop_id", "listing_id"]


class UpdateVariationImages(EtsyAPI):
    """
    Docs:
    https://www.etsy.com/openapi/developers#operation/updateVariationImages
    """

    http_method = "POST"
    resource_method = "shops/{shop_id}/listings/{listing_id}/variation-images"
    required_params = ["shop_id", "listing_id", "variation_images"]
