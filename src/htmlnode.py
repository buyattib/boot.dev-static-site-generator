class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children: list, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")

        if self.children is None or type(self.children) != list:
            raise ValueError("Invalid HTML: no children")

        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
