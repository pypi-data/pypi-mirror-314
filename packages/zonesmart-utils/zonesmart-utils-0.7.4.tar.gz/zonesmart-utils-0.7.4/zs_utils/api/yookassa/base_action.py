from yookassa import Configuration
from yookassa.domain.common import ResponseObject

from zs_utils.api.base_action import APIAction


class YooKassaAction(APIAction):
    description = "Взаимодействие с API Yoo Kassa"
    save_notifications = True
    api_method = None
    VALIDATE_PARAMS = True

    def __init__(self, instance=None, propagate_exception: bool = False, **kwargs):
        super().__init__(instance, propagate_exception, **kwargs)

        self.configured = False

    def copy_instance(self, instance, **kwargs) -> None:
        super().copy_instance(instance, **kwargs)

        self.user = instance.user
        self.test_mode = instance.test_mode
        self.credentials = instance.credentials

    def set_action_variables(self, **kwargs) -> None:
        super().set_action_variables(**kwargs)
        self.user = kwargs.get("user")
        self.credentials = kwargs.get("credentials")
        self.test_mode = kwargs.get("test_mode")

    @classmethod
    def clean_data(cls, data: dict):
        cleaned_data = {}
        for key, value in data.items():
            if value or type(value) in [bool, int]:
                if isinstance(value, dict):
                    cleaned_data.update({key: cls.clean_data(value)})
                else:
                    cleaned_data.update({key: value})
        return cleaned_data

    def get_params(self, **kwargs) -> dict:
        if "params" in self.required_params:
            if kwargs.get("params"):
                kwargs["params"] = self.clean_data(data=kwargs["params"])
            else:
                kwargs["params"] = {}
        return super().get_params(**kwargs)

    def configure_yookassa(self):
        if self.test_mode:
            account_id = self.credentials["test"]["account_id"]
            secret_key = self.credentials["test"]["secret_key"]
        else:
            account_id = self.credentials["production"]["account_id"]
            secret_key = self.credentials["production"]["secret_key"]

        Configuration.configure(account_id, secret_key)

        self.configured = True

    def before_request(self, **kwargs):
        super().before_request(**kwargs)

        self.configure_yookassa()

    def make_request(self, **kwargs):
        if not getattr(self, "api_method", None):
            raise NotImplementedError("Для обращения к API YooKassa необходимо задать атрибут 'api_method'.")

        assert self.configured, "Метод Configuration.configure не был вызван."

        try:
            response: ResponseObject = self.api_method(**kwargs)
        except Exception as error:
            if error.args and isinstance(error.args[0], dict):
                errors: dict = error.args[0]
                message = f'{errors["description"]}. Code: {errors["code"]}.'
                raise self.exception_class(message=message, message_dict=errors)
            else:
                raise self.exception_class(message=str(error))

        return {"results": dict(response)}
