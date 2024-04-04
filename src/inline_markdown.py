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
