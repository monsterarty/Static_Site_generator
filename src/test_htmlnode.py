import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNodePropsToHTML(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_single_property(self):
        node = HTMLNode(props={"class": "myclass"})
        expected = ' class="myclass"'
        self.assertEqual(node.props_to_html(), expected)

    def test_multiple_properties(self):
        props = {"class": "myclass", "id": "myid"}
        node = HTMLNode(props=props)
        expected = ' class="myclass" id="myid"'
        self.assertEqual(node.props_to_html(), expected)

    

class TestLeafNodeToHTML(unittest.TestCase):
    #LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_empty_value_raises_error(self):
        # If value is an empty string, a ValueError should be raised.
        with self.assertRaises(ValueError):
            node = LeafNode("p", "")
            node.to_html()
        # Also test when value is None.
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_empty_tag_returns_value(self):
        # If tag is an empty string, the HTML output should be just the value.
        node = LeafNode("", "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
        # Similarly, if tag is None.
        node = LeafNode(None, "Some text")
        self.assertEqual(node.to_html(), "Some text")

    def test_standard_tag_without_props(self):
        # When a tag is provided with a non-empty value and no props,
        # the output should be a normal HTML tag with the value inside.
        node = LeafNode("span", "Hello World")
        self.assertEqual(node.to_html(), "<span>Hello World</span>")

    def test_tag_with_single_prop(self):
        # When a single property is provided, it should be rendered correctly.
        node = LeafNode("a", "Link", props={"href": "http://example.com"})
        expected = '<a href="http://example.com">Link</a>'
        self.assertEqual(node.to_html(), expected)

    def test_tag_with_multiple_props(self):
        # Test with multiple properties. In Python 3.7+ the insertion order is preserved.
        props = {"class": "myclass", "id": "myid"}
        node = LeafNode("div", "Content", props=props)
        expected = '<div class="myclass" id="myid">Content</div>'
        self.assertEqual(node.to_html(), expected)

if __name__ == '__main__':
    unittest.main()