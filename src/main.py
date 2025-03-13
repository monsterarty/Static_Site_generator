import os
import shutil
from copystatic import copy_files
from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def process_markdown_files(content_dir, public_dir, template):
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                
                rel_path = os.path.relpath(markdown_path, content_dir)
                
                dest_path = os.path.join(public_dir, rel_path.replace(".md", ".html"))
                
                generate_page(markdown_path, template, dest_path)

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    print("Generating pages...")
    process_markdown_files(dir_path_content, dir_path_public, template_path)

main()