import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_creation_default_url(self):
        node = TextNode("Hello", TextType.NORMAL)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.NORMAL)
        self.assertIsNone(node.url)

    def test_creation_with_url(self):
        node = TextNode("Click here", TextType.LINKS, url="http://www.boot.dev")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, TextType.LINKS)
        self.assertEqual(node.url, "http://www.boot.dev")

    def test_repr(self):
        node = TextNode("Test", TextType.BOLD)
        expected = f"TextNode(Test, {TextType.BOLD.value}, None)"
        self.assertEqual(repr(node), expected)

    def test_eq_return_type(self):
        node1 = TextNode("Hello", TextType.NORMAL)
        node2 = TextNode("Hello", TextType.NORMAL)
        result = node1.__eq__(node2)
        self.assertIsInstance(result, bool)

        node3 = TextNode("World", TextType.NORMAL)
        self.assertFalse(node1 == node3, "Nodes with different text should not be equal.")


if __name__ == "__main__":
    unittest.main()