import unittest
from crawl import *


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_trailing_slash(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_no_path(self):
        input_url = "https://blog.boot.dev"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev"
        self.assertEqual(actual, expected)  
        
    def test_normalize_url_no_scheme(self):
        input_url = "blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    #Empty String - Consider Exception Handling
    def test_normalize_url_empty(self):
        input_url = ""
        actual = normalize_url(input_url)
        expected = ""
        self.assertEqual(actual, expected)

    def test_normalize_url_complex(self):
        input_url = "https://blog.boot.dev/path/to/resource?query=param#fragment"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path/to/resource"
        self.assertEqual(actual, expected)

    def test_normalize_url_subdomain(self):
        input_url = "https://sub.blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "sub.blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_no_h1(self):
        input_body = '<html><body><h2>No H1 Here</h2></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_multiple_h1(self):
        input_body = '<html><body><h1>First H1</h1><h1>Second H1</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "First H1"
        self.assertEqual(actual, expected)
        
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
        
    def test_get_first_paragraph_from_html_no_main(self):
        input_body = '''<html><body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraphs(self):
        input_body = '<html><body><div>No paragraphs here.</div></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_trailing_slash(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev/"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_https(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="blog.boot.dev/"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["blog.boot.dev/"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/path"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/path"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_subpath(self):
        input_url = "https://blog.boot.dev/subpath"
        input_body = '<html><body><a href="/path"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/path"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_multiple_subpath(self):
        input_url = "https://blog.boot.dev/subpath/more"
        input_body = '<html><body><a href="/path"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/path"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_links(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <a href="/path1"><span>Link 1</span></a>
            <a href="https://blog.boot.dev/path2"><span>Link 2</span></a>
            <a href="/path3"><span>Link 3</span></a>
        </body></html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://blog.boot.dev/path1",
            "https://blog.boot.dev/path2",
            "https://blog.boot.dev/path3"
        ]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()