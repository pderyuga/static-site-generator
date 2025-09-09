import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_bold_basic(self):
        node = TextNode("before **bold** after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("before ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_multiple_pairs(self):
        node = TextNode("a **x** b **y** c", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("x", TextType.BOLD),
            TextNode(" b ", TextType.TEXT),
            TextNode("y", TextType.BOLD),
            TextNode(" c", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_at_string_edges(self):
        node = TextNode("_start_ and _end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("start", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("end", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter_returns_text_node(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_odd_delimiter_count_raises_for_backtick(self):
        node = TextNode("broken `code", TextType.TEXT)  # one backtick only
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "closing delimeter missing")

    def test_non_text_nodes_are_passed_through_unchanged(self):
        link = TextNode("Example", TextType.LINK, url="https://example.com")
        new_nodes = split_nodes_delimiter([link], "`", TextType.CODE)
        expected = [link]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/image.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/image.png")],
            matches,
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = (
            "This is text with a link "
            "[to site one](http://www.one.com) and "
            "[to site two](http://www.two.com)"
        )
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to site one", "http://www.one.com"),
                ("to site two", "http://www.two.com"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
