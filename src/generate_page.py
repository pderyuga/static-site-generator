import os
import pathlib

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

    with open(dest_path, "w") as destination_file:
        destination_file.write(html_doc)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(
        f"copying contents of source directory {dir_path_content} into destination directory {dest_dir_path}..."
    )

    if not os.path.exists(dir_path_content):
        raise Exception(f"source path does not exist: {dir_path_content}")

    content_files = os.listdir(dir_path_content)
    print(f"files in {dir_path_content} directory: {content_files}")

    for content_file in content_files:
        content_file_path = pathlib.Path(dir_path_content, content_file)
        dest_file_path = pathlib.Path(dest_dir_path, content_file)
        if os.path.isfile(content_file_path) and str(content_file_path).endswith(".md"):
            dest_file_path = pathlib.Path(dest_dir_path, content_file).with_suffix(".html")
            print(f"copying file from {content_file_path}")
            generate_page(content_file_path, template_path, dest_file_path)
            print(f"copied file to {dest_file_path}")
        else:
            print(f"{content_file} is a directory")
            generate_pages_recursive(content_file_path, template_path, dest_file_path)
