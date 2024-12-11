from requests import Session


__all__ = [
    "SessionWithResponseKeeper",
    "response_keeper",
]


# Кастомный класс, который вешает декоратор на метод self.send
class SessionWithResponseKeeper(Session):
    def __init__(self):
        super().__init__()
        self.send = response_keeper(self.send)


# Сохраняет в себя результат вызова (мы используем для хранения response)
def response_keeper(func):
    def wrapper(*args, **kwargs):
        raw_response = func(*args, **kwargs)
        response_keeper.raw_response = raw_response
        return raw_response

    return wrapper
