import re
import unittest

from textnode import extract_markdown_images, extract_markdown_link

class TestExtractionsMethods(unittest.TestCase):
    def test_basic_execution(self):
        try:
            text1 = "Here is [a link](https://example.com)"
            extract_markdown_link(text1)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
        
        try:
            text2 = "Look at this ![cute cat](https://example.com/cat.jpg)"
            extract_markdown_images(text2)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")

        try:
            text3 = "Multiple [link one](https://example1.com) and [link two](https://example2.com)"
            extract_markdown_link(text3)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
        
        try:
            text4 = "![Image with spaces](https://example.com/image.jpg) and [Link with spaces](https://example.com)"
            extract_markdown_images(text4)
            extract_markdown_link(text4)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
        
        try:
            text5 = "Mixed ![image](https://example.com/img.jpg) and [link](https://example.com) content"
            extract_markdown_images(text5)
            extract_markdown_link(text5)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
        
        try:
            text7 = "A [link with special @#$ in url](https://example.com/@user/page?id=123)"
            extract_markdown_link(text7)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")

        try:
            text6 = "No links or images here"
            extract_markdown_link(text6)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
    
    def test_single_link(self):
        text = "Here is [a link](https://example.com)"
        expected = [("a link", "https://example.com")]
        self.assertEqual(extract_markdown_link(text), expected)
    
    def test_single_mage(self):
        text = "Look at this ![cute cat](https://example.com/cat.jpg)"
        expected = [("cute cat", "https://example.com/cat.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_links(self):
        text = "Multiple [link one](https://example1.com) and [link two](https://example2.com)"
        expected = [("link one", "https://example1.com"), ("link two", "https://example2.com")]
        self.assertEqual(extract_markdown_link(text), expected)
    
    def test_complex1(self):
        text = "![Image with spaces](https://example.com/image.jpg) and [Link with spaces](https://example.com)"
        expected_images = [("Image with spaces", "https://example.com/image.jpg")]
        expected_links = [("Link with spaces", "https://example.com")]
        self.assertEqual(extract_markdown_link(text), expected_links)
        self.assertEqual(extract_markdown_images(text), expected_images)

    def test_complex2(self):
        text = "Mixed ![image](https://example.com/img.jpg) and [link](https://example.com) content"
        expected_images = [("image", "https://example.com/img.jpg")]
        expected_links = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_link(text), expected_links)
        self.assertEqual(extract_markdown_images(text), expected_images)

    def test_missing(self):
        text = "No links or images here"
        expected_images = []
        expected_links = []
        self.assertEqual(extract_markdown_link(text), expected_links)
        self.assertEqual(extract_markdown_images(text), expected_images)

    def test_missing2(self):
        text = ""
        expected_images = []
        expected_links = []
        self.assertEqual(extract_markdown_link(text), expected_links)
        self.assertEqual(extract_markdown_images(text), expected_images)

    def test_complex3(self):
        text = "A [link with special @#$ in url](https://example.com/@user/page?id=123)"
        expected_links = [("link with special @#$ in url", "https://example.com/@user/page?id=123")]
        self.assertEqual(extract_markdown_link(text), expected_links)

    def test_broken(self):
        text = "Broken ![alt](url and [link](url"
        expected_images = []
        expected_links = []
        self.assertEqual(extract_markdown_link(text), expected_links)
        self.assertEqual(extract_markdown_images(text), expected_images)