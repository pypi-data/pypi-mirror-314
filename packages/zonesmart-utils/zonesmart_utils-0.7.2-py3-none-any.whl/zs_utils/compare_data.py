import uuid
import datetime

from zs_utils.exceptions import CustomException


class DataCompareException(CustomException):
    pass


def get_dict_field_value(field: str, data: dict):
    """
    Получение значения поля 'field' словаря 'data'.
    Синтаксис аргумента 'field':
        -- символ '.' позволяет получить элемент из вложенного словаря или списка;
        -- символ ':' позволяет получить определенный элемент списка.
    Примеры работы:
        Пусть data = {'a': 1, 'b': {'d': 2}, 'c': [{'e': 3}, {'e': 4, 'f': 5}]}.
        Результат при 'field'='a': 1.
        Результат при 'field'='b': {'d': 2}.
        Результат при 'field'='b.d': 2.
        Результат при 'field'='c': [{'e': 3}, {'e': 4, 'f': 5}].
        Результат при 'field'='c.e': [3, 4].
        Результат при 'field'='c.f': [None, 5].
        Результат при 'field'='c:0': {'e': 3}.
    """

    exists = True

    for i, key in enumerate(field.split(".")):
        if ":" in key:
            key, num = key.split(":")
        else:
            num = None

        try:
            if num:
                data = data[key][int(num)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            exists = False
            data = None
            break

        if isinstance(data, list):
            field = ".".join(field.split(".")[i + 1 :])

            if field:
                if data:
                    data = [get_dict_field_value(field, item)[1] if isinstance(item, dict) else None for item in data]
                else:
                    data = None
                    exists = False

            break

    return exists, data


def dict_field_exists(*, field: str, data: dict):
    """
    Проверка, можно ли найти поле 'field' в словаре 'data'
    """

    return get_dict_field_value(field, data)[0]


def dict_fields_exist(*, fields: list, data: dict, raise_exception: bool = False):
    """
    Проверка наличия полей 'fields' в словаре 'data'
    """

    errors = {}

    for field in fields:
        if not dict_field_exists(field=field, data=data):
            errors[field] = f"Поле '{field}' не найдено."

    if errors and raise_exception:
        raise DataCompareException(message_dict=errors)

    return errors


def compare_values(a, b) -> bool:
    """
    Сравнение двух объектов на равенство.
    Допустимые типы аргументов: dict, list, str, int, float, bool, NoneType, datetime.
    """

    for value in [a, b]:
        assert type(value) in [
            dict,
            list,
            str,
            int,
            float,
            bool,
            type(None),
            datetime.datetime,
            uuid.UUID,
        ], f"Недопустимый тип {type(value)} значения '{value}'."

    values = [a, b]
    types = [type(a), type(b)]

    if dict in types:
        if isinstance(b, dict):
            # Делаем, так чтобы 'a' являлся словарем
            a, b = b, a

        if not isinstance(b, dict):
            # None и {} считаются равными
            return (b is None) and (not a)
        else:
            # Случай, когда оба значения -- словари
            if (not a) and (not b):
                # Два пустых словаря
                return True
            if set(list(a.keys())) == set(list(b.keys())):
                return all(compare_values(a[key], b[key]) for key in a.keys())
    elif types == [list, list]:
        # Списки сравниваются поэлементно
        if len(a) != len(b):
            # Равенство списков разной длины не считается возможным
            return False

        if all([(type(x) in [str, int, float]) for x in a + b]):
            try:
                # Сортировка таким образом, чтобы массив чисел сортировался так же,
                # как тот же массив с элементами, приведенными к типу str
                a = sorted(a, key=str)
                b = sorted(b, key=str)
            except TypeError:
                pass

        # Рекурсивное сравнение пар элементов списков
        return all(compare_values(a_i, b_i) for a_i, b_i in zip(a, b))
    elif (bool in types) or (None in values):
        if (int in types) or (float in types) or (str in types):
            # Равенство между bool или None с числами и строками не считается возможным
            return False
        elif (list in types) and (bool in types):
            # Равенство между bool со списком не считается возможным
            return False

        # Приведение обоих значений к bool
        return bool(a) == bool(b)

    try:
        # Попытка привести оба значения к типу float
        return float(a) == float(b)
    except (TypeError, ValueError):
        pass

    if set(types) == {uuid.UUID, str}:
        return str(a) == str(b)

    return a == b


def compare_dicts_keys(
    dict_1: dict,
    dict_2: dict,
    fields_to_compare: list = None,
    raise_exception: bool = False,
) -> dict:
    """
    Проверка одновременного существования полей из списка 'fields_to_compare'
    в словарях 'dict_1' и 'dict_2'.
    """

    errors = {}

    if fields_to_compare is None:
        fields_to_compare = set(list(dict_1.keys()) + list(dict_2.keys()))

    for field in fields_to_compare:
        dict_1_field_exists: bool = dict_field_exists(field=field, data=dict_1)
        dict_2_field_exists: bool = dict_field_exists(field=field, data=dict_2)

        if dict_1_field_exists != dict_2_field_exists:
            errors[field] = {
                "1": f"Поле '{field}' {'не ' if not dict_1_field_exists else ''} существует",
                "2": f"Поле '{field}' {'не ' if not dict_2_field_exists else ''} существует",
            }

    if errors and raise_exception:
        raise DataCompareException(message_dict=errors)

    return errors


def compare_dicts_values(
    dict_1: dict,
    dict_2: dict,
    fields_to_compare: list = None,
    raise_exception: bool = False,
) -> dict:
    """
    Сравнение значений полей из списка 'fields_to_compare' словарей 'dict_1' и 'dict_2'.
    """

    errors = {}

    if fields_to_compare is None:
        fields_to_compare = set(list(dict_1.keys()) + list(dict_2.keys()))

    for fields_pair in fields_to_compare:
        if isinstance(fields_pair, list) or isinstance(fields_pair, tuple):
            fields_pair = tuple(fields_pair)  # для хешируемости
            field_1 = fields_pair[0]
            field_2 = fields_pair[1]
        else:
            field_1 = fields_pair
            field_2 = fields_pair

        for field in [field_1, field_2]:
            if not isinstance(field, str):
                raise ValueError(f"Недопустимый тип поля: {type(field)}")

        _, value_1 = get_dict_field_value(field_1, dict_1)
        _, value_2 = get_dict_field_value(field_2, dict_2)

        equal = compare_values(value_1, value_2)
        if not equal:
            errors[fields_pair] = {
                "1": f"Значение поля '{field_1}': {value_1}",
                "2": f"Значение поля '{field_2}': {value_2}",
            }

    if errors and raise_exception:
        raise DataCompareException(message_dict=errors)

    return errors
