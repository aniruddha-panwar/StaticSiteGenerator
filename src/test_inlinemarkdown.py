import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)
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

    def test_extract_markdown_image_alt_text_url(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        extracted_alt_text_url = extract_markdown_images(text)
        self.assertEqual(
            extracted_alt_text_url,
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_markdown_links_anchor_text_url(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        extracted_anchor_text_url = extract_markdown_links(text)
        self.assertEqual(
            extracted_anchor_text_url,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
