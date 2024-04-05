import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


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

        for image in images:

            # the following split, should split the text into 2 parts
            # one part before the img anchor text and url
            # one part after the img anchor text and url
            sections = old_node_text.split(f"![{image[0]}]({image[1]}), 1")

            # we should have 2 sections per the split above
            # anything else is an invalid image markdown
            if len(sections) != 2:
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
 
            if sections[1] != "":
                split_nodes.append(
                    TextNode(
                        sections[1],
                        text_type_text
                    )
                )

    return split_nodes
