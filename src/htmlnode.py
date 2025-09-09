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
