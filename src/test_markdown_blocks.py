import unittest
from markdown_blocks import (
    BlockType, 
    markdown_to_blocks, 
    block_to_block_type,
    markdown_to_html_node
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        # Test that a markdown string with no double newlines returns one block.
        md = "Only one block without extra newlines"
        expected = ["Only one block without extra newlines"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_extra_whitespace(self):
        # Test that extra leading/trailing whitespace and blank lines are removed.
        md = "   \n   Only one block with extra whitespace   \n\n   \n"
        expected = ["Only one block with extra whitespace"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_multiple_blank_lines(self):
        md = """
        First block


        
        
        Second block

        Third block
        """
        expected = [
            "First block",
            "Second block",
            "Third block"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_block_line_indentation(self):
        # Test that inner lines in a block are properly stripped.
        md = "Line one\n    Line two\n\tLine three"
        expected = ["Line one\nLine two\nLine three"]
        self.assertEqual(markdown_to_blocks(md), expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        # Blocks starting with a heading indicator should be HEADING.
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Something else"), BlockType.HEADING)

    def test_code_block(self):
        # A valid code block: first and last lines start with ```
        code = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        # Another example with more lines
        code2 = "```\nline 1\nline 2\nline 3\n```"
        self.assertEqual(block_to_block_type(code2), BlockType.CODE)

    def test_quote_valid(self):
        # A valid quote: every line begins with ">"
        quote = "> This is a quote\n> Continued quote"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_quote_invalid(self):
        # If one line does not start with ">", then it's a paragraph.
        quote_invalid = "> This is a quote\nNot a quote line"
        self.assertEqual(block_to_block_type(quote_invalid), BlockType.PARAGRAPH)

    def test_ulist_valid(self):
        # Every line starts with "- "
        ulist = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ulist), BlockType.ULIST)

    def test_ulist_invalid(self):
        # If not every line starts with "- ", return PARAGRAPH.
        ulist_invalid = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(ulist_invalid), BlockType.PARAGRAPH)

    def test_olist_valid(self):
        # Sequential ordered list: 1. then 2. then 3.
        olist = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(olist), BlockType.OLIST)

    def test_olist_invalid(self):
        # If the sequence is broken, return PARAGRAPH.
        olist_invalid = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(olist_invalid), BlockType.PARAGRAPH)

    def test_default_paragraph(self):
        # Any block that doesn't match special patterns should be PARAGRAPH.
        paragraph = "This is just a plain paragraph with no markdown formatting."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

    def test_heading_with_leading_spaces(self):
        # If there are leading spaces, block.startswith won't detect a heading.
        heading_with_spaces = "   # Heading with spaces"
        self.assertEqual(block_to_block_type(heading_with_spaces), BlockType.PARAGRAPH)

        
class TestBlockToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == '__main__':
    unittest.main()