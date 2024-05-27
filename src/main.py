import os
from textnode import TextNode
from copy_static_to_public import copy_files
from gen_page import generate_pages_recursive


def main():
    print("Copying files from static/ to public/")
    copy_files()

    print("Generating HTML from Markdown")
    # generate_page(
    #     from_path=os.path.join("./content","index.md"),
    #     template_path=os.path.join("./","template.html"),
    #     dest_path=os.path.join("./public","index.html")
    # )
    generate_pages_recursive("./content", "./template.html", "./public")


main()
