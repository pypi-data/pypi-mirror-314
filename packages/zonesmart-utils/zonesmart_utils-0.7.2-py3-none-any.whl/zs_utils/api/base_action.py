import logging
import requests
import simplejson
from abc import ABC
from unittest.mock import patch
from rest_framework import status
from rest_framework.exceptions import ValidationError
from zs_utils.exceptions import CustomException

from django.utils.translation import gettext as _

from zs_utils.api.base_api import BaseAPI
from zs_utils.api.utils import response_keeper, SessionWithResponseKeeper
from zs_utils.api.constants import API_ERROR_REASONS
from zs_utils.api.services import ApiRequestLogService


__all__ = [
    "APIAction",
    "APIActionError",
]


class APIActionError(CustomException):
    """
    Исключения для APIAction
    """

    pass


class APIAction(ABC):
    """
    Базовый класс экшенов.
    """

    # Атрибуты
    # ------------------------------------------------------------------------------

    # Описание
    description = "Действие с внешним API"

    # Стандартное исключение
    exception_class = APIActionError

    # Предварительные экшены
    ancestor_actions = {}

    # Сущность
    ENTITY_REQUIRED = False
    entity_model = None
    entity_name = None

    # Параметры вызова
    VALIDATE_PARAMS = False
    required_params = []
    allowed_params = []

    # Логирование
    SAVE_REQUEST_LOG = False

    # Таймаут запроса к стороннему API
    RESPONSE_TIMEOUT = 30

    # Логирование запросов (получение requests.Response)
    PATCH_REQUEST_WITH_RESPONSE_KEEPER = False
    REQUEST_PATCH_TARGET = "requests.sessions.Session"  # requests.Session для requests.request()

    # Инициализация
    # ------------------------------------------------------------------------------

    def __init__(
        self,
        instance=None,
        propagate_exception: bool = False,
        raw_results: bool = False,
        **kwargs,
    ):
        self.logger = logging.getLogger()

        self.instance = instance
        if instance:
            self.copy_instance(instance=instance)
        else:
            self.set_action_variables(**kwargs)

        self.propagate_exception = propagate_exception
        self.raw_results = raw_results

        self.validate_action_variables()

    def copy_instance(self, instance, **kwargs) -> None:
        """
        Копирование экземпляра класса instance (вынесение его атрибутов в новый экземпляр)
        """

        self.set_entity(**kwargs)
        if (not self.entity) and (self.entity_model == instance.entity_model):
            self.entity = instance.entity

            if self.entity_name:
                setattr(self, self.entity_name, self.entity)

        # Ссылка на счетчик запросов к внешнему API
        self.request_counter = instance.request_counter

    def set_action_variables(self, **kwargs) -> None:
        """
        Установка атрибутов экшена
        """
        self.set_entity(**kwargs)

        # Инициализация счетчика запросов к внешнему API
        self.request_counter = 0

    def set_entity(self, entity=None, entity_id: str = None, **kwargs) -> None:
        """
        Установка объекта в атрибут
        """
        self.entity = None

        if self.entity_name:
            if self.entity_name in kwargs:
                entity = kwargs[self.entity_name]
            if f"{self.entity_name}_id" in kwargs:
                entity_id = kwargs[f"{self.entity_name}_id"]

        if entity or entity_id:
            if not self.entity_name:
                raise ValueError("Необходимо определить атрибут 'entity_name'.")
            if not self.entity_model:
                raise ValueError("Необходимо определить атрибут 'entity_model'.")

            if entity:
                self.entity = entity
            else:
                self.entity = self.entity_model.objects.get(id=entity_id)

        if self.entity_name:
            setattr(self, self.entity_name, self.entity)

    def validate_action_variables(self) -> None:
        """
        Валидация атрибутов экземпляра
        """
        self.validate_entity()

    def validate_entity(self) -> None:
        """
        Валидация объекта
        """
        if self.entity:
            if not isinstance(self.entity, self.entity_model):
                raise ValueError(
                    f"Параметры 'entity' и '{self.entity_name}' должны быть экземплярами модели '{self.entity_model}'."
                )
        elif self.ENTITY_REQUIRED:
            raise ValueError(
                f"В конструкторе класса {self.__class__.__name__} необходимо задать один из следующих параметров: "
                f"'entity', 'entity_id', '{self.entity_name}', '{self.entity_name}_id'."
            )

    # Вывод сообщения
    # ------------------------------------------------------------------------------

    def _get_message_template(self) -> str:
        """
        Шаблон сообщения
        """
        message = self.description
        if message.endswith("."):
            message = message[:-1]
        return message

    def get_success_internal_message(self) -> str:
        return _("{message_template}: успешно выполнено.").format(message_template=self._get_message_template())

    def get_failure_internal_message(self) -> str:
        return _("{message_template}: возникла ошибка.").format(message_template=self._get_message_template())

    def get_success_message(self, objects) -> str:
        """
        Получение сообщения об успешной отработки экшена
        """

        return self.get_success_internal_message()

    def get_failure_message(self, error: Exception) -> str:
        """
        Получение сообщения об ошибке error при выполнении экшена
        """

        if isinstance(error, CustomException):
            if error.message_dict and error.message_dict.get("external_message"):
                external_message = error.message_dict["external_message"]
            else:
                external_message = error.message

            # Стандартное сообщение для известного типа ошибок
            if (not external_message) and (error.reason in API_ERROR_REASONS):
                external_message = API_ERROR_REASONS[error.reason]

            if not external_message:
                external_message = ""
        else:
            external_message = str(error)

        internal_message = self.get_failure_internal_message()
        if internal_message:
            message = internal_message + " " + external_message
        else:
            message = external_message

        return message

    # Пайплайн
    # ------------------------------------------------------------------------------

    def set_used_action(self, action_class: type["APIAction"], **kwargs) -> "APIAction":
        """
        Инициализация используемого экшена.
        """

        action = action_class(instance=self, propagate_exception=True, **kwargs)

        if not hasattr(self, "used_actions"):
            self.used_actions: list["APIAction"] = []
        self.used_actions.append(action)

        return action

    def set_used_actions(self) -> None:
        """
        Инициализация используемых экшенов.
        """

        pass

    def execute_ancestor_actions(self) -> None:
        """
        Выполнение предварительных экшенов и передача их результатов в качестве параметров текущего экшена.
        """

        for results_name, action_class in self.ancestor_actions.items():
            if not self.params.get(results_name):
                is_success, message, objects = action_class(instance=self, propagate_exception=True)(**self.params)
                self.params[results_name] = objects.get("results", objects)

    def __call__(self, **kwargs) -> tuple:
        """
        Запуск экшена (контроллер)
        """
        is_success = False
        message = None
        objects = {}

        try:
            # Инициализация используемых экшенов
            self.set_used_actions()

            # Обработка входных параметров
            self.params = self.get_params(**kwargs)

            # Действия перед началом выполнения данного экшена
            self.before_request()

            # Выполнение предварительных экшенов и передача их результатов в качестве параметров данного экшена
            self.execute_ancestor_actions()

            # Выполнение данного экшена
            objects: dict = self.run_action(**self.params)
            if not objects:
                objects = {"results": {}, "response": None}

            # Действия после успешного выполнения данного экшена
            self.success_callback(objects=objects, **self.params)
        except CustomException as error:
            response: requests.Response = error.response

            if not error.reason:
                error.reason = API_ERROR_REASONS.unknown

            is_success = False
            message: str = self.get_failure_message(error=error)
            objects = {
                "results": {},
                "errors": error,
                "error_reason": error.reason,
                "response": response,
            }

            # Действия после неудачного выполнения данного экшена
            self.failure_callback(objects)

            if self.propagate_exception:
                raise
        except ValidationError as error:  # TODO: не обрабатывать ValidationError?
            is_success = False
            message: str = self.get_failure_message(error=error)
            objects = {
                "results": {},
                "errors": error,
                "error_reason": API_ERROR_REASONS.data_validation,
                "response": None,
            }

            # Действия после неудачного выполнения данного экшена
            self.failure_callback(objects)

            if self.propagate_exception:
                raise
        else:
            is_success = True
            message = self.get_success_message(objects)

        if is_success:
            self.logger.info(message)
        else:
            self.logger.warning(message)

        return is_success, message, objects

    @classmethod
    def simple_run(cls, **kwargs) -> dict:
        """
        Вызов конструктора с propagate_exception=True, а затем вызов __call__ и возврат objects["results"].
        """

        kwargs["propagate_exception"] = True
        action = cls(**kwargs)
        return action.__call__(**kwargs)[2].get("results", {})

    # Методы, поддерживающие переопределение
    # ------------------------------------------------------------------------------

    def before_request(self, **kwargs) -> None:
        """
        Действия перед выполнением запроса
        """
        pass

    def format_success_results(self, results: dict, **kwargs) -> dict:
        """
        Форматирование результатов после успешного выполнения данного экшена.
        """

        return results

    def success_callback(self, objects: dict, **kwargs) -> None:
        """
        Действия после успешного выполнения данного экшена.
        """

        if (not self.raw_results) and isinstance(objects, dict) and ("results" in objects):
            objects["results"] = self.format_success_results(results=objects["results"], objects=objects)

    def failure_callback(self, objects: dict, **kwargs) -> None:
        """
        Действия после неудачного выполнения данного экшена.
        """

        pass

    def get_params(self, **kwargs) -> dict:
        """
        Определение параметров вызова экшена.
        """

        return kwargs

    @property
    def possible_params(self):
        """
        Возможные параметры (required_params + allowed_params)
        """
        return self.required_params + self.allowed_params + ["size", "page"]  # TODO: где нужны size и page?

    def clean_api_request_params(self, raw_params: dict) -> dict:
        """
        Валидация и отчистка параметров запроса к API
        """
        # Проверка наличия обязательных параметров
        for param in self.required_params:
            if raw_params.get(param) is None:
                raise self.exception_class(f"Обязательный параметр '{param}' не задан.")

        # Фильтрация допустимых параметров
        params = {param: raw_params[param] for param in self.possible_params if param in raw_params}

        return params

    def get_api_class_init_params(self, **kwargs) -> dict:
        """
        Получение параметров для инициализации API класса
        """
        raise NotImplementedError("Необходимо определить метод 'get_api_class_init_params'.")

    def get_api(self, **kwargs) -> BaseAPI:
        """
        Получение API класса
        """
        if not getattr(self, "api_class", None):
            raise NotImplementedError("Необходимо определить атрибут 'api_class'.")
        init_params: dict = self.get_api_class_init_params(**kwargs)
        init_params["response_timeout"] = self.RESPONSE_TIMEOUT
        return self.api_class(**init_params)

    def make_request(self, **kwargs) -> dict:
        """
        Исполнение запроса через API класс к API сервиса
        """
        self.api: BaseAPI = self.get_api(**kwargs)

        try:
            response = self.api.make_request(**kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout):
            raise self.exception_class(reason=API_ERROR_REASONS.timeout)

        results = self.get_response_results(response=response)

        return {"results": results, "response": response}

    def get_response_results(self, response: requests.Response) -> dict:
        """
        Извлечение результатов выполнения запроса из response
        """
        if response is not None:
            try:
                return response.json()
            except simplejson.JSONDecodeError:
                pass
        return {}

    def run_action(self, **kwargs) -> dict:
        """
        Запрос к API сервиса с последующей обработкой ответа
        """
        if self.VALIDATE_PARAMS:
            params = self.clean_api_request_params(raw_params=kwargs)
        else:
            params = kwargs

        # Инкрементирование счетчика запросов к API маркетплейса
        self.incr_request_counter()

        exception = None
        try:
            if self.PATCH_REQUEST_WITH_RESPONSE_KEEPER:
                with patch(self.REQUEST_PATCH_TARGET, SessionWithResponseKeeper):
                    response_data: dict = self.make_request(**params)
                # Извлекаем из декоратора сохраненный response
                response_attr = "raw_response"
                response: requests.Response = getattr(response_keeper, response_attr, None)
                if response is not None:
                    response_data["response"] = response
                    setattr(response_keeper, response_attr, None)
            else:
                response_data: dict = self.make_request(**params)
        except self.exception_class as error:
            response: requests.Response = error.response
            if response is None:
                results = {}
            else:
                results = self.get_response_results(response=response)
            if (not results) and error.message_dict:
                results = error.message_dict
            exception = error
        else:
            results: dict = response_data["results"]
            response: requests.Response = response_data.get("response")

        response_is_success: bool = self.response_is_success(results=results, response=response, exception=exception)
        if response_is_success:
            results: dict = self.format_success_response_results(results=results, response=response)
            exception = None
        else:
            error_message = self.get_error_message(results=results, response=response)
            if (not error_message) and exception:
                error_message = exception.message

            if exception is None:
                exception = self.exception_class(message=error_message, response=response)

            # Определение типа ошибки
            if not exception.reason:
                exception.reason = self.get_error_reason(
                    results=results,
                    response=response,
                    error_message=error_message,
                )

        # Сохранение лога
        if (not response_is_success) or self.SAVE_REQUEST_LOG:
            try:
                self.save_request_log(results=results, response=response)
            except Exception as error:
                self.logger.critical(f"Не удалось сохранить лог запроса к внешнему API: {str(error)}")

        if exception is not None:
            raise exception

        return {"results": results, "response": response}

    def incr_request_counter(self) -> None:
        """
        Увеличение счётчика запросов
        """
        self.request_counter += 1
        if self.instance:
            self.instance.incr_request_counter()

    def response_is_success(
        self,
        results: dict,
        response: requests.Response,
        exception: CustomException | None = None,
    ) -> bool:
        """
        Проверка, что запрос успешный
        """
        if exception is not None:
            return False
        if response is not None:
            return status.is_success(response.status_code)
        return True

    def format_success_response_results(self, results: dict, response: requests.Response) -> dict:
        """
        Форматирование данных ответа успешного запроса
        """
        return results

    def get_error_message(self, results: dict, response: requests.Response) -> str:
        """
        Получение сообщения об ошибке из ответа response или results
        """
        return ""

    def get_error_reason(self, results: dict, response: requests.Response, error_message: str) -> API_ERROR_REASONS:
        """
        Получение причины ошибки
        """

        if (response is not None) and getattr(response, "status_code", None):
            code: int = response.status_code
            if str(code).startswith("5"):
                return API_ERROR_REASONS.system
            elif code in [401, 403]:
                return API_ERROR_REASONS.invalid_token
            elif code == 404:
                return API_ERROR_REASONS.object_not_found
            elif response.status_code == 429:
                return API_ERROR_REASONS.request_limit

    def get_apirequest_log_extra_data(self) -> dict:
        return {}

    def save_request_log(self, results: dict, response: requests.Response):
        if (response is not None) and isinstance(response, requests.Response):
            ApiRequestLogService.save_api_request_log_by_response(
                response=response,
                **self.get_apirequest_log_extra_data(),
            )
