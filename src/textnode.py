import re
from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if isinstance(value, TextNode):
            return (self.text == value.text and 
                    self.text_type == value.text_type and 
                    self.url == value.url)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise Exception("Wrong Text Type.")
    
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(None, text_node.text, None)
    if text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text, None)
    if text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text, None)
    if text_node.text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text, None)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception("Text Type not implemented yet.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            final_list.append(node)
        elif node.text == "":
            continue
        else:
            splited = node.text.split(delimiter)
            if len(splited) % 2 == 0:
                raise Exception("Incorrect usage of delimiter")
            for index, part in enumerate(splited):
                if part == "":
                    continue
                elif index % 2 == 0:
                    final_list.append(TextNode(part, TextType.NORMAL_TEXT))
                elif index % 2 != 0:
                    final_list.append(TextNode(part, text_type))

    return final_list

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_link(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_images(old_nodes):
    final_list= []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            final_list.append(node)
        elif node.text == "":
            continue
        else:
            processed_image = extract_markdown_images(node.text)
            if len(processed_image) == 0:
                final_list.append(node)
            else:
                remaining_text = node.text
                for tupl in processed_image:
                    text_section = remaining_text.split(f"![{tupl[0]}]({tupl[1]})", 1)   
                    if text_section[0] != "":
                        final_list.append(TextNode(text_section[0], TextType.NORMAL_TEXT))
                    final_list.append(TextNode(tupl[0], TextType.IMAGE, tupl[1]))
                    remaining_text = text_section[1]
                if remaining_text != "":
                    final_list.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
    
    return final_list

def split_nodes_links(old_nodes):
    final_list= []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            final_list.append(node)
        elif node.text == "":
            continue
        else:
            processed_link = extract_markdown_link(node.text)
            if len(processed_link) == 0:
                final_list.append(node)
            else:
                remaining_text = node.text
                for tupl in processed_link:
                    text_section = remaining_text.split(f"[{tupl[0]}]({tupl[1]})", 1)   
                    if text_section[0] != "":
                        final_list.append(TextNode(text_section[0], TextType.NORMAL_TEXT))
                    final_list.append(TextNode(tupl[0], TextType.LINK, tupl[1]))
                    remaining_text = text_section[1]
                if remaining_text != "":
                    final_list.append(TextNode(remaining_text, TextType.NORMAL_TEXT))

    return final_list