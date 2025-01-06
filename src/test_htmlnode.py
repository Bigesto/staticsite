import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("b", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("b", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = HTMLNode("a", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = HTMLNode("a", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "This is the text of the node 2", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = HTMLNode("a", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "This is the text of the node", "z", {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_assetis(self):
        node = HTMLNode("a", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertIsNone(node.children)

class TestLeaftNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("b", "This is the text of the node", {"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("b", "This is the text of the node", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = LeafNode("c", "This is the text of the nodezzzz", {"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("b", "This is the text of the node", {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)
    
    def test_assetis(self):
        node = LeafNode("a", "This is the text of the node")
        self.assertIsNone(node.props)

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html_str = node.to_html()
        self.assertEqual(html_str, '<a href="https://www.google.com">Click me!</a>')
    
    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph.")
        html_str = node.to_html()
        self.assertEqual(html_str, '<p>This is a paragraph.</p>')
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just some text.")
        html_str = node.to_html()
        self.assertEqual(html_str, 'Just some text.')
    
    def test_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        node2 = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        node2 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), node2)

    def test_not_eq(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        node2 = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "JE MANGE DES ENFANTS !!"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        self.assertNotEqual(node, node2)

    def test_basic_execution1(self):
    # This will pass if no exceptions are raised
        try:
            node = ParentNode("div", [
            LeafNode("p", "Text")
            ], {"class": "container", "id": "main"})
            node.to_html()
        except Exception as e:
            self.fail(f"ParentNode raised an unexpected exception: {e}")
    
    def test_basic_execution2(self):
    # This will pass if no exceptions are raised
        try:
            node = ParentNode("div", [
            ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode("i", "Italic")
            ]),
            LeafNode("span", "Normal")
            ])
            node.to_html()
        except Exception as e:
            self.fail(f"ParentNode raised an unexpected exception: {e}")

    def test_value_error_no_tag(self):
        node = ParentNode(None, [
        LeafNode("b", "Bold"),
        LeafNode(None, "Normal"),
        LeafNode("i", "Italic")
        ])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_value_error_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_value_error_children_empty(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()
    
if __name__ == "__main__":
    unittest.main()