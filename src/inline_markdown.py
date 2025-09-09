import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception("closing delimeter missing")

        old_node_parts = old_node.text.split(delimiter)
        for i in range(len(old_node_parts)):
            if old_node_parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(old_node_parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(old_node_parts[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
