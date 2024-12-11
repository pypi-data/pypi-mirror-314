from zs_utils.api.aliexpress.base_api import AliexpressAPI


class GetShippingTemplateListAPI(AliexpressAPI):
    resource_method = "aliexpress.freight.redefining.listfreighttemplate"


class GetShippingTemplateInfoAPI(AliexpressAPI):
    resource_method = "aliexpress.freight.redefining.getfreightsettingbytemplatequery"
    required_params = ["template_id"]
