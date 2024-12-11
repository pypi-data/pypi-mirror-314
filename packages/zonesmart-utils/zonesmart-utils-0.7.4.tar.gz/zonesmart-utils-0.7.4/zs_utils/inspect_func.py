import inspect


__all__ = [
    "get_params_for_func",
    "call_func_with_filtered_params",
]


def _get_func_params(func) -> dict:
    """
    Получение информации о принимаемых функцией (или методом класса) func параметрах из сигнатуры.
    """

    params = {}
    for name, info in dict(inspect.signature(func).parameters).items():
        data = {"kind": info.kind.name}
        if info.default != info.empty:
            data["default"] = info.default
        params[name] = data
    return params


def get_params_for_func(func, data: dict) -> dict:
    """
    Получение параметров для вызова функции func из словаря data.
    """

    params = {"kwargs": {}}

    for param_name, info in _get_func_params(func=func).items():
        if info["kind"] == "VAR_POSITIONAL":
            continue

        if param_name in data:
            value = data[param_name]
        elif "default" in info:
            value = info["default"]
        elif info["kind"] != "VAR_KEYWORD":
            raise ValueError(f"В словаре 'data' отсутствует обязательный ключ '{param_name}'.")
        else:
            continue

        if info["kind"] == "VAR_KEYWORD":
            if not isinstance(value, dict):
                raise ValueError(f"Параметр '{param_name}' должен быть словарем.")
            params["kwargs"] = value
        else:
            params[param_name] = value

    return params


def call_func_with_filtered_params(func, data: dict):
    """
    Вызов функции func с параметрами, полученными из словаря data.
    """

    params: dict = get_params_for_func(func=func, data=data)
    params.update(params.pop("kwargs", {}))
    return func(**params)
