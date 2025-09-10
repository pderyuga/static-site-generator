def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = list(map(lambda x: x.strip(), filter(lambda x: x != "", blocks)))
    return stripped_blocks
