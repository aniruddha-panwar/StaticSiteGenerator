import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_leafnode_props(self):
        tag = "a"
        text = "Click me!"
        props = {"href": "https://www.google.com"}

        props_html = ""

        for prop, prop_val in props.items():
            props_html += f' {prop}="{prop_val}"'

        node = LeafNode(tag=tag, value=text, props=props)
        self.assertEqual(node.to_html(), f"<{tag}{props_html}>{text}</{tag}>")

    def test_to_html_parentnode(self):
        tag = "p"
        children = [
            LeafNode("b", "Bold Text"),
            LeafNode(None, "Normal Text"),
            LeafNode("i", "Italic Text"),
            LeafNode(None, "Normal Text"),
        ]
        node = ParentNode(
            tag=tag,
            children=children,
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold Text</b>Normal Text<i>Italic Text</i>Normal Text</p>",
        )

    def test_to_html_parentnode_grandchildren(self):
        grandchild1 = LeafNode("b", "Grandchild1")
        grandchild2 = LeafNode("i", "Grandchild2")
        child1 = ParentNode("span", [grandchild1, grandchild2])
        child2 = LeafNode("code", "y=mx+c")
        parentnode = ParentNode("div", [child1, child2])

        self.assertEqual(
            parentnode.to_html(),
            f"<div><span><b>Grandchild1</b><i>Grandchild2</i></span><code>y=mx+c</code></div>",
        )


if __name__ == "__main__":
    unittest.main()
