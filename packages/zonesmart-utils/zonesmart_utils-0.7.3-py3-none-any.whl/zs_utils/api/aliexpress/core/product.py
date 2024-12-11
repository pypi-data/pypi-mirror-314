from zs_utils.api.aliexpress.base_api import AliexpressAPI


# PRODUCT
class CreateProductAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.product.post"
    required_params = ["post_product_request"]


class EditProductAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.product.edit"
    required_params = ["edit_product_request"]


class GetProductAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=42383&docType=2
    """

    resource_method = "aliexpress.solution.product.info.get"
    required_params = ["product_id"]


class GetProductListAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=42384&docType=2
    """

    resource_method = "aliexpress.solution.product.list.get"
    required_params = ["aeop_a_e_product_list_query"]


class GetSkuAttributeAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.sku.attribute.query"
    allowed_params = ["query_sku_attribute_info_request"]


# В доках нет
# class EditProductSkuInventoryAPI(AliexpressAPI):
#     resource_method = "aliexpress.solution.product.sku.inventory.edit"
#     required_params = ["edit_product_sku_inventory_request"]
#
#
# class EditProductSkuPriceAPI(AliexpressAPI):
#     resource_method = "aliexpress.solution.product.sku.price.edit"
#     required_params = ["edit_product_sku_price_request"]


class DeleteProductsAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.batch.product.delete"
    required_params = ["productIds"]


class UpdateBatchProductPriceAPI(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=45140&docType=2
    """

    resource_method = "aliexpress.solution.batch.product.price.update"
    required_params = ["mutiple_product_update_list"]


class UpdateBatchInventory(AliexpressAPI):
    """
    Docs: https://developers.aliexpress.com/en/doc.htm?docId=45135&docType=2
    """

    resource_method = "aliexpress.solution.batch.product.inventory.update"
    required_params = ["mutiple_product_update_list"]


class OnlineProductAPI(AliexpressAPI):
    resource_method = "aliexpress.postproduct.redefining.onlineaeproduct"
    allowed_params = ["product_ids"]


class OfflineProductAPI(AliexpressAPI):
    resource_method = "aliexpress.postproduct.redefining.offlineaeproduct"
    allowed_params = ["product_ids"]


class SubmitFeedDataAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.feed.submit"
    required_params = ["operation_type", "item_list"]


class FeedQueryAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.feed.query"
    allowed_params = ["job_id"]


class GetFeedListAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.feed.list.get"
    allowed_params = ["current_page", "data_type", "page_size", "status"]


# PRODUCT SCHEMA
class GetProductSchemaAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.product.schema.get"
    required_params = ["aliexpress_category_id"]


class PostProductBasedOnSchemaAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.schema.product.instance.post"
    required_params = ["product_instance_request"]


class UpdateProductBasedOnSchemaAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.schema.product.full.update"
    required_params = ["schema_full_update_request"]


# PRODUCT GROUP
class CreateProductGroupAPI(AliexpressAPI):
    resource_method = "aliexpress.postproduct.redefining.createproductgroup"
    allowed_params = ["name", "parent_id"]


class SetProductGroupAPI(AliexpressAPI):
    resource_method = "aliexpress.postproduct.redefining.setgroups"
    allowed_params = ["product_id", "group_ids"]


class GetProductGroupAPI(AliexpressAPI):
    resource_method = "aliexpress.product.productgroups.get"


# PRODUCT IMAGE
class UploadProductImageAPI(AliexpressAPI):
    resource_method = "aliexpress.photobank.redefining.uploadimageforsdk"
    allowed_params = ["group_id", "image_bytes", "file_name"]
