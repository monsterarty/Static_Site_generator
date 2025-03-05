import unittest
from markdown_blocks import markdown_to_blocks

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

if __name__ == '__main__':
    unittest.main()