import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
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

    def test_split_nodes_single_image_single(self):
        """
        Test case to check split_nodes_image when one text node has one image
        """
        anchor_text = "image1"
        img_url = "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"
        text = f"This is a text with ![{anchor_text}]({img_url}). So now what?"

        import logging

        logging.info(text)

        input_node = TextNode(
            text,
            text_type_text,
        )
        self.assertEqual(
            split_nodes_image([input_node]),
            [
                TextNode("This is a text with ", text_type_text),
                TextNode(anchor_text, text_type_image, img_url),
                TextNode(". So now what?", text_type_text),
            ],
        )

    def test_split_nodes_multiple_image_multiple(self):
        self.maxDiff = None
        anchor_texts = ["image" + str(i + 1) for i in range(3)]
        img_urls = [
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
        ]

        input_nodes = [
            TextNode(
                "The nodes after this will have images",
                text_type_text,
            ),
            TextNode(
                f"Here is an image - ![{anchor_texts[0]}]({img_urls[0]})",
                text_type_text,
            ),
            TextNode(
                f"Here is img1 -> ![{anchor_texts[1]}]({img_urls[1]}) and another -> ![{anchor_texts[2]}]({img_urls[2]})",
                text_type_text,
            ),
        ]
        self.assertEqual(
            split_nodes_image(input_nodes),
            [
                TextNode("The nodes after this will have images", text_type_text),
                TextNode("Here is an image - ", text_type_text),
                TextNode(anchor_texts[0], text_type_image, img_urls[0]),
                TextNode(
                    "Here is img1 -> ",
                    text_type_text,
                ),
                TextNode(anchor_texts[1], text_type_image, img_urls[1]),
                TextNode(" and another -> ", text_type_text),
                TextNode(anchor_texts[2], text_type_image, img_urls[2]),
            ],
        )

    def test_split_nodes_link_single(self):
        """
        Test the split_nodes_link method, with single text node input
        that contains a single link
        """
        alt_text = "link"
        url = "https://www.linkedin.com/"
        text = f"This text contains a [{alt_text}]({url}). Whoa!"
        input_node = TextNode(
            text,
            text_type_text,
        )

        self.assertEqual(
            split_nodes_link([input_node]),
            [
                TextNode(
                    "This text contains a ",
                    text_type_text,
                ),
                TextNode(alt_text, text_type_link, url),
                TextNode(". Whoa!", text_type_text),
            ],
        )

    def test_split_nodes_link_multiple(self):
        """
        Test the split_nodes_link method, with multiple text node input
        One of the text nodes contains > 1 link
        """
        alt_texts = [f"link{i+1}" for i in range(3)]
        urls = [
            "www.google.com",
            "www.linkedin.com",
            "www.youtube.com",
        ]

        text1 = f"This text contains 2 links - [{alt_texts[0]}]({urls[0]}) and [{alt_texts[1]}]({urls[1]})"
        text2 = ""
        text3 = f"But wait, there's more - [{alt_texts[2]}]({urls[2]})"
        input_nodes = [
            TextNode(
                text1,
                text_type_text,
            ),
            TextNode(
                text2,
                text_type_text,
            ),
            TextNode(
                text3,
                text_type_text,
            ),
        ]

        self.assertEqual(
            split_nodes_link(input_nodes),
            [
                TextNode("This text contains 2 links - ", text_type_text),
                TextNode(alt_texts[0], text_type_link, urls[0]),
                TextNode(" and ", text_type_text),
                TextNode(alt_texts[1], text_type_link, urls[1]),
                TextNode("", text_type_text),
                TextNode("But wait, there's more - ", text_type_text),
                TextNode(alt_texts[2], text_type_link, urls[2]),
            ],
        )

    def test_text_to_textnodes(self):
        """
        Test case to check text_to_textnodes helper
        """
        input_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            text_to_textnodes(input_text),
        )


if __name__ == "__main__":
    unittest.main()
