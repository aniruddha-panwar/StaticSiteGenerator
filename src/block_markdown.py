def markdown_to_blocks(markdown: str) -> list[str]:
    block_list = markdown.split("\n\n")

    block_list = [elem.strip() for elem in block_list if elem != ""]

    return block_list
