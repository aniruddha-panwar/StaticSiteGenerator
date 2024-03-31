class HTMLNode:
    """
    class to represent HTML tags
    """
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Method to_html not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""

        props_html = ""

        for prop, prop_val in self.props.items():
            props_html += f' {prop}="{prop_val}"'

        return props_html

    def __repr__(self):
        return f'''{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})'''


class LeafNode(HTMLNode):
    """
    class to represent HTML tags that do not have children
    For e.g. a simple <p> tag with simple text, has no nested children
    """
    def __init__(self, tag, value, props = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        """
        Method to render the leaf node as HTML string
        """
        if self.value is None: raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value

        return f"""<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.props})"

