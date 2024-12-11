import re


__all__ = [
    "custom_quote",
    "custom_unquote",
]


mapping = {
    ";": "a",
    "/": "b",
    "?": "c",
    ":": "d",
    "@": "e",
    "&": "f",
    "=": "g",
    "+": "h",
    "$": "i",
    ",": "j",
    "~": "k",
}


def custom_quote(value: str):
    if not value:
        return value

    def repl(matchobj):
        return f"_ZS1{mapping[matchobj.group(0)]}ZS2_"

    pattern = "[" + "".join(mapping.keys()) + "]"

    return re.sub(pattern=pattern, repl=repl, string=str(value))


def custom_unquote(value: str):
    if not value:
        return value

    def repl(matchobj):
        for key, value in mapping.items():
            if value == matchobj.group(1):
                return key
        raise ValueError()

    pattern = "_ZS1([" + "".join(mapping.values()) + "])ZS2_"

    return re.sub(pattern=pattern, repl=repl, string=str(value))
