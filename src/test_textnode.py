import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")

        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)

        self.assertNotEqual(node1, node2)

    def test_eq_false2(self):
        node1 = TextNode("This si a text node", text_type_code)
        node2 = TextNode("This is a text node", text_type_italic)

        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode(
            "This is a text node", text_type_text, "https://www.google.com"
        )
        node2 = TextNode(
            "This is a text node", text_type_text, "https://www.google.com"
        )

        self.assertEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://www.boot.dev)", repr(node1)
        )


if __name__ == "__main__":
    unittest.main()
