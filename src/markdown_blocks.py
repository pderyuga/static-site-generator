from enum import Enum
import re


from markdown_blocks import markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = list(map(lambda x: x.strip(), filter(lambda x: x != "", blocks)))
    return stripped_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(re.match(r"^>", line) for line in block.split("\n")):
        return BlockType.QUOTE
    if all(re.match(r"^- ", line) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def is_ordered_list(block):
    if not block.startswith("1. "):
        return False
    lines = block.split("\n")
    i = 1
    for line in lines:
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True


def markdown_to_html_node(markdown):
    # split markdown into an array of lines
    blocks = markdown_to_blocks(markdown)

    html_nodes = []
    for block in blocks:
        # determine the type of block, returns a BlockType
        block_type = block_to_block_type(block)

        # based on the type of block, create a new HTML node with the proper data
        # and assign the proper child HTMLNode objects to the block node
        if block_type.value == "paragraph":
            paragraph_lines = block.split("\n")
            paragraph_text = " ".join(paragraph_lines)
            children = text_to_children(paragraph_text)
            paragraph_html_node = ParentNode("p", children)
            html_nodes.append(paragraph_html_node)

        if block_type.value == "heading":
            heading_level, heading_text = extract_heading(block)
            children = text_to_children(heading_text)
            heading_html_node = ParentNode(f"h{heading_level}", children)
            html_nodes.append(heading_html_node)

        # the code block is special - it should not do any inline markdown parsing of its children
        if block_type.value == "code":
            code_text = extract_code(block)
            code_text_node = TextNode(code_text, TextType.CODE)
            child = text_node_to_html_node(code_text_node)
            code_html_node = ParentNode("pre", [child])
            html_nodes.append(code_html_node)

        if block_type.value == "quote":
            quote_lines = block.split("\n")
            quote_text_lines = []
            for line in quote_lines:
                quote_line_text = extract_quote(line)
                quote_text_lines.append(quote_line_text)
            quote_text = " ".join(quote_text_lines)
            children = text_to_children(quote_text)
            quote_html_node = ParentNode("blockquote", children)
            html_nodes.append(quote_html_node)

        if block_type.value == "unordered_list":
            list_lines = block.split("\n")
            children = []
            for line in list_lines:
                line_text = extract_bullet(line)
                line_item_children = text_to_children(line_text)
                line_item_node = ParentNode("li", line_item_children)
                children.append(line_item_node)
            unordered_list_node = ParentNode("ul", children)
            html_nodes.append(unordered_list_node)

        if block_type.value == "ordered_list":
            list_lines = block.split("\n")
            children = []
            for line in list_lines:
                line_text = extract_number(line)
                line_item_children = text_to_children(line_text)
                line_item_node = ParentNode("li", line_item_children)
                children.append(line_item_node)
            ordered_list_node = ParentNode("ol", children)
            html_nodes.append(ordered_list_node)

    # make all block nodes under a single parent HTMLNode with tag "div"
    parent_node = ParentNode("div", html_nodes)

    return parent_node


# --- Helper functions ---


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes


def extract_heading(text):
    matches = re.search(r"^#{1,6}", text)
    heading_regex = matches.group(0)
    heading_level = len(heading_regex)
    heading_text = text.strip(f"{heading_regex} ")

    return heading_level, heading_text


def extract_bullet(text):
    bullet_text = re.sub(r"^- ", "", text)

    return bullet_text


def extract_number(text):
    number_text = re.sub(r"^\d+\. ", "", text)

    return number_text


def extract_quote(text):
    quote_text = re.sub(r"^>", "", text)

    return quote_text.strip()


def extract_code(text):
    lines = text.split("\n")
    code_lines = lines[1:-1]
    code_block = "\n".join(code_lines)

    if len(code_lines) > 0 and code_lines[-1]:
        code_block += "\n"

    return code_block
