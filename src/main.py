from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    node = HTMLNode("a", "This is the text of the node", None, {"href": "https://www.google.com", "target": "_blank"})
    print(node.props_to_html())

if __name__ == "__main__":
    main()