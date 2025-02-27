import unittest
from htmlnode import HTMLNode

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

if __name__ == '__main__':
    unittest.main()