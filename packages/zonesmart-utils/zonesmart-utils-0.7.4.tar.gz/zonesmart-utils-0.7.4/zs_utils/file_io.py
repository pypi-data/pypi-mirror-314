import os
import io
import base64
import ssl
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from uuid import uuid4


__all__ = [
    "open_url_with_basic_auth",
    "get_file_by_url",
    "get_url_file_ext",
    "generate_unique_name_for_url_file",
]


def open_url_with_basic_auth(url: str, username: str, password: str):
    request = Request(url=url)
    b64auth = base64.b64encode(f"{username}:{password}".encode())
    request.add_header("Authorization", f"Basic {b64auth.decode()}")
    return urlopen(request, context=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS))


def get_file_by_url(url: str, auth_username: str = None, auth_password: str = None) -> io.BytesIO:
    file = io.BytesIO()

    if auth_username and auth_password:
        page = open_url_with_basic_auth(url=url, username=auth_username, password=auth_password)
    else:
        page = urlopen(
            url=Request(url=url, headers={"User-Agent": "Magic Browser"}),
            context=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS),
        )
    page.getcode()

    file.write(page.read())
    file.seek(0)

    return file


def get_url_file_ext(url: str) -> str:
    path = urlparse(url).path
    return os.path.splitext(path)[1]


def generate_unique_name_for_url_file(url: str) -> str:
    name = str(uuid4())

    ext = get_url_file_ext(url)
    if ext:
        name += ext

    return name
