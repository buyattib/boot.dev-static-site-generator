from textnode import (
    TextNode,
    TEXT_TYPE_BOLD,
    TEXT_TYPE_ITALIC,
    TEXT_TYPE_CODE,
    TEXT_TYPE_TEXT,
    TEXT_TYPE_IMAGE,
    TEXT_TYPE_LINK,
)
import re

BOLD_DELIMITER = "**"
ITALIC_DELIMITER = "*"
CODE_DELIMITER = "`"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if type(old_node) != TextNode or old_node.text_type != TEXT_TYPE_TEXT:
            new_list.append(old_node)
            continue

        split_list = old_node.text.split(delimiter)
        if len(split_list) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: {delimiter} should be closed")

        for i, block in enumerate(split_list):
            if len(block) == 0:
                continue

            if i % 2 == 0:
                new_list.append(TextNode(block, TEXT_TYPE_TEXT))
            else:
                new_list.append(TextNode(block, text_type))

    return new_list


def extract_markdown_images(text):
    result = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return result


def extract_markdown_links(text):
    result = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return result


def split_nodes_image(old_nodes):
    new_list = []
    for old_node in old_nodes:
        if type(old_node) != TextNode or old_node.text_type != TEXT_TYPE_TEXT:
            new_list.append(old_node)
            continue

        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_list.append(old_node)
            continue

        split_text = old_node.text
        for alt, url in matches:
            split_list = split_text.split(f"![{alt}]({url})", 1)
            if len(split_list[0]) != 0:
                new_list.append(TextNode(split_list[0], TEXT_TYPE_TEXT))

            new_list.append(TextNode(alt, TEXT_TYPE_IMAGE, url))
            split_text = split_list[1]

        if len(split_text) != 0:
            new_list.append(TextNode(split_text, TEXT_TYPE_TEXT))

    return new_list


def split_nodes_link(old_nodes):
    new_list = []
    for old_node in old_nodes:
        if type(old_node) != TextNode or old_node.text_type != TEXT_TYPE_TEXT:
            new_list.append(old_node)
            continue

        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_list.append(old_node)
            continue

        split_text = old_node.text
        for alt, url in matches:
            split_list = split_text.split(f"[{alt}]({url})", 1)
            new_list.append(TextNode(split_list[0], TEXT_TYPE_TEXT))
            new_list.append(TextNode(alt, TEXT_TYPE_LINK, url))
            split_text = split_list[1]

        if len(split_text) != 0:
            new_list.append(TextNode(split_text, TEXT_TYPE_TEXT))

    return new_list


def text_to_textnodes(text):
    new_list = [TextNode(text, TEXT_TYPE_TEXT)]
    type_delimiters = [
        (TEXT_TYPE_BOLD, BOLD_DELIMITER),
        (TEXT_TYPE_ITALIC, ITALIC_DELIMITER),
        (TEXT_TYPE_CODE, CODE_DELIMITER),
    ]
    for text_type, delimiter in type_delimiters:
        new_list = split_nodes_delimiter(new_list, delimiter, text_type)

    new_list = split_nodes_image(new_list)
    new_list = split_nodes_link(new_list)
    return new_list
