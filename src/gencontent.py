import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_page_all(basepath, dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(basepath, from_path, template_path, dest_path)
        else:
            generate_page_all(basepath, from_path, template_path, dest_path)

# Generating page with template
def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(template_path, "r") as file:
        template_content = file.read()
    
    with open(from_path, "r") as file:
        markdown_content = file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(final_html)

# Extracting title
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            print(f"Success: Found title {stripped_line.lstrip("#").strip()}")
            return stripped_line.lstrip("#").strip()
    raise Exception("Error: Header is missing.")

