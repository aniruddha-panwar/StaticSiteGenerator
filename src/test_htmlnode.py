import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="div",
            value="Hello World",
            children=None,
            props={"class": "greeting", "href": "https://boot.dev"},
        )

        self.assertEqual(
            node.props_to_html(), ' class="greeting" href="https://boot.dev"'
        )

    def test_to_html_leafnode(self):
        tag = "p"
        text = "Hello World!"
        node = LeafNode(tag, text)
        self.assertEqual(node.to_html(), f"<{tag}>{text}</{tag}>")

    def test_to_html_leafnode_no_tag(self):
        tag = None
        text = "Hello, World!"
        node = LeafNode(tag=tag, value=text)
        self.assertEqual(node.to_html(), text)


if __name__ == "__main__":
    unittest.main()
