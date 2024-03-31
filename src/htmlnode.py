class HTMLNode:
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
