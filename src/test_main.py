import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_one_line(self):
        title = "# Hello world"
        self.assertEqual(extract_title(title), "Hello world")
    
    def test_no_title(self):
        title = "#Hello world"
        with self.assertRaises(Exception):
            extract_title(title)

    def test_more_linesAndSpace(self):
        title = " # Hello world\nByeBye"
        self.assertEqual(extract_title(title), "Hello world")

    def test_more_linesSecond(self):
        title = "Byebye\n# Hello world"
        self.assertEqual(extract_title(title), "Hello world")

    def test_more_linesWrong(self):
        title = "Byebye\n## Hello world"
        with self.assertRaises(Exception):
            extract_title(title)

    def test_more_linesWrongTwo(self):
        title = "Byebye\n## Hello world\n### Asdf"
        with self.assertRaises(Exception):
            extract_title(title)
    
    def test_empty_line(self):
        title = ""
        with self.assertRaises(Exception):
            extract_title(title)

if __name__ == "__main__":
    unittest.main()