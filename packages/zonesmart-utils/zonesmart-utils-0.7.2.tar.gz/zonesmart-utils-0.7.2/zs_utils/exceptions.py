from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler as drf_exception_handler

from zs_utils.json_utils import pretty_json


__all__ = [
    "CustomException",
    "CaptchaException",
]


class CustomException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST

    message: str = None
    messages: list = None
    message_dict: dict = None
    message_dict_key_prefix: str = None

    response = None
    response_code = None

    reason = None

    def __init__(
        self,
        message: str = None,
        *,
        instance=None,
        messages: list = None,
        message_dict: dict = None,
        message_dict_key_prefix: str = None,
        status_code=None,
        response=None,
        reason=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        attrs = dict(
            message=message,
            messages=messages,
            message_dict=message_dict,
            message_dict_key_prefix=message_dict_key_prefix,
            status_code=status_code,
            response=response,
            reason=reason,
        )

        if instance:
            if not isinstance(instance, self.__class__):
                raise ValueError(f"Параметр 'instance' должен быть экземпляром класса '{self.__class__.__name__}'.")

            for key, value in attrs.items():
                if value is None:
                    attrs[key] = getattr(instance, key)

        self.set_attributes(**attrs)

    def __str__(self):
        message = ""

        if self.message:
            message += str(self.message)
        elif self.messages:
            message += "; ".join(self.messages)

        if self.message_dict:
            message += "\n" + pretty_json(data=self.message_dict)

        if (not message) and (self.response_code):
            message = f"Code: {self.response_code}"

        return message

    def __repr__(self) -> str:
        val = ""
        if self.messages:
            val = f"messages={self.messages}"
        elif self.message:
            val = f"message={self.message}"
        if self.message_dict:
            if val:
                val += ", "
            val += f"message_dict={self.message_dict}"
        return f"{self.__class__.__name__}({val})"

    def set_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == "status_code":
                    if not value:
                        continue
                elif key == "response":
                    if value is not None:
                        for field in ["code", "status_code", "status"]:
                            if getattr(value, field, None):
                                self.response_code = getattr(value, field)
                                break
                elif key == "message_dict":
                    prefix = kwargs.get("message_dict_key_prefix")
                    if prefix:
                        value = self.add_key_prefix(data=value, prefix=prefix)

                setattr(self, key, value)

    def add_key_prefix(self, data: dict, prefix: str, connector: str = ".", safe: bool = True):
        updated_data = {}

        for key, value in data.items():
            if (not safe) or (not key.startswith(prefix)):
                updated_key = f"{prefix}{connector}{key}"
            else:
                updated_key = str(key)

            if isinstance(value, dict):
                updated_data[updated_key] = self.add_key_prefix(data=value, prefix=prefix, connector=connector)
            else:
                updated_data[updated_key] = value

        return updated_data

    def to_dict(self):
        if self.message_dict:
            data = dict(self.message_dict)
        elif self.messages:
            data = {"messages": self.messages}
        elif self.message:
            data = {"message": self.message}
        else:
            data = {"message": super().__str__()}

        return data

    def message_dict_to_str(self) -> str:
        if self.message_dict:
            return "\n".join(f"{key}: {value}" for key, value in self.message_dict.items())
        else:
            return ""

    def messages_to_str(self) -> str:
        if self.messages:
            if len(self.messages) == 1:
                return str(self.messages[0])
            else:
                return "\n".join(f"{num}) {msg}" for num, msg in enumerate(self.messages, start=1))
        else:
            return ""


class CaptchaException(CustomException):
    pass


def flatten_errors_dict(data=None, parent_string=None):
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                result.update(
                    flatten_errors_dict(
                        data=value,
                        parent_string=parent_string + "." + str(key) if parent_string else str(key),
                    )
                )
            else:
                pre_parent_string = parent_string + "." if parent_string else ""
                result[pre_parent_string + str(key)] = value
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for num, item in enumerate(data):
                    result.update(flatten_errors_dict(data=item, parent_string=f"{parent_string}.{num}"))
                break
        else:
            result[parent_string] = data

    return result


def custom_exception_handler(exc: Exception, context: dict) -> Response:
    """
    Кастомный обработчик ошибок.
    """

    if isinstance(exc, CustomException):
        if (not exc.status_code) or (not status.is_server_error(code=exc.status_code)):
            detail = {}

            if exc.message:
                detail["message"] = exc.message

            if exc.messages:
                detail["messages"] = exc.messages

            if exc.message_dict:
                detail["errors"] = exc.message_dict

            exc = ValidationError(detail=detail, code=exc.status_code)
    elif isinstance(exc, ValidationError) and isinstance(exc.detail, dict):
        exc.detail = flatten_errors_dict(data=exc.detail)
        if "errors" not in exc.detail:
            exc.detail = {"errors": exc.detail}

    # if settings.SENTRY_ENABLED:
    #     capture_sentry_exception(error=exc, user=context.get("user"))

    return drf_exception_handler(exc, context)
