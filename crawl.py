from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup

def normalize_url(urlstring: str) -> str:
    if not isinstance(urlstring, str):
        raise TypeError("urlstring must be a string")

    url = urlparse(urlstring)
    host = url.hostname or ""
    port = url.port

    # drop default ports
    if port and not ((url.scheme == "http" and port == 80) or (url.scheme == "https" and port == 443)):
        host = f"{host}:{port}"

    path = url.path.rstrip("/") or ""
    return f"{host}{path}"

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.h1:
        return soup.h1.string
    else:
        return ""

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.main and soup.main.p:
        return soup.main.p.string
    elif soup.p:
        return soup.p.string
    else:
        return ""
