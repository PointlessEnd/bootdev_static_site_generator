import unittest
from gencontent import extract_title


class TestHTMLNode(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# Title

## subtitle

test test test test
"""
        self.assertEqual(
            extract_title(markdown),
            'Title'
        )

    def test_extract_title2(self):
        markdown = """
## Title

# Why would the title be in a middle?

test test test test
"""
        self.assertEqual(
            extract_title(markdown),
            'Why would the title be in a middle?'
        )

    def test_extract_title_exception(self):
        markdown = """
## Title

## Why would the title be in a middle?

test test test test
"""
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_exception_text(self):
        markdown = """
## Title

## Why would the title be in a middle?

test test test test
"""
        with self.assertRaises(ValueError) as ctx:
            extract_title(markdown)
        self.assertIn('no title', str(ctx.exception))