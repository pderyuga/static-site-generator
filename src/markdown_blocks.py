from enum import Enum
import re


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
