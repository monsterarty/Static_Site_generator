import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
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
        text = "Image: ![Alt](http://example.com/image.png) and link: [Link](http://example.com/link)"
        expected = [("Link", "http://example.com/link")]
        self.assertEqual(extract_markdown_links(text), expected)
    
class TestSplitNodesImage(unittest.TestCase):
    def test_no_image_markdown(self):
        # If there are no image markdowns, return the original TEXT node.
        node = TextNode("No images here", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No images here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_valid_image_single(self):
        # Test valid image markdown splitting:
        # "Start text ![Alt Text](http://example.com/img.png) End text"
        input_text = "Start text ![Alt Text](http://example.com/img.png) End text"
        node = TextNode(input_text, TextType.TEXT)
        result = split_nodes_image([node])
        # Expecting three nodes:
        #   1. TEXT("Start text ")
        #   2. IMAGE("Alt Text", url "http://example.com/img.png")
        #   3. TEXT(" End text")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Start text ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Alt Text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "http://example.com/img.png")
        self.assertEqual(result[2].text, " End text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_valid_image_with_empty_preceding_text(self):
        # Test case where the image markdown is at the very start.
        input_text = "![Alt](http://example.com/img.png)After"
        node = TextNode(input_text, TextType.TEXT)
        result = split_nodes_image([node])
        # Since the text before the image is empty, don't include an empty TEXT node.
        # Expected nodes: [IMAGE("Alt", url "http://example.com/img.png"), TEXT("After")]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Alt")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "http://example.com/img.png")
        self.assertEqual(result[1].text, "After")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_invalid_image_unclosed(self):
        # Test that an unclosed image markdown raises a ValueError.
        # For example, missing the closing parenthesis:
        input_text = "Some text ![Alt](http://example.com/img.png"
        node = TextNode(input_text, TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_image([node])
        self.assertIn("invalid markdown", str(cm.exception))

    def test_non_text_node_image(self):
        # Non-TEXT nodes should be left untouched.
        node = TextNode("Some text", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

class TestSplitNodesLink(unittest.TestCase):
    def test_no_link_markdown(self):
        # If no link markdown is present, return the original TEXT node.
        node = TextNode("No link here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No link here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_valid_link_single(self):
        # Test valid link markdown splitting:
        # "Before [Link Text](http://example.com) after"
        input_text = "Before [Link Text](http://example.com) after"
        node = TextNode(input_text, TextType.TEXT)
        result = split_nodes_link([node])
        # Expected: [TEXT("Before "), LINK("Link Text", url "http://example.com"), TEXT(" after")]
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Before ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Link Text")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "http://example.com")
        self.assertEqual(result[2].text, " after")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_valid_link_with_empty_preceding_text(self):
        # Test where the link markdown is at the beginning.
        input_text = "[Link](http://example.com)After"
        node = TextNode(input_text, TextType.TEXT)
        result = split_nodes_link([node])
        # Expected: since there's no preceding text, only [LINK node, TEXT("After")]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Link")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "http://example.com")
        self.assertEqual(result[1].text, "After")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_invalid_link_unclosed(self):
        # Test that an unclosed link markdown raises a ValueError.
        # For example, missing the closing parenthesis:
        input_text = "Some text [Link Text](http://example.com"
        node = TextNode(input_text, TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_link([node])
        self.assertIn("invalid markdown", str(cm.exception))

    def test_non_text_node_link(self):
        # Non-TEXT nodes should be left unchanged.
        node = TextNode("Some text", TextType.CODE)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

class TestTextToTextNodes(unittest.TestCase):
    def test_combined_markdown(self):
        # Input text with various inline markdown elements.
        input_text = ("This is **text** with an _italic_ word and a `code block` and an "
                      "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        nodes = text_to_textnodes(input_text)

        # Expected breakdown:
        # 1. TEXT: "This is "
        # 2. BOLD: "text"
        # 3. TEXT: " with an "
        # 4. ITALIC: "italic"
        # 5. TEXT: " word and a "
        # 6. CODE: "code block"
        # 7. TEXT: " and an "
        # 8. IMAGE: "obi wan image" with url "https://i.imgur.com/fJRm4Vk.jpeg"
        # 9. TEXT: " and a "
        # 10. LINK: "link" with url "https://boot.dev"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]

        # Check that the number of nodes is as expected.
        self.assertEqual(len(nodes), len(expected), "Number of nodes does not match expected.")

        # Compare each node's properties.
        for idx, (node, exp) in enumerate(zip(nodes, expected)):
            with self.subTest(node_index=idx):
                self.assertEqual(node.text, exp.text, f"Text mismatch at index {idx}")
                self.assertEqual(node.text_type, exp.text_type, f"TextType mismatch at index {idx}")
                self.assertEqual(node.url, exp.url, f"URL mismatch at index {idx}")

if __name__ == '__main__':
    unittest.main()
