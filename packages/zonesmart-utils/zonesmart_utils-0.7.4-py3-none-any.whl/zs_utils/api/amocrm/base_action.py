import requests

from zs_utils.api.constants import API_ERROR_REASONS
from zs_utils.api.base_action import APIAction
from zs_utils.api.amocrm import services


class AmocrmAction(APIAction):
    description = "Взаимодествие с API amoCRM"
    VALIDATE_PARAMS = True
    CUSTOM_FIELDS_MAPPING = None

    def __init__(self, app_id: str = None, **kwargs):
        super().__init__(**kwargs)

        # ID приложения
        self.app_id = app_id
        if app_id:
            self.app = services.AmocrmService.get_amocrm_app(app_id=app_id)
        else:
            self.app = services.AmocrmService.get_default_amocrm_app()

    def get_api_class_init_params(self, **kwargs) -> dict:
        if (not self.app.access_token) or self.app.access_token_expired:
            if (not self.app.refresh_token) or self.app.refresh_token_expired:
                raise self.exception_class("Токен обновления приложения amoCRM недействителен.")
            access_token = services.AmocrmService.refresh_amocrm_access_token(app_id=self.app_id)
        else:
            access_token = self.app.access_token
        return {"access_token": access_token}

    def get_params(self, **kwargs) -> dict:
        if self.CUSTOM_FIELDS_MAPPING:
            kwargs = self.process_custom_fields(data=kwargs, fields_mapping=self.CUSTOM_FIELDS_MAPPING)

        return super().get_params(**kwargs)

    def clean_api_request_params(self, raw_params: dict) -> dict:
        params = super().clean_api_request_params(raw_params)

        if getattr(self, "api_class", None) and self.api_class.array_payload:
            params = {"array_payload": [params]}

        return params

    def get_error_message(self, results: dict, response: requests.Response) -> str:
        message = ""

        if results.get("detail"):
            message = results["detail"]
        elif results.get("title"):
            message = results["title"]

        if results.get("hint"):
            message += ". " + results["hint"]

        if results.get("validation-errors"):
            for item in results["validation-errors"]:
                if item.get("errors"):
                    for error in item["errors"]:
                        message += error["path"] + ": " + error["detail"] + ". "

        return message

    def get_error_reason(self, results: dict, response: requests.Response, error_message: str) -> API_ERROR_REASONS:
        if results and results.get("hint") and (results["hint"] == "Token has expired"):
            return API_ERROR_REASONS.invalid_token
        return super().get_error_reason(results, response, error_message)

    @staticmethod
    def process_custom_fields(data: dict, fields_mapping: dict):
        result = {"custom_fields_values": []}

        for key, value in data.items():
            if key in fields_mapping:
                if isinstance(value, list):
                    if not value:
                        continue
                    values = [{"value": item} for item in value]
                else:
                    if (value is None) or (value == ""):
                        continue
                    values = [{"value": value}]
                result["custom_fields_values"].append({"field_id": fields_mapping[key], "values": values})
            else:
                result[key] = value

        if not result["custom_fields_values"]:
            result.pop("custom_fields_values")

        return result
