from zs_utils.api.apiship.base_api import ApishipAPI


class ApishipLoginApi(ApishipAPI):
    resource_method = "users/login"
    http_method = "POST"
    required_params = ["login", "password"]


class ApishipAutoSignUpAPI(ApishipAPI):
    resource_method = "users/autosignup"
    http_method = "POST"
    required_params = ["login", "password", "email"]
