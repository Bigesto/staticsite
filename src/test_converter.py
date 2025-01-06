import unittest
import re

from textnode import TextNode, TextType
from textconverter import text_to_textnodes, markdown_to_block, block_to_block_type

class TestTextToNodes(unittest.TestCase):
    def test_text_converter_basic(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_text_converter_basic2(self):
        # input text
        text = "No special formatting here."
        result = text_to_textnodes(text)
        expected = [
            TextNode("No special formatting here.", TextType.NORMAL_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

    def test_text_converter_raise_error(self):
        text = "This is **bold with no end and normal"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_converter_raise_error2(self):
        # input text 
        text = "Text with a single * asterisk."
        # expected result
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_converter_empty(self):
        # input text
        text = ""
        result = text_to_textnodes(text)
        expected = []  # An empty list indicating no nodes*
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type
        
    def test_text_converter_sequence(text):
        # input text
        text = "**bold**`code``code`*italic*"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT)
        ]
        assert len(result) == len(expected)
        for actual, expected in zip(result, expected):
            assert actual.text == expected.text
            assert actual.text_type == expected.text_type

class TestMdToBlocs(unittest.TestCase):
    def test_md_to_bloc_basic(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ['# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
        ]
        assert result == expected

    def test_md_to_bloc_empty2(self):
        text = """C'est juste une phrase simple"""
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ["""C'est juste une phrase simple"""]
        assert result == expected

    def test_md_to_bloc_empty(self):
        text = """"""
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = []
        assert result == expected

    def test_md_to_bloc_multiblank(self):
        text = "Block one\n\n\n\nBlock two\n\nBlock three"
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ["Block one", "Block two", "Block three"]
        assert result == expected

    def test_md_to_bloc_multiblank2(self):
        text = "\t  Block One with tabs\n\n   Block Two with spaces\t\n\nBlock Three with mix   \t"
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ["Block One with tabs", "Block Two with spaces", "Block Three with mix"]
        assert result == expected

    def test_md_to_bloc_manycharacters(self):
        text = "!!! ** @@ ## $$\n\n&&& ***()?\n\n:) ;)"
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ["!!! ** @@ ## $$", "&&& ***()?", ":) ;)"]
        assert result == expected

    def test_md_to_bloc_trailingblanks(self):
        text = "\n\n\nBlock A\n\nBlock B\n\n\n"
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ["Block A", "Block B"]
        assert result == expected

    def test_md_to_bloc_toomanyws(self):
        text = "   \n\nBlock X\n\n   \n   \nBlock Y"
        result = markdown_to_block(text)  # or 'markdown_to_block', as long as it's consistent
        expected = ["Block X", "Block Y"]
        assert result == expected

class TestBlocktoBlock(unittest.TestCase):
    def test_base_cases(self):
        heading1 = "# heading 1"
        heading2 = "# heading 2" 
        heading6 = "# heading 6"
        code = "```This is some code```"
        quote = "> This is a quote"
        quote_multiline = """> This is the first line of the quote
        > this is the second line
        """
        unordered_list = "* This is a single liner list"
        unordered_list_multiline = """- This is the first element of the list
        - This is the second
        """
        ordered_list = """1. This is the first element of this list
        2. This is the second element
        3. this is the last element
        """
        paragraph = "This is a normal paragraph with nothing special."

        result_heading1 = block_to_block_type(heading1)
        result_heading2 = block_to_block_type(heading2)
        result_heading6 = block_to_block_type(heading6)
        result_code = block_to_block_type(code)
        result_quote = block_to_block_type(quote)
        result_quote_multiline = block_to_block_type(quote_multiline)
        result_unordered_list = block_to_block_type(unordered_list)
        result_unordered_list_multiline = block_to_block_type(unordered_list_multiline)
        result_ordered_list = block_to_block_type(ordered_list)
        result_paragraph = block_to_block_type(paragraph)

        expected_heading1 = "heading"
        expected_heading2 = "heading"
        expected_heading6 = "heading"
        expected_code = "code"
        expected_quote = "quote"
        expected_quote_multiline = "quote"
        expected_unordered_list = "unordered_list"
        expected_unordered_list_multiline = "unordered_list"
        expected_ordered_list = "ordered_list"
        expected_paragraph = "paragraph"

        assert result_heading1 == expected_heading1
        assert result_heading2 == expected_heading2
        assert result_heading6 == expected_heading6
        assert result_code == expected_code
        assert result_quote == expected_quote
        assert result_quote_multiline == expected_quote_multiline
        assert result_unordered_list == expected_unordered_list
        assert result_unordered_list_multiline == expected_unordered_list_multiline
        assert result_ordered_list == expected_ordered_list
        assert result_paragraph == expected_paragraph
    
    def test_edge_cases(self):
        # Mixed format case
        assert block_to_block_type("1. First\n* Second\n2. Third") == "paragraph"
        # Out of order numbers
        assert block_to_block_type("1. First\n3. Third\n2. Second") == "paragraph"
        # Empty lines between items
        assert block_to_block_type("1. First\n\n2. Second") == "ordered_list"
        # Malformed numbers
        assert block_to_block_type("1. First\n2 Second\n3.Third") == "paragraph"
        # Valid but tricky content
        assert block_to_block_type("1. ```code```\n2. > quote") == "ordered_list"


if __name__ == "__main__":
    unittest.main()