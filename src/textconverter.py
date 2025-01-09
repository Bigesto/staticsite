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
            final_list.append(clean_bloc)
    return final_list

def block_to_block_type(block):
    lines = block_to_block_splitter(block)
    first_line = lines[0]
    if not lines:
        return "paragraph"
    if re.match(r"^#{1,6} ", first_line):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if all(re.match(r"^> ", line) for line in lines):
        return "quote"
    if all(line.strip().startswith(("* ", "- ")) for line in lines):
        return "unordered_list"
    if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return "ordered_list"
    
    return "paragraph"

def block_to_block_splitter(block):
    splitted = block.split("\n")
    final_list = []
    for bloc in splitted:
        clean_bloc = bloc.strip()
        if len(clean_bloc) > 0:
            final_list.append(clean_bloc)
    return final_list

def markdown_to_html_node(markdown):
    text_blocks = markdown_to_block(markdown)
    parent_node = ParentNode("div", children=[])
    for block in text_blocks:
        block_type = block_to_block_type(block)
        # clean_block = block_to_block_splitter(block)
        if block_type == "paragraph":
            p_node = ParentNode("p", children=[])
            text_nodes = text_to_textnodes(block)
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                p_node.children.append(html_node)
            parent_node.children.append(p_node)
        
        elif block_type == "heading":
            heading_level = count_hashtags(block)
            h_node = ParentNode(f"h{heading_level}", children=[])
            text_nodes = text_to_textnodes(block[heading_level+1:])
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                h_node.children.append(html_node)
            parent_node.children.append(h_node)

        elif block_type == "code":
            code_content = block.strip("`").strip()
            code_node = LeafNode("code", code_content)
            pre_node = ParentNode("pre", [code_node])
            parent_node.children.append(pre_node)
        
        elif block_type == "quote":
            q_node = ParentNode("blockquote", children=[])

            # Divise le bloc en lignes et nettoie les préfixes ">"
            lines = block.splitlines()
            clean_lines = [line.lstrip("> ").strip() for line in lines if line.strip()]

            # Reconstruit le contenu propre des blockquotes
            quote_content = " ".join(clean_lines)

            # Transforme le contenu nettoyé en nœuds de texte
            text_nodes = text_to_textnodes(quote_content)
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                q_node.children.append(html_node)

            parent_node.children.append(q_node)

        elif block_type == "unordered_list":
            ul_node = ParentNode("ul", children=[])
            lines = block.split("\n")
            for line in lines:
                li_node = ParentNode("li", children=[])
                text_nodes = text_to_textnodes(line[2:])
                for node in text_nodes:
                    html_node = text_node_to_html_node(node)
                    li_node.children.append(html_node)
                ul_node.children.append(li_node)
            parent_node.children.append(ul_node)

        elif block_type == "ordered_list":
            ol_node = ParentNode("ol", children=[])
            lines = block.split("\n")
            for line in lines:
                li_node = ParentNode("li", children=[])
                text_nodes = text_to_textnodes(line[3:])
                for node in text_nodes:
                    html_node = text_node_to_html_node(node)
                    li_node.children.append(html_node)
                ol_node.children.append(li_node)
            parent_node.children.append(ol_node)

    return parent_node

def count_hashtags(text):
    first_space = text.find(" ", 1)
    if first_space != -1:
        return text[:first_space + 1].count("#")
    return text[:7].count("#")

def extract_title(markdown):
    splitted = markdown.split("\n")
    clean_md = [line.strip() for line in splitted]
    for line in clean_md:
        if "# " in line[:2]:
            return line
        else:
            continue
    raise Exception("No header 1 in the text.")