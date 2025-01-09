from textconverter import extract_title, markdown_to_html_node

text = "![LOTR_image_artistmonkeys](/images/rivendell.png)"

def cut_in_lines(markdown):
    splitted = markdown.split("\n")
    clean_md = [line.strip() for line in splitted]
    return clean_md

html_nodes = markdown_to_html_node(text).to_html()

print(html_nodes)