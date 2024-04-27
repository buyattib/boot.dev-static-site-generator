import unittest
from textnode import (
    TEXT_TYPE_BOLD,
    TEXT_TYPE_ITALIC,
    TEXT_TYPE_CODE,
    TEXT_TYPE_TEXT,
    TEXT_TYPE_IMAGE,
    TEXT_TYPE_LINK,
    TextNode,
)
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_split_delimiter(self):
        raw_node = TextNode("Testing **bold** text", TEXT_TYPE_TEXT)

        text_node1 = TextNode("Testing ", TEXT_TYPE_TEXT)
        text_node2 = TextNode("bold", TEXT_TYPE_BOLD)
        text_node3 = TextNode(" text", TEXT_TYPE_TEXT)

        raw_nodes = [text_node1, text_node2, text_node3]
        parsed_nodes = split_nodes_delimiter([raw_node], "**", TEXT_TYPE_BOLD)

        for raw, parsed in zip(raw_nodes, parsed_nodes):
            self.assertEqual(raw, parsed)

    def test_image_extraction(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_link_extraction(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TEXT_TYPE_TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TEXT_TYPE_TEXT),
            TextNode(
                "image",
                TEXT_TYPE_IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TEXT_TYPE_TEXT),
            TextNode(
                "second image",
                TEXT_TYPE_IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(result, expected)

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and done.",
            TEXT_TYPE_TEXT,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TEXT_TYPE_TEXT),
            TextNode(
                "link",
                TEXT_TYPE_LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TEXT_TYPE_TEXT),
            TextNode(
                "second link",
                TEXT_TYPE_LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode(" and done.", TEXT_TYPE_TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TEXT_TYPE_TEXT),
            TextNode("text", TEXT_TYPE_BOLD),
            TextNode(" with an ", TEXT_TYPE_TEXT),
            TextNode("italic", TEXT_TYPE_ITALIC),
            TextNode(" word and a ", TEXT_TYPE_TEXT),
            TextNode("code block", TEXT_TYPE_CODE),
            TextNode(" and an ", TEXT_TYPE_TEXT),
            TextNode(
                "image",
                TEXT_TYPE_IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TEXT_TYPE_TEXT),
            TextNode(
                "link",
                TEXT_TYPE_LINK,
                "https://boot.dev",
            ),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
