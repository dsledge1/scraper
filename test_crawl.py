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
    
    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/path"><span>Boot.dev Path</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/path"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_mixed(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <a href="https://blog.boot.dev"><span>Boot.dev</span></a>
            <a href="/path"><span>Boot.dev Path</span></a>
            <a href="https://boogers.com/path"><span>Boogers</span></a>
            <a href="https://blog.boot.dev/boogers"><span>Boogers</span></a>
        </body></html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev", "https://blog.boot.dev/path", "https://blog.boot.dev/boogers"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><div>No links here.</div></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_empty(self):
        input_url = "https://blog.boot.dev"
        input_body = ''
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_href_None(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href=None><span>None</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_href_empty(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href=""><span>Empty</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_href_javascript(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="javascript:void(0)"><span>JavaScript Link</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_href_mailto(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="mailto:"><span>Email Link</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_href_fragment(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="#section1"><span>Fragment Link</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_bad_base_url(self):
        input_url = "ht!tp://bad_url"
        input_body = '<html><body><a href="/path"><span>Boot.dev Path</span></a></body></html>'
        with self.assertRaises(Exception):
            get_urls_from_html(input_body, input_url)

    def test_get_images_from_html(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><div>No images here.</div></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_empty(self):
        input_url = "https://blog.boot.dev"
        input_body = ''
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_src_None(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src=None alt="No Source"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_src_empty(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="" alt="Empty Source"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_bad_base_url(self):
        input_url = "ht!tp://bad_url"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        with self.assertRaises(Exception):
            get_images_from_html(input_body, input_url)

    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_h1(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple_images_and_links(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <a href="https://blog.boot.dev/link2">Link 2</a>
            <img src="/image1.jpg" alt="Image 1">
            <img src="https://blog.boot.dev/image2.jpg" alt="Image 2">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1", "https://blog.boot.dev/link2"],
            "image_urls": ["https://blog.boot.dev/image1.jpg", "https://blog.boot.dev/image2.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_paragraphs(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()