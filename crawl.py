from urllib.parse import urlparse, urlunparse

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
    pass