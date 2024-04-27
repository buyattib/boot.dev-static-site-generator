import re
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UN_LIST = "unordered_list"
BLOCK_TYPE_OR_LIST = "ordered_list"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if len(block) != 0]


def block_to_html_node(block):
    # get the type of markdown block and convert it to corresponding html node
    block_type = block_to_block_type(block)

    if block_type == BLOCK_TYPE_PARAGRAPH:
        return paragraph_block_to_p_node(block)
    if block_type == BLOCK_TYPE_HEADING:
        return heading_block_to_h_node(block)
    if block_type == BLOCK_TYPE_OR_LIST:
        return olist_block_to_ol_node(block)
    if block_type == BLOCK_TYPE_UN_LIST:
        return ulist_block_to_ul_node(block)
    if block_type == BLOCK_TYPE_CODE:
        return code_block_to_code_node(block)
    if block_type == BLOCK_TYPE_QUOTE:
        return quote_block_to_blockquote_node(block)

    raise ValueError("Invalid block type")


def block_to_block_type(block):
    lines = [line for line in block.split("\n") if len(line) != 0]

    if len(re.findall(r"#{1,6}\ \w+", block)) > 0:
        return BLOCK_TYPE_HEADING

    if block.startswith("```") and block.endswith("```"):
        return BLOCK_TYPE_CODE

    if all([line.startswith(">") for line in lines]):
        return BLOCK_TYPE_QUOTE

    if all([line.startswith("* ") for line in lines]) or all(
        [line.startswith("- ") for line in lines]
    ):
        return BLOCK_TYPE_UN_LIST

    if all(
        [
            len(re.findall(r"^\d+\.\s.+", line)) == 1 and line[0] == str(i + 1)
            for i, line in enumerate(lines)
            if len(line) != 0
        ]
    ):
        return BLOCK_TYPE_OR_LIST

    return BLOCK_TYPE_PARAGRAPH


def text_to_children(text):
    # convert text to a list of text nodes with correct text node types
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        # convert each text node to html node
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_block_to_p_node(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)


def heading_block_to_h_node(block):
    heading_type = block.count("#")
    if heading_type > 6:
        raise ValueError(f"Invalid heading level: {heading_type}")

    heading_content = block.replace(heading_type * "#" + " ", "")
    children = text_to_children(heading_content)
    return ParentNode(f"h{heading_type}", children)


def olist_block_to_ol_node(block):
    lines_content = [line[3:] for line in block.split("\n") if len(line) != 0]
    html = []
    for line in lines_content:
        children = text_to_children(line)
        html.append(ParentNode("li", children))
    return ParentNode("ol", html)


def ulist_block_to_ul_node(block):
    lines_content = [line[2:] for line in block.split("\n") if len(line) != 0]
    html = []
    for line in lines_content:
        children = text_to_children(line)
        html.append(ParentNode("li", children))
    return ParentNode("ul", html)


def code_block_to_code_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")

    text = block.replace("```", "")
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_block_to_blockquote_node(block):
    lines = []
    for line in block.split("\n"):
        if len(line) == 0:
            continue

        if not line.startswith(">"):
            raise ValueError("Invalid quote block")

        line_content = line.replace(">", "").strip()
        lines.append(line_content)

    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)
