import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

delimiter_map = {"**": text_type_bold, "*": text_type_italic, "`": text_type_code}


def text_to_textnodes(text: str) -> list["TextNode"]:
    nodes = [TextNode(text, text_type_text)]
    for delimiter, text_type in delimiter_map.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delimited_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            delimited_nodes.append(old_node)
            continue

        split_content = old_node.text.split(delimiter)

        # check if formatted section has open and close delim (len%2 == 1)
        if len(split_content) % 2 == 0:
            raise ValueError(
                f"Invalid markdown, formatted section within {delimiter = } not closed"
            )

        for idx, content in enumerate(split_content):
            if content == "":
                continue

            # this represents the non-formatted content of the TextNode's text
            if idx % 2 == 0:
                delimited_nodes.append(
                    TextNode(text=content, text_type=text_type_text, url=None)
                )
            # this represents the part of the content contained within delimited section
            else:
                delimited_nodes.append(
                    TextNode(text=content, text_type=text_type, url=None)
                )
    return delimited_nodes


def extract_markdown_images(text):
    """
    Takes in raw text and spits out alt text and url of markdown images
    The return value is a list of tuples
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Takes in raw text and spits out anchor text and URL
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    """
    Takes in a list of TextNodes and spews out TextNodes with text and image types
    """
    split_nodes = []

    # Check if the old nodes have images
    # If they have images process them (split up into text and image type)

    for old_node in old_nodes:
        # if encountering a non-text type node
        if old_node.text_type != text_type_text:
            split_nodes.append(old_node)
            continue

        old_node_text = old_node.text
        images = extract_markdown_images(old_node.text)

        # No images in nodes text; dont split up the node
        if len(images) == 0:
            split_nodes.append(old_node)
            continue

        for image in images:
            # the following split, should split the text into 2 parts
            # one part before the img anchor text and url
            # one part after the img anchor text and url
            sections = old_node_text.split(f"![{image[0]}]({image[1]})", 1)

            # we should have 2 sections per the split above
            # anything else is an invalid image markdown
            if len(sections) != 2:
                import logging

                logging.error(f"{image = }")
                logging.error(f"{old_node_text = }")
                logging.error(f"{sections = }")
                raise ValueError("Invalid markdown, image section not closed")

            # check if sections[0] text is not empty
            if sections[0] != "":
                split_nodes.append(
                    TextNode(
                        sections[0],
                        text_type_text,
                    )
                )

            split_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )

            # sections[0] and first image has been processed
            # so take it out of the text (old_node_text)
            old_node_text = sections[1]

        # any left over unprocessed sections
        if old_node_text != "":
            split_nodes.append(
                TextNode(
                    old_node_text,
                    text_type_text,
                )
            )

    return split_nodes


def split_nodes_link(old_nodes: list["TextNode"]) -> list["TextNode"]:
    split_nodes = []

    for old_node in old_nodes:
        # If node is not a TextNode of text text_type, do not process it
        # and move on to the next node
        if old_node.text_type != text_type_text:
            split_nodes.append(old_node)
            continue

        current_text = old_node.text
        links = extract_markdown_links(current_text)

        # no links in the current node
        if len(links) == 0:
            split_nodes.append(old_node)
            continue

        for link in links:
            splits = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(splits) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if splits[0] != "":
                split_nodes.append(
                    TextNode(
                        splits[0],
                        text_type_text,
                    )
                )
            split_nodes.append(
                TextNode(
                    link[0],
                    text_type_link,
                    link[1],
                )
            )
            # update current text to remove the processed part for the next iteration
            current_text = splits[1]

        if current_text != "":
            split_nodes.append(
                TextNode(
                    current_text,
                    text_type_text,
                )
            )
    return split_nodes
