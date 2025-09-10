import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        md = "Just one paragraph."
        self.assertEqual(markdown_to_blocks(md), ["Just one paragraph."])

    def test_consecutive_blank_lines_do_not_create_empty_block(self):
        md = "para 1\n\n\n\npara 2"
        self.assertEqual(markdown_to_blocks(md), ["para 1", "para 2"])

    def test_leading_and_trailing_blank_lines(self):
        # Leading/trailing blanks become empty strings after strip()
        md = """

First paragraph

Second paragraph

"""

        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph", "Second paragraph"],
        )

    def test_inline_newlines_stay_within_block(self):
        md = "line 1\nline 2\n\nlast block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["line 1\nline 2", "last block"],
        )


if __name__ == "__main__":
    unittest.main()
