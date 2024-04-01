import unittest
from inline_markdown import split_nodes_delimiter
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
        )

    def test_delim_multi_italic(self):
        node = TextNode(
            "This is text with *italisized words* there and *here*",
            text_type_text,
        )
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with ", text_type_text),
                TextNode("italisized words", text_type_italic),
                TextNode(" there and ", text_type_text),
                TextNode("here", text_type_italic),
            ],
        )

    def test_delim_multinode_input(self):
        node1 = TextNode(
            "Find the value of `x` given `y` and `c` using `y=mx+c`",
            text_type_text,
        )
        node2 = TextNode(
            "Answer: `42`",
            text_type_text,
        )
        new_nodes = split_nodes_delimiter(
            [node1, node2],
            "`",
            text_type_code,
        )

        self.assertListEqual(
            new_nodes,
            [
                TextNode("Find the value of ", text_type_text),
                TextNode("x", text_type_code),
                TextNode(" given ", text_type_text),
                TextNode("y", text_type_code),
                TextNode(" and ", text_type_text),
                TextNode("c", text_type_code),
                TextNode(" using ", text_type_text),
                TextNode("y=mx+c", text_type_code),
                TextNode("Answer: ", text_type_text),
                TextNode("42", text_type_code),
            ],
        )


if __name__ == "__main__":
    unittest.main()
