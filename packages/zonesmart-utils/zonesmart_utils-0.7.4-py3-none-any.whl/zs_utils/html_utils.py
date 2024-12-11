from html2text import html2text
from bs4 import BeautifulSoup


def is_html(text: str) -> bool:
    return bool(BeautifulSoup(text, "html.parser").find())


def html_to_plain_text(text: str, check_if_not_html: bool = True) -> str:
    if check_if_not_html or is_html(text=text):
        return html2text(html=text)
    return text
