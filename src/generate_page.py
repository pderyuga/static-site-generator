import os
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise Exception("no title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path)
    markdown_doc = markdown_file.read()

    template_file = open(template_path)
    template_doc = template_file.read()

    markdown_html_node = markdown_to_html_node(markdown_doc)
    markdown_html = markdown_html_node.to_html()

    page_title = extract_title(markdown_doc)
    html_doc_with_title = template_doc.replace("{{ Title }}", page_title)
    html_doc = html_doc_with_title.replace("{{ Content }}", markdown_html)

    dest_directory = os.path.dirname(dest_path)

    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    with open(dest_path, 'w') as destination_file:
        destination_file.write(html_doc)
