import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links
)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_nodes_pass_through(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        result = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], bold_node)

    def test_no_delimiter_found(self):
        text_node = TextNode("Just a regular text", TextType.TEXT)
        result = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just a regular text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_even_number_of_delimiters_raises_error(self):
        text_node = TextNode("This is **bold** text**", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertIn("invalid markdown", str(context.exception))

    def test_valid_splitting_bold(self):
        text_node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_valid_splitting_italic(self):
        text_node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_valid_splitting_code(self):
        text_node = TextNode("Here is `code` snippet", TextType.TEXT)
        result = split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Here is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " snippet")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_formatting_passes(self):
        text = "A **bold** and _italic_ and `code` example"
        node = TextNode(text, TextType.TEXT)
        nodes = [node]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0].text, "A ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " and ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " example")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)

    def test_invalid_formatting_unclosed(self):
        text_node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertIn("invalid markdown", str(context.exception))
        

    # Extraction of Links and Images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_none(self):
        text = "No images here, just text."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "![First](http://example.com/first.png) some text ![Second](http://example.com/second.png)"
        expected = [
            ("First", "http://example.com/first.png"),
            ("Second", "http://example.com/second.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_empty_alt(self):
        text = "![](http://example.com/empty.png)"
        expected = [("", "http://example.com/empty.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Tests for extract_markdown_links
    def test_extract_markdown_links_single(self):
        text = "Here is a link: [Link text](http://example.com)"
        expected = [("Link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_none(self):
        text = "No links here, just text."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "Links: [First](http://example.com/first) and [Second](http://example.com/second)"
        expected = [
            ("First", "http://example.com/first"),
            ("Second", "http://example.com/second")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_empty_alt(self):
        text = "[](http://example.com/empty)"
        expected = [("", "http://example.com/empty")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_ignore_images(self):
        # Ensure that image markdown is not extracted as a link.
        text = "Image: ![Alt](http://example.com/image.png) and link: [Link](http://example.com/link)"
        expected = [("Link", "http://example.com/link")]
        self.assertEqual(extract_markdown_links(text), expected)
    
if __name__ == '__main__':
    unittest.main()
