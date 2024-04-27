import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = [line for line in markdown.split("\n") if len(line) != 0]
    line_with_header = [line for line in lines if line.startswith("#")]
    if len(line_with_header) == 0:
        raise Exception("All pages need a header")

    return line_with_header[0].replace("# ", "")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    content = os.listdir(dir_path_content)
    for item in content:
        item_path = os.path.join(dir_path_content, item)
        item_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            item_dest_path = Path(item_dest_path).with_suffix(".html")
            generate_page(item_path, template_path, item_dest_path)
        else:
            generate_page_recursive(item_path, template_path, item_dest_path)
