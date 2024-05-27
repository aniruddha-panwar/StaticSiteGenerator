import os
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_heading,
    markdown_to_htmlnode,
)


def extract_title(markdown: str):
    """
    Get the title from a markdown text wall
    A valid/qualifying markdown should have a level 1 title ("# blah blah")
        which will be used as the h1 header
    """
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            if block.startswith("# "):
                return block[2:]
    raise ValueError("No title found for h1 header")


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # read markdown file at from_path
    if not os.path.exists(from_path):
        raise ValueError(f"Markdown file does not exist at: {from_path}")
    with open(from_path, "r") as md_file:
        markdown_contents = md_file.read()

    # read the template file at template_path
    if not os.path.exists(template_path):
        raise ValueError(f"Template file does not exist : {template_path}")
    with open(template_path, "r") as template_file:
        template_contents = template_file.read()

    # convert markdown to html
    html_node = markdown_to_htmlnode(markdown_contents)
    html_contents = html_node.to_html()

    # grab title
    title = extract_title(markdown_contents)

    # replace title and content in template
    template_contents = template_contents.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_contents
    )

    # write new html to file at dest_path
    # get dest_path parent dir
    dest_path_parent_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_path_parent_dir):
        os.makedirs(dest_path_parent_dir)
    with open(dest_path, "w") as writer:
        writer.write(template_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Source directory does not exist: {dir_path_content}")

    if not os.path.isdir(dir_path_content):
        raise ValueError(f"Source path is not a directory: {dir_path_content}")

    print(f"Scanning the directory {dir_path_content}")

    for file_folder in os.listdir(dir_path_content):
        file_folder_path = os.path.join(dir_path_content, file_folder)
        dest_path = os.path.join(dest_dir_path, file_folder)
        if file_folder.endswith(".md"):
            generate_page(
                file_folder_path, template_path, dest_path.replace(".md", "") + ".html"
            )

        if os.path.isdir(file_folder_path):
            generate_pages_recursive(file_folder_path, template_path, dest_path)
