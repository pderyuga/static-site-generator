import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


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


class TestBlockToBlockType(unittest.TestCase):
    # --- Headings ---
    def test_heading_level_1(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)

    def test_heading_level_6(self):
        self.assertEqual(block_to_block_type("###### Deep"), BlockType.HEADING)

    def test_heading_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#Title"), BlockType.PARAGRAPH)

    def test_heading_level_7_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too deep"), BlockType.PARAGRAPH)

    # --- Code fences ---
    def test_code_fenced_block(self):
        md = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_inline_triple_backticks_is_paragraph_now(self):
        md = "```print('inline')```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_code_fence_unclosed_is_paragraph(self):
        md = "```\nprint('oops')"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Block quotes ---
    def test_quote_all_lines(self):
        md = "> line 1\n> line 2\n> line 3"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_quote_mixed_lines_is_paragraph(self):
        md = "> quote line\nnot quote"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Unordered lists ---
    def test_unordered_list_dash_space(self):
        md = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_lines_is_paragraph(self):
        md = "- item 1\nnot list"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Ordered lists ---
    def test_ordered_list_strict_sequence_ok(self):
        md = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_ordered_list_starts_at_two_is_paragraph(self):
        md = "2. two\n3. three"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_non_consecutive_is_paragraph(self):
        md = "1. one\n3. three"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_mixed_lines_is_paragraph(self):
        md = "1. one\nnot list"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    # --- Fallback ---
    def test_paragraph_default(self):
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
