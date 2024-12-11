from zs_utils.api.aliexpress.base_api import AliexpressAPI


class GetServiceTemplate(AliexpressAPI):
    resource_method = "aliexpress.postproduct.redefining.querypromisetemplatebyid"
    required_params = ["template_id"]
