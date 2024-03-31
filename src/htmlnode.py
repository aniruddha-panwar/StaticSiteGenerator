class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_list = []
        if self.props:
            props_list = [f'''{key}="{value}"''' for key, value in self.props.items()]
        return " "+" ".join(props_list)

    def __repr__(self):
        return f'''{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})'''
