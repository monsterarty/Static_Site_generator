import os
import shutil
from textnode import TextNode, TextType

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
            else:
                print("Error: Couldn't create public folder")         
    else:
        print("Public folder not found!!\nCreating new empty folder Public")
        os.mkdir("public")
        if os.path.exists("public"):
            print("Success: New empty public folder created!\nAdding static files")
            copy_files()
        else:
            print("Error: Couldn't create public folder")     

def copy_files(src="static", dsc="public"):

    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dsc_path = os.path.join(dsc, file)

        if os.path.isfile(src_path):
            print(f"Found file: {file}")
            shutil.copy(src_path, dsc_path)
        elif os.path.isdir(src_path):
            print(f"Found folder: {file}")
            if not os.path.exists(dsc_path):
                os.mkdir(dsc_path)
            copy_files(src_path, dsc_path)
        else:
            print(f"Error: Found ANOMALY: {src_path}")

def main():
    print(TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev"))
    public_folder()


main()