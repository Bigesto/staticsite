import unittest
import re

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_images, split_nodes_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node different", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "URL")
        self.assertNotEqual(node, node2)

    def test_assetis(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertIsNone(node.url)
        self.assertNotEqual(node.text_type, TextType.IMAGE)

    def test_eq3(self):
        node = text_node_to_html_node(TextNode(text="Hello, world!", text_type=TextType.NORMAL_TEXT))
        node2 = text_node_to_html_node(TextNode(text="Hello, world!", text_type=TextType.NORMAL_TEXT))
        self.assertEqual(node, node2)

    def test_noteq2(self):
        node = TextNode(text="This is italic", text_type=TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node different", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_basic_execution1(self):
    # This will pass if no exceptions are raised
        try:
            node = TextNode(text="This is italic", text_type=TextType.ITALIC_TEXT)
            text_node_to_html_node(node)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
    
    def test_basic_execution2(self):
    # This will pass if no exceptions are raised
        try:
            node = TextNode(text="print('Hello, world!')", text_type=TextType.CODE_TEXT)
            text_node_to_html_node(node)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
    
    def test_basic_execution3(self):
    # This will pass if no exceptions are raised
        try:
            node = TextNode(text="An example image", text_type=TextType.IMAGE, url="http://example.com/image.png")
            text_node_to_html_node(node)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")

    def test_unsupported_type(self):
        with self.assertRaises(Exception):
            node = TextNode("Unsupported type test", None) # Assuming None is not in TextType
            text_node_to_html_node(node)

    def test_link_node(self):
        node = TextNode("Visit Boot.dev", TextType.LINK, url="http://boot.dev")
        html_node = text_node_to_html_node(node)
        # Ensure the properties are set correctly, adjust as needed for your HTMLNode implementation
        self.assertEqual(html_node.tag, "a")

    def test_image_node(self):
        node = TextNode(text="An example image", text_type=TextType.IMAGE, url="http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")

    def test_special_characters(self):
        node = TextNode("Text with punctuation!?#", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "Text with punctuation!?#") # Adjust based on HTMLNode implementation
    
    def test_split_base_function(self):
        try:
            node = TextNode("This is **bold**", TextType.NORMAL_TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        except Exception as e:
            self.fail(f"function raised an unexpected exception: {e}")
    
    def test_split_multiple_delimiters(self):
            node = TextNode("Here is a **bold** word and a `code block`", TextType.NORMAL_TEXT)
            intermediate_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
            final_nodes = split_nodes_delimiter(intermediate_nodes, "`", TextType.CODE_TEXT)
            # Expected result list
            expected_nodes = [
                TextNode("Here is a ", TextType.NORMAL_TEXT),
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" word and a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode("", TextType.NORMAL_TEXT)
            ]
            # Compare actual and expected results
            for idx, (actual_node, expected_node) in enumerate(zip(final_nodes, expected_nodes)):
                assert actual_node == expected_node, f"Node at index {idx} is incorrect: got {actual_node}, expected {expected_node}"
    
    def test_split_empty_string(self):
        node = TextNode("", TextType.NORMAL_TEXT)
        # Call the function with delimiter and text_type, though they won't affect an empty string.
        final_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        expected_nodes = []  # Expected result should be an empty list
        # Compare actual and expected results
        assert final_nodes == expected_nodes, f"Result is incorrect: got {final_nodes}, expected {expected_nodes}"
    
    def test_non_text_node_unchanged(self):
        # Create a node that's already bold
        node = TextNode("this is already bold", TextType.BOLD_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        # Should return exactly the same node
        assert len(result) == 1
        assert result[0].text == "this is already bold"
        assert result[0].text_type == TextType.BOLD_TEXT

    def test_different_delimiter_on_non_text_node(self):
        # Try to split an already bold node with italic delimiters
        node = TextNode("this is bold", TextType.BOLD_TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        # Should return exactly the same node, unchanged
        assert len(result) == 1
        assert result[0].text == "this is bold"
        assert result[0].text_type == TextType.BOLD_TEXT

    def test_different_delimiter_after_bold(self):
        node = TextNode("Test text **dangerously bold** test text final", TextType.NORMAL_TEXT)
        # First process bold
        bold_result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        # Then try to split with italic delimiter
        italic_result = split_nodes_delimiter(bold_result, "*", TextType.ITALIC_TEXT)
        
        # Should have three nodes after bold processing
        expected_nodes = [
            TextNode("Test text ", TextType.NORMAL_TEXT),
            TextNode("dangerously bold", TextType.BOLD_TEXT),
            TextNode(" test text final", TextType.NORMAL_TEXT)
        ]
        
        # Verify the results
        assert len(italic_result) == len(expected_nodes)
        for actual, expected in zip(italic_result, expected_nodes):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_delimiters_at_start_and_end(self):
        node = TextNode("**bold text**", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("bold text", TextType.BOLD_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_multiple_bold_sections(self):
        node = TextNode("**bold** normal **bold again**", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" normal ", TextType.NORMAL_TEXT),
            TextNode("bold again", TextType.BOLD_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_adjacent_delimiters(self):
        node = TextNode("**bold****also bold**", TextType.NORMAL_TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode("also bold", TextType.BOLD_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
    
    def test_missing_closing_delimiter(self):
        node = TextNode("**bold text without closing", TextType.NORMAL_TEXT)
        # Should raise an exception for unclosed delimiter
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("normal ", TextType.NORMAL_TEXT),
            TextNode("already bold", TextType.BOLD_TEXT),
            TextNode(" **bold this** normal", TextType.NORMAL_TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("normal ", TextType.NORMAL_TEXT),
            TextNode("already bold", TextType.BOLD_TEXT),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("bold this", TextType.BOLD_TEXT),
            TextNode(" normal", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_complex_mixed_delimiters(self):
        nodes = [
            TextNode("Start ", TextType.NORMAL_TEXT),
            TextNode("existing bold", TextType.BOLD_TEXT),
            TextNode(" then **bold** between **more bold** end", TextType.NORMAL_TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
        expected = [
            TextNode("Start ", TextType.NORMAL_TEXT),
            TextNode("existing bold", TextType.BOLD_TEXT),
            TextNode(" then ", TextType.NORMAL_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" between ", TextType.NORMAL_TEXT),
            TextNode("more bold", TextType.BOLD_TEXT),
            TextNode(" end", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
    
    def test_incomplete_delimiter_pairs(self):
        # Single ** without closure
        node1 = TextNode("This **will break", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "**", TextType.BOLD_TEXT)
        
        # Unmatched closing **
        node2 = TextNode("This will** also break", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node2], "**", TextType.BOLD_TEXT)

    def test_mismatched_delimiter_count(self):
        # Three delimiters instead of pairs
        node = TextNode("**bold**extra**", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)

    def test_invalid_delimiters(self):
        # Missing closing delimiter
        node1 = TextNode("This **will break", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "**", TextType.BOLD_TEXT)
        
        # Unmatched closing delimiter
        node2 = TextNode("This will** also break", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node2], "**", TextType.BOLD_TEXT)

        # Delimiter in middle of bold section (this should be invalid)
        node3 = TextNode("**bold ** text**", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node3], "**", TextType.BOLD_TEXT)

    def test_split_image(self):
        node = [TextNode("Hello ![alt](image.png) World", TextType.NORMAL_TEXT)]
        result = split_nodes_images(node)
        expected = [
            TextNode("Hello ", TextType.NORMAL_TEXT),
            TextNode("alt", TextType.IMAGE, "image.png"),
            TextNode(" World", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_split_nodes_images_multiple(self):
        node = [TextNode("![one](1.png) Hello ![two](2.png) World ![three](3.png)", TextType.NORMAL_TEXT)]
        result = split_nodes_images(node)
        expected = [
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" Hello ", TextType.NORMAL_TEXT),
            TextNode("two", TextType.IMAGE, "2.png"),
            TextNode(" World ", TextType.NORMAL_TEXT),
            TextNode("three", TextType.IMAGE, "3.png")
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
    
    def test_split_nodes_links_basic(self):
        node = [TextNode("Click [here](https://boot.dev) to learn", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
            TextNode("Click ", TextType.NORMAL_TEXT),
            TextNode("here", TextType.LINK, "https://boot.dev"),
            TextNode(" to learn", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_split_nodes_links_multiple(self):
        node = [TextNode("Visit [Boot.dev](https://boot.dev) or [Google](https://google.com)", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
            TextNode("Visit ", TextType.NORMAL_TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" or ", TextType.NORMAL_TEXT),
            TextNode("Google", TextType.LINK, "https://google.com")
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
        
    def test_empty_nodes(self):
        node = [TextNode("", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)  # or split_nodes_images
        expected = []
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_mixed_links_and_text(self):
        node = [TextNode("Text [link](url) more [stuff](links) here", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
            TextNode("Text ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" more ", TextType.NORMAL_TEXT),
            TextNode("stuff", TextType.LINK, "links"),
            TextNode(" here", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type


    def test_link_at_start(self):
        node = [TextNode("[link](url) after", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" after", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type


    def test_link_at_end(self):
        node = [TextNode("before [link](url)", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
            TextNode("before ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "url")
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type


    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First [link](url1)", TextType.NORMAL_TEXT),
            TextNode("Second [link](url2)", TextType.NORMAL_TEXT)
        ]
        result = split_nodes_links(nodes)
        expected = [
            TextNode("First ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "url1"),
            TextNode("Second ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "url2")
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_mixed_links_and_images(self):
        node = [TextNode("![img](pic.jpg) then [link](url) and ![img2](pic2.jpg)", TextType.NORMAL_TEXT)]
        result1 = split_nodes_images(node)
        expected1 = [
            TextNode("img", TextType.IMAGE, "pic.jpg"),
            TextNode(" then [link](url) and ", TextType.NORMAL_TEXT),
            TextNode("img2", TextType.IMAGE, "pic2.jpg")
        ]
        # test images first
        assert len(result1) == len(expected1)
        for actual, expected in zip(result1, expected1):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
        
        # then test links on the result
        result2 = split_nodes_links(result1)
        expected2 = [
            TextNode("img", TextType.IMAGE, "pic.jpg"),
            TextNode(" then ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode("img2", TextType.IMAGE, "pic2.jpg")
        ]
        assert len(result2) == len(expected2)
        for actual, expected in zip(result2, expected2):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_interleaved_links_and_images(self):
        node = [TextNode("[link](url1) ![img](pic.jpg) [link2](url2)", TextType.NORMAL_TEXT)]
        result1 = split_nodes_images(node)
        expected1 = [
            TextNode("[link](url1) ", TextType.NORMAL_TEXT),
            TextNode("img", TextType.IMAGE, "pic.jpg"),
            TextNode(" [link2](url2)", TextType.NORMAL_TEXT)
        ]
        # test images first
        assert len(result1) == len(expected1)
        for actual, expected in zip(result1, expected1):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
        
        result2 = split_nodes_links(result1)
        expected2 = [
            TextNode("link", TextType.LINK, "url1"),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("img", TextType.IMAGE, "pic.jpg"),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ]
        # test links second
        assert len(result2) == len(expected2)
        for actual, expected in zip(result2, expected2):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type


    def test_nested_brackets_in_text(self):
        node = [TextNode("[[text]] [link](url) ![img](pic.jpg)", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
        TextNode("[[text]] ", TextType.NORMAL_TEXT),
        TextNode("link", TextType.LINK, "url"),
        TextNode(" ![img](pic.jpg)", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_empty_link_parts(self):
        node = [TextNode("[](url) and [text]() and []()", TextType.NORMAL_TEXT)]
        result = split_nodes_links(node)
        expected = [
        TextNode("", TextType.LINK, "url"),
        TextNode(" and ", TextType.NORMAL_TEXT),
        TextNode("text", TextType.LINK, ""),
        TextNode(" and ", TextType.NORMAL_TEXT),
        TextNode("", TextType.LINK, "")
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_malformed_markdown(self):
        node = [TextNode("[partial link text] and ![partial image", TextType.NORMAL_TEXT)]
        result1 = split_nodes_images(node)
        result = split_nodes_links(result1)
        expected = [
        TextNode("[partial link text] and ![partial image", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_special_characters(self):
        node = [TextNode("![image with spaces](path with spaces.jpg) [link!@#$%](url?param=value&other=123)", TextType.NORMAL_TEXT)]
        result1 = split_nodes_images(node)
        result = split_nodes_links(result1)
        expected = [
        TextNode("image with spaces", TextType.IMAGE, "path with spaces.jpg"),
        TextNode(" ", TextType.NORMAL_TEXT),
        TextNode("link!@#$%", TextType.LINK, "url?param=value&other=123")
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_consecutive_elements(self):
        node = [TextNode("[link1](url1)[link2](url2)![img1](pic1)![img2](pic2)", TextType.NORMAL_TEXT)]
        result1 = split_nodes_images(node)
        expected1 = [
            TextNode("[link1](url1)[link2](url2)", TextType.NORMAL_TEXT),
            TextNode("img1", TextType.IMAGE, "pic1"),
            TextNode("img2", TextType.IMAGE, "pic2")
        ]
        assert len(result1) == len(expected1)
        for actual, expected in zip(result1, expected1):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

        result2 = split_nodes_links(result1)
        expected2 = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode("img1", TextType.IMAGE, "pic1"),
            TextNode("img2", TextType.IMAGE, "pic2")
        ]
        assert len(result2) == len(expected2)
        for actual, expected in zip(result2, expected2):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type


# When running split_nodes_images first:


# Then when running split_nodes_links on the result:

if __name__ == "__main__":
    unittest.main()