from htmlnode import LeafNode

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return (
            self.text == node.text
            and self.text_type == node.text_type
            and self.url == node.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    text_type = text_node.text_type

    if text_type == TEXT_TYPE_TEXT:
        return LeafNode(None, text_node.text)
    elif text_type == TEXT_TYPE_BOLD:
        return LeafNode("b", text_node.text)
    elif text_type == TEXT_TYPE_ITALIC:
        return LeafNode("i", text_node.text)
    elif text_type == TEXT_TYPE_CODE:
        return LeafNode("code", text_node.text)
    elif text_type == TEXT_TYPE_LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_type == TEXT_TYPE_IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Invalid text type: {text_type}")
