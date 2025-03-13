import os
import shutil
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_html_node

# Folders
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
content_path = os.path.join(root_dir, "content", "index.md")
template_path = os.path.join(root_dir, "template.html")
dest_path = os.path.join(root_dir, "public", "index.html")

# Function to check and delete public folder and it's files
def public_folder():
    if os.path.exists("public"):
        print("Public folder exists, removing")
        shutil.rmtree("public")
        if os.path.exists("public"):
            print("Error: Couldn't delete public folder")
        else:
            print("Success: Public folder deleted\nCreating new empty folder Public")
            os.mkdir("public")
            if os.path.exists("public"):
                print("Success: New empty public folder created!\nAdding static files")
                copy_files()
                generate_page(content_path, template_path, dest_path)
            else:
                print("Error: Couldn't create public folder")         
    else:
        print("Public folder not found!!\nCreating new empty folder Public")
        os.mkdir("public")
        public_folder()    

# Function for copy files from static to public folder
def copy_files(src="static", dest="public"):

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)

        if os.path.isfile(src_path):
            print(f"Found file: {file}")
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            print(f"Found folder: {file}")
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            copy_files(src_path, dest_path)
        else:
            print(f"Error: Found ANOMALY: {src_path}")

# Function to create index.html
def create_index():
    pass

# Extracting title
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            print(f"Success: Found title {stripped_line.lstrip("#").strip()}")
            return stripped_line.lstrip("#").strip()
    raise Exception("Error: Header is missing.")

# Generating page with template
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()
    
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(final_html)

def main():
    public_folder()


main()