import os
import shutil

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from textconverter import markdown_to_html_node, extract_title

def get_static(src_path, dst_path):
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dst_item = os.path.join(dst_path, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_path)

        if os.path.isdir(src_item):
            os.mkdir(dst_item)
            get_static(src_item, dst_item)

def copy_static():
    if not os.path.exists("static"):
        raise Exception("There is no static directory.")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    get_static("static", "public")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError as e:
        print(f"Error reading template file: {e}")
        return
    
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dst_item = os.path.join(dest_dir_path, item).replace(".md", ".html")

        if os.path.isfile(src_item) and ".md" in src_item:
            with open(src_item, "r", encoding="utf-8") as file:
                content = file.read()
            print(f"Processing file: {src_item}")
            print(f"Content length: {len(content)}")
            html_content = markdown_to_html_node(content).to_html()
            title_1 = extract_title(content)
            full_html = template.replace("{{ Title }}", title_1).replace("{{ Content }}", html_content)
            
            try:
                with open(dst_item, "w", encoding="utf-8") as file:
                    file.write(full_html)
    
            except IOError as e:
                print(f"Error writing to {dst_item}: {e}")

        if os.path.isdir(src_item):
            os.makedirs(dst_item)
            generate_pages_recursive(src_item, template_path, dst_item)


# def generate_page(from_path, template_path, dest_path):
#     print(f"Generating page from {from_path} to {dest_path} using {template_path}")
#     try:
#         with open(from_path, "r", encoding="utf-8") as file:
#             content = file.read()
#     except FileNotFoundError as e:
#         print(f"Error reading markdown file: {e}")
#         return
    
#     try:
#         with open(template_path, "r", encoding="utf-8") as file:
#             template = file.read()
#     except FileNotFoundError as e:
#         print(f"Error reading template file: {e}")
#         return

#     html_content = markdown_to_html_node(content).to_html()
#     title_1 = extract_title(content)
#     print(html_content, title_1)
#     full_html = template.replace("{{ Title }}", title_1).replace("{{ Content }}", html_content)

#     dest_name = os.path.dirname(dest_path)
#     if not os.path.exists(dest_name):
#         os.makedirs(dest_name)
    
#     try:
#         with open(dest_path, "w", encoding="utf-8") as file:
#             file.write(full_html)
    
#     except IOError as e:
#         print(f"Error writing to {dest_path}: {e}")



def main():
    copy_static()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()