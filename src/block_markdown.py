import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    block_list = markdown.split("\n\n")

    block_list = [elem.strip() for elem in block_list if elem != ""]

    return block_list


def block_to_block_type(block: str) -> str:
    # heading block type check
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading

    # code block type check
    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    # The rest of the block types need line by line check
    lines = block.split("\n")

    # quote block type check
    if any(map(lambda x: x.startswith(">"), lines)):
        return block_type_quote

    # unordered list block type check
    if any(map(lambda x: x.startswith("* ") or x.startswith("- "), lines)):
        return block_type_unordered_list

    # ordered list check
    if lines[0].startswith("1. "):
        line_num = 1
        for line in lines:
            if not line.startswith(f"{line_num}. "):
                return block_type_paragraph
            line_num += 1
        return block_type_ordered_list
    return block_type_paragraph
