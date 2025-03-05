import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

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

if __name__ == '__main__':
    unittest.main()
