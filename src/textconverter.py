import re
from enum import Enum

from textnode import TextType, TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_link, split_nodes_images, split_nodes_links
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_to_textnodes(text):
    subject = TextNode(text, TextType.NORMAL_TEXT)
    result1 = split_nodes_delimiter([subject], "**", TextType.BOLD_TEXT)
    result2 = split_nodes_delimiter(result1, "*", TextType.ITALIC_TEXT)
    result3 = split_nodes_delimiter(result2, "`", TextType.CODE_TEXT)
    result4 = split_nodes_images(result3)
    result5 = split_nodes_links(result4)

    return result5

def markdown_to_block(markdown):
    splitted = markdown.split("\n\n")
    final_list = []
    for bloc in splitted:
        clean_bloc = bloc.strip()
        if len(clean_bloc) > 0:
            final_list.append(clean_bloc.strip())

    return final_list

def block_to_block_type(block):
    first_six = block[:6]
    lines = block_to_block_splitter(block)
    if "# " in first_six:
        # index_space = first_six.find(" ")
        # headers = block[:index_space]
        # heading_level = headers.count("#")
        # return f"header {heading_level}"
        return "heading"
    if block[:3] == "```" and block[-3:] == "```":
        return "code"
    if all(re.match(r"^> ", line) for line in lines):
        return "quote"
    if all(re.match(r"^(\* |- )", line) for line in lines):
        return "unordered_list"
    count = 1
    for line in lines:
        match = re.match(fr"^{count}\. ", line)
        if len(line) < 3:
            return "paragraph"
        elif match:
            count += 1
    if len(lines) + 1 == count:
        return "ordered_list"
    
    return "paragraph"

def block_to_block_splitter(block):
    splitted = block.split("\n")
    final_list = []
    for bloc in splitted:
        clean_bloc = bloc.strip()
        if len(clean_bloc) > 0:
            final_list.append(clean_bloc.strip())
    return final_list