import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) == 2:
        print(f"starting crawl of: {sys.argv[1]}")
    print(get_html(sys.argv[1]))


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


if __name__ == "__main__":
    main()
