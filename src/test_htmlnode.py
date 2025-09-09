import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLNode(
            tag="a", value="link", children=[], props={"href": "https://ex.com"}
        )
        expected = "HTMLNode(a, link, [], {'href': 'https://ex.com'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "to_html method not implemented")

    def test_props_to_html_none_returns_empty_string(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict_returns_empty_string(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_attributes_in_order(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        expected = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_strong(self):
        node = LeafNode("strong", "Bold!")
        self.assertEqual(node.to_html(), "<strong>Bold!</strong>")

    def test_leaf_to_html_em(self):
        node = LeafNode("em", "Italic text")
        self.assertEqual(node.to_html(), "<em>Italic text</em>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "x < y && y > 0")
        self.assertEqual(node.to_html(), "<code>x < y && y > 0</code>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode(
            "a", "Example", props={"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank">Example</a>',
        )

    def test_leaf_to_html_span_with_class_and_data_attr(self):
        node = LeafNode("span", "Badge", props={"class": "badge", "data-kind": "info"})
        self.assertEqual(
            node.to_html(),
            '<span class="badge" data-kind="info">Badge</span>',
        )

    def test_leaf_to_html_tag_none_returns_value_only(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_when_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "all leaf nodes must have a value")

    def test_leaf_to_html_preserves_whitespace_in_value(self):
        node = LeafNode("pre", "  indented\nline  ")
        self.assertEqual(node.to_html(), "<pre>  indented\nline  </pre>")


if __name__ == "__main__":
    unittest.main()
