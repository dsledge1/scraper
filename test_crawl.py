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

if __name__ == "__main__":
    unittest.main()