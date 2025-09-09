class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children=None,
        props=None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # child classes will override this method
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        html = ""
        if self.props != None and self.props != {}:
            for key, value in self.props.items():
                html += f' {key}="{value}"'
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")

        if self.tag == None:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
