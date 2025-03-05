import re

def markdown_to_blocks(markdown):
    list_of_blocks = []
    markdown = markdown.strip()
    blocks = re.split(r"\n{2,}", markdown)
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            lines = [line.strip() for line in stripped_block.splitlines()]
            cleaned_block = "\n".join(lines)
            list_of_blocks.append(cleaned_block)
    return list_of_blocks