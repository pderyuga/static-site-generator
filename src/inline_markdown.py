import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
    step2 = split_nodes_delimiter(step1, "_", TextType.ITALIC)
    step3 = split_nodes_delimiter(step2, "`", TextType.CODE)
    step4 = split_nodes_image(step3)
    result = split_nodes_link(step4)

    return result


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


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        markdown_images = extract_markdown_images(text)

        if len(markdown_images) == 0:
            new_nodes.append(old_node)
            continue

        for image_alt, image_link in markdown_images:
            delimiter = f"![{image_alt}]({image_link})"
            old_node_parts = text.split(delimiter, 1)

            if len(old_node_parts) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if old_node_parts[0] != "":
                new_nodes.append(TextNode(old_node_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = old_node_parts[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text

        markdown_links = extract_markdown_links(text)

        if len(markdown_links) == 0:
            new_nodes.append(old_node)
            continue

        for link_anchor, link_url in markdown_links:
            delimiter = f"[{link_anchor}]({link_url})"
            old_node_parts = text.split(delimiter, 1)

            if len(old_node_parts) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if old_node_parts[0] != "":
                new_nodes.append(TextNode(old_node_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            text = old_node_parts[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
