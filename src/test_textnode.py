import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_creation_default_url(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_creation_with_url(self):
        node = TextNode("Click here", TextType.LINK, url="http://www.boot.dev")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "http://www.boot.dev")

    def test_repr(self):
        node = TextNode("Test", TextType.BOLD)
        expected = f"TextNode(Test, {TextType.BOLD.value}, None)"
        self.assertEqual(repr(node), expected)

    def test_eq_return_type(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)
        result = node1.__eq__(node2)
        self.assertIsInstance(result, bool)

        node3 = TextNode("World", TextType.TEXT)
        self.assertFalse(node1 == node3, "Nodes with different text should not be equal.")

    # Tests for textNodeToHTMLNode
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type_bold(self):
        # Test for TextType.BOLD should produce a LeafNode with tag "b".
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_text_type_italic(self):
        # Test for TextType.ITALIC should produce a LeafNode with tag "i".
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

    def test_text_type_code(self):
        # Test for TextType.CODE should produce a LeafNode with tag "code".
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertIsNone(html_node.props)

    def test_text_type_link(self):
        # Test for TextType.LINK should produce a LeafNode with tag "a" and proper props.
        node = TextNode("Link text", TextType.LINK)
        node.url = "http://example.com"
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "http://example.com"})

    def test_text_type_image(self):
        # Test for TextType.IMAGE should produce a LeafNode with tag "img", empty value, and proper props.
        node = TextNode("Image alt", TextType.IMAGE)
        node.url = "http://example.com/image.png"
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "Image alt"})

    def test_invalid_text_type(self):
        # Test that an invalid text type raises an Exception.
        # We can pass a string that does not match any of the cases.
        node = TextNode("Invalid", "invalid")
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Invalid text type")


if __name__ == "__main__":
    unittest.main()