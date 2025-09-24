import sys
import requests
from crawl import *

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) == 2:
        print(f"starting crawl of: {sys.argv[1]}")
    data = crawl_page(sys.argv[1], page_data={})
    print("crawl complete")
    print(f"crawled {len(data)} pages")
    for url, page_data in data.items():
        print(f"URL: {url}")
        print(f"H1: {page_data.get('h1', 'N/A')}")
        print(f"First Paragraph: {page_data.get('first_paragraph', 'N/A')}")
        print(f"Outgoing Links: {len(page_data.get('outgoing_links', []))}")
        print(f"Image URLs: {len(page_data.get('image_urls', []))}")
        print("-" * 40)




if __name__ == "__main__":
    main()
