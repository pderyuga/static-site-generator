import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_simple_child(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multiple_children_and_props(self):
        parent = ParentNode(
            "div",
            [LeafNode("span", "one"), LeafNode("em", "two")],
            props={"class": "wrapper", "id": "main"},
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="wrapper" id="main"><span>one</span><em>two</em></div>',
        )

    def test_to_html_nested_list_with_inner_props(self):
        li1 = ParentNode("li", [LeafNode(None, "Item 1")])
        li2 = ParentNode(
            "li", [LeafNode("strong", "Item 2")], props={"class": "active"}
        )
        ul = ParentNode("ul", [li1, li2])
        self.assertEqual(
            ul.to_html(),
            '<ul><li>Item 1</li><li class="active"><strong>Item 2</strong></li></ul>',
        )

    def test_children_order_preserved(self):
        parent = ParentNode(
            "div", [LeafNode("span", "first"), LeafNode("span", "second")]
        )
        self.assertEqual(
            parent.to_html(),
            "<div><span>first</span><span>second</span></div>",
        )

    def test_to_html_raises_when_tag_none(self):
        parent = ParentNode(None, [LeafNode("span", "x")])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "all parent nodes must have a tag")

    def test_to_html_raises_when_tag_empty(self):
        parent = ParentNode("", [LeafNode("span", "x")])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "all parent nodes must have a tag")

    def test_to_html_raises_when_children_empty_list(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "all parent nodes must have children")

    def test_to_html_raises_when_children_none(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "all parent nodes must have children")

    def test_error_propagates_from_child(self):
        bad_child = LeafNode("p", None)  # will raise ValueError
        parent = ParentNode("div", [bad_child])
        with self.assertRaises(ValueError) as cm:
            parent.to_html()
        self.assertEqual(str(cm.exception), "all leaf nodes must have a value")

    def test_repr(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "box"})
        self.assertEqual(
            repr(parent),
            "ParentNode(div, children: [LeafNode(span, child, None)], {'class': 'box'})",
        )


if __name__ == "__main__":
    unittest.main()
