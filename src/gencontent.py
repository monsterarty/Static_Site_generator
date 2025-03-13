import os
from markdown_blocks import markdown_to_html_node

# Generating page with template
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(template_path, "r") as file:
        template_content = file.read()
    
    with open(from_path, "r") as file:
        markdown_content = file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
        print(f" CREATING DIRECTORY: {dest_dir_path}")

    with open(dest_path, "w") as file:
        file.write(final_html)
        print(f"WRITING FILE: {dest_path}")

# Extracting title
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            print(f"Success: Found title {stripped_line.lstrip("#").strip()}")
            return stripped_line.lstrip("#").strip()
    raise Exception("Error: Header is missing.")

