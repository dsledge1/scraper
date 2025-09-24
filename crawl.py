from urllib.parse import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup
import requests

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

def get_urls_from_html(html, base_url):
    if base_url == "":
        return []
    if html == "":
        return []
    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in ["http", "https", ""] or not parsed_base.netloc:
        raise ValueError("base_url must be a valid URL with http or https scheme and a non-empty netloc")
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        lnk = link.get('href')
        parsed = urlparse(lnk)
        if parsed.scheme not in ["http", "https", ""]:
            continue
        if lnk == "None" or lnk == "":
            continue
        else:
            if normalize_url(base_url) in parsed.netloc:
                urls.append(lnk)
            elif parsed.netloc == "":
                if parsed.path:
                    urls.append(urljoin(base_url, lnk))
    return urls

def get_images_from_html(html, base_url):
    if base_url == "":
        return []
    if html == "":
        return []
    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in ["http", "https", ""] or not parsed_base.netloc:
        raise ValueError("base_url must be a valid URL with http or https scheme and a non-empty netloc")
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        parsed = urlparse(src)
        if parsed.scheme not in ["http", "https", ""]:
            continue
        if src == "None" or src == "":
            continue
        else:
            if normalize_url(base_url) in parsed.netloc:
                images.append(src)
            elif parsed.netloc == "":
                if parsed.path:
                    images.append(urljoin(base_url, src))
    return images

def extract_page_data(html, page_url):
    data = {}
    if page_url == "" or page_url is None:
        raise ValueError("must have a valid url")
    if html == "" or html is None:
        raise ValueError("no HTML to extract")
    data["url"]=page_url
    data["h1"]=get_h1_from_html(html)
    data["first_paragraph"]=get_first_paragraph_from_html(html)
    data["outgoing_links"]=get_urls_from_html(html, page_url)
    data["image_urls"]=get_images_from_html(html, page_url)
    return data

def get_html(url):
    try:
        r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    if r.status_code >= 400:
        r.raise_for_status()
    if not r.headers['Content-Type'].startswith('text/html'):
        raise Exception("Content type is not text/html")
    return r.text

def crawl_page(base_url, current_url=None, page_data=None):
    parsed_base = urlparse(base_url)
    if current_url is None:
        current_url = base_url
    parsed_current = urlparse(current_url)
    if parsed_base.hostname != parsed_current.hostname:
        return
    norm_current_url = normalize_url(current_url)
    if norm_current_url in page_data:
        return
    r = requests.get(current_url, headers={"User-Agent": "BootCrawler/1.0"})
    print(f"Crawling: {current_url} - Status code: {r.status_code}")
    page_data[norm_current_url]=extract_page_data(r.text, current_url)
    urls = get_urls_from_html(r.text, current_url)
    for url in urls:
        crawl_page(base_url, url, page_data)
    return page_data