__all__ = [
    "convert_from_nested_dict_to_plain_dict",
    "convert_from_plain_dict_to_nested_dict",
]


def convert_from_nested_dict_to_plain_dict(data=None, parent_string=None):
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                result.update(
                    convert_from_nested_dict_to_plain_dict(
                        value,
                        parent_string + "." + str(key) if parent_string else str(key),
                    )
                )
            else:
                pre_parent_string = parent_string + "." if parent_string else ""
                result[pre_parent_string + str(key)] = value

    elif isinstance(data, list):
        for key, value in enumerate(data):
            if isinstance(value, dict) or isinstance(value, list):
                result.update(
                    convert_from_nested_dict_to_plain_dict(
                        value,
                        parent_string + "[" + str(key) + "]" if parent_string else "[" + str(key) + "]",
                    )
                )
            else:
                pre_parent_string = parent_string if parent_string else ""
                result[pre_parent_string + "[" + str(key) + "]"] = value

    return result


def convert_from_plain_dict_to_nested_dict(data=None):
    if not data:
        return data

    if list(data.keys())[0].startswith("["):
        result = list()
    else:
        result = dict()

    last_key = None
    ignored_keys = []
    for key, value in data.items():
        if key in ignored_keys:
            continue
        elif key == "":
            return value
        elif key.startswith("["):
            rsb_idx = key.index("]")
            if last_key != key[1:rsb_idx]:
                last_key = key[1:rsb_idx]
                new_data = {k[rsb_idx + 1 :]: v for k, v in data.items() if k[1 : k.index("]")] == key[1:rsb_idx]}
                result.insert(
                    int(key[1:rsb_idx]),
                    convert_from_plain_dict_to_nested_dict(new_data),
                )
        elif key.startswith("."):
            if last_key != key[0]:
                last_key = key[0]
                new_data = {k[1:]: v for k, v in data.items() if k[0] == key[0]}
                result.update(convert_from_plain_dict_to_nested_dict(new_data))
        else:
            for index, char in enumerate(key):
                if char == "[" or char == ".":
                    if last_key != key[0:index]:
                        last_key = key[0:index]

                        new_data = {}
                        for k, v in data.items():
                            if k[0:index] == last_key:
                                new_data[k[index:]] = v
                                ignored_keys.append(k)

                        result[last_key] = convert_from_plain_dict_to_nested_dict(new_data)

                    break
            else:
                result[key] = value

    return result
