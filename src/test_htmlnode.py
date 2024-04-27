import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"style": "margin:4px"}
        node = HTMLNode("div", None, None, props)

        self.assertEqual(node.props_to_html(), ' style="margin:4px"')

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello from a p tag!", {"style": "margin:4px"})
        self.assertEqual(
            node.to_html(), '<p style="margin:4px">Hello from a p tag!</p>'
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_to_html(self):
        leaf1 = LeafNode("p", "Leaf 1")
        leaf2 = LeafNode("p", "Leaf 2")
        leaf3 = LeafNode(None, "Leaf 3")
        parent1 = ParentNode("div", [leaf2])

        children = [leaf1, parent1, leaf3]
        root = ParentNode("div", children)
        self.assertEqual(
            root.to_html(), "<div><p>Leaf 1</p><div><p>Leaf 2</p></div>Leaf 3</div>"
        )


if __name__ == "__main__":
    unittest.main()
