import inspect
from sys import modules
from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


__all__ = [
    "get_class_by_method",
    "get_func_path",
    "get_class_method_path",
    "get_callable_path",
    "import_object",
    "import_object_by_path",
    "import_class_attr",
    "import_class_attr_by_path",
]


def get_class_by_method(method):
    """
    Получения класса по его методу
    """

    return vars(modules[method.__module__])[method.__qualname__.split(".")[0]]


def get_func_path(func) -> str:
    """
    Получение пути функции.
    """

    return ".".join([func.__module__, func.__name__])


def get_class_method_path(method) -> str:
    """
    Получение пути метода класса.
    """

    return ".".join([method.__module__, get_class_by_method(method).__name__, method.__name__])


def get_callable_path(obj) -> str:
    if inspect.isclass(obj):
        return get_func_path(func=obj)
    elif inspect.isfunction(obj):
        if "." in obj.__qualname__:  # Статический метод класса
            return get_class_method_path(method=obj)
        else:
            return get_func_path(func=obj)
    elif inspect.ismethod(obj):
        return get_class_method_path(method=obj)
    else:
        raise ValueError(f"Неизвестный тип объекта: '{type(obj)}'")


def import_object(module_name: str, object_name: str):
    # Получение модуля
    module = import_module(module_name)

    # Получение функции модуля
    func = getattr(module, object_name, None)
    if not func:
        raise AttributeError(f"Объект '{object_name}' не найден в модуле '{module_name}'.")

    return func


def import_object_by_path(path: str):
    path_parts = path.split(".")
    return import_object(module_name=".".join(path_parts[:-1]), object_name=path_parts[-1])


def import_class_attr(module_name: str, class_name: str, attr_name: str):
    # Получение модуля
    module = import_module(module_name)

    # Получение класса
    class_obj = getattr(module, class_name, None)
    if not class_obj:
        raise AttributeError(f"Класс '{class_name}' не найден в модуле '{module_name}'.")

    # Получение метода класса
    try:
        class_method = getattr(class_obj, attr_name)
    except AttributeError:
        raise AttributeError(f"Метод '{attr_name}' не найден у класса '{class_name}'.")

    return class_method


def import_class_attr_by_path(path: str):
    path_parts = path.split(".")
    return import_class_attr(
        module_name=".".join(path_parts[:-2]),
        class_name=path_parts[-2],
        attr_name=path_parts[-1],
    )


def get_email_service():
    """
    Return the EmailService that is active in this project.
    """
    try:
        return import_string(settings.EMAIL_SERVICE)
    except ValueError:
        raise ImproperlyConfigured(
            "EMAIL_SERVICE must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "EMAIL_SERVICE refers to model '%s' that has not been installed"
            % settings.EMAIL_SERVICE
        )
