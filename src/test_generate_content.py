import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_finds_title_at_start(self):
        md = """
# My Title

Some content
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_finds_title_not_first_line(self):
        md = """
Intro text

# Real Title

More text
"""
        self.assertEqual(extract_title(md), "Real Title")

    def test_returns_first_title_only(self):
        md = """
# First Title

# Second Title
"""
        self.assertEqual(extract_title(md), "First Title")

    def test_raises_when_no_title(self):
        md = """
No headers here
"""
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "no title found")


if __name__ == "__main__":
    unittest.main()
