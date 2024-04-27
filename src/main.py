# from textnode import TEXT_TYPE_BOLD

import os
import shutil

from copystatic import copy_recursive
from generate import generate_page_recursive

static_path = "./static/"
public_path = "./public/"
content_path = "./content/"

template_path = "./template.html"


def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    copy_recursive(
        static_path,
        public_path,
    )

    generate_page_recursive(
        content_path,
        template_path,
        public_path,
    )


main()
