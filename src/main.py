import os
import shutil
from copystatic import copy_files
from gencontent import generate_page_all
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_page_all(basepath, dir_path_content, template_path, dir_path_public)

main()