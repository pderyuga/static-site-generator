import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
