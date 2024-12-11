import requests

from django.conf import settings
from django.utils.translation import gettext as _

from zs_utils.exceptions import CaptchaException


def validate_captcha(token: str, ip: str) -> None:
    resp = requests.get(
        url="https://captcha-api.yandex.ru/validate",
        params={
            "secret": settings.YANDEX_CAPTCHA_SERVER_KEY,
            "token": token,
            "ip": ip,
        },
        timeout=1,
    )
    resp.raise_for_status()

    results = resp.json()
    if results["status"] != "ok":
        raise CaptchaException(message=_("Ошибка валидации капчи: {error}").format(error=results["message"]))
