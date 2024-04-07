from block_markdown import markdown_to_blocks
import unittest


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md_text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

        self.assertEqual(
            markdown_to_blocks(md_text),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_multi_newlines(self):
        md_text = """
This is **bolded** paragraph



This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


* This is a list 
* with items  
"""
        self.assertEqual(
            markdown_to_blocks(md_text),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "This is a list \n* with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
