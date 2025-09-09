import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        expected = "TextNode(Click here, link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_empty_text(self):
        node = TextNode("", TextType.ITALIC)
        expected = "TextNode(, italic, None)"

        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.url, None)
        self.assertEqual(repr(node), expected)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_maps_to_b_leaf(self):
        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")
        self.assertIsNone(html_node.props)

    def test_italic_maps_to_i_leaf(self):
        node = TextNode("Hi", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hi")
        self.assertIsNone(html_node.props)

    def test_code_maps_to_code_leaf(self):
        node = TextNode("x < y", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "x < y")
        self.assertIsNone(html_node.props)

    def test_link_maps_to_anchor_with_href(self):
        node = TextNode("Docs", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Docs")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Docs</a>')

    def test_image_maps_to_img_with_src_and_alt(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://cdn/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://cdn/img.png", "alt": "Alt text"}
        )

    def test_invalid_text_type_raises(self):
        node = TextNode("Oops", "bold")  # intentionally wrong type
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "text_type is not valid")


if __name__ == "__main__":
    unittest.main()
