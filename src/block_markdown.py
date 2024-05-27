from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode

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


def markdown_to_htmlnode(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


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
    if all(map(lambda x: x.startswith(">"), lines)):
        return block_type_quote

    # unordered list block type check
    if all(map(lambda x: x.startswith("* ") or x.startswith("- "), lines)):
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


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_htmlnode(block)
    if block_type == block_type_heading:
        return heading_to_htmlnode(block)
    if block_type == block_type_code:
        return code_to_htmlnode(block)
    if block_type == block_type_quote:
        return quote_to_htmlnode(block)
    if block_type == block_type_unordered_list:
        return ulist_to_htmlnode(block)
    if block_type == block_type_ordered_list:
        return olist_to_htmlnode(block)
    raise ValueError(f"Invalid block type {block_type}")


def paragraph_to_htmlnode(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_htmlnode(block: str):
    heading_lvl = 0
    for char in block:
        if char == "#":
            heading_lvl += 1
        else:
            break
    # check if there is no text in block
    if heading_lvl + 1 >= len(block):
        raise ValueError(f"Invalid Heading level : {heading_lvl}")
    text = block[heading_lvl + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{heading_lvl}", children)


def code_to_htmlnode(block: str):
    code_text = block[4:-3]
    children = text_to_children(code_text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_htmlnode(block: str):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    children = text_to_children(" ".join(new_lines))
    return ParentNode("blockquote", children)


def ulist_to_htmlnode(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def olist_to_htmlnode(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
