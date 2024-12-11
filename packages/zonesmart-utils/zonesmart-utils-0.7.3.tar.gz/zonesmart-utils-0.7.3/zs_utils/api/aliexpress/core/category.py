from zs_utils.api.aliexpress.base_api import AliexpressAPI


class GetCategoryTreeAPI(AliexpressAPI):
    resource_method = "aliexpress.solution.seller.category.tree.query"
    required_params = ["category_id", "filter_no_permission"]


class GetCategoryAttributesAPI(AliexpressAPI):
    resource_method = "aliexpress.category.redefining.getallchildattributesresult"
    required_params = ["cate_id"]
    allowed_params = ["parent_attrvalue_list", "locale"]


class GetCategoryInfoAPI(AliexpressAPI):
    resource_method = "aliexpress.category.redefining.getpostcategorybyid"
    required_params = ["param0"]
