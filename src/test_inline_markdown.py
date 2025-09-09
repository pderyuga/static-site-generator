import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes
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


class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_at_start_and_between_text(self):
        node = TextNode(
            "![first](u1) middle ![second](u2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "u1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "u2"),
            ],
            new_nodes,
        )

    def test_trailing_text_after_last_image_is_preserved(self):
        node = TextNode("before ![alt](u1) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "u1"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_only_text_node(self):
        node = TextNode("![solo](u)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo", TextType.IMAGE, "u")],
            new_nodes,
        )

    def test_no_images_pass_through(self):
        node = TextNode("no images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("no images here", TextType.TEXT)], new_nodes)

    def test_non_text_nodes_are_passed_through_unchanged(self):
        link = TextNode("Example", TextType.LINK, "https://ex.com")
        new_nodes = split_nodes_image([link])
        self.assertListEqual([link], new_nodes)

    def test_processing_continues_across_multiple_nodes(self):
        nodes = [
            TextNode("no images here", TextType.TEXT),
            TextNode(" then an ![img](u)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("no images here", TextType.TEXT),
                TextNode(" then an ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "u"),
            ],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](http://www.first.com) and [another link](http://www.second.com) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://www.first.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "http://www.second.com"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


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


class TestTextToTextnode(unittest.TestCase):
    def test_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(textnodes, expected)


if __name__ == "__main__":
    unittest.main()
