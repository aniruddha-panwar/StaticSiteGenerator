import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
