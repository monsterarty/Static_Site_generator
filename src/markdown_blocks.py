import re
from enum import Enum

from htmlnode import ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_html_node(markdown):

    parent = ParentNode("div", [])
    child_list = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                paragraph_text = block.replace("\n", " ")
                child = ParentNode("p", text_to_children(paragraph_text))
                child_list.append(child)
            case BlockType.HEADING:
                level = hashtag_level(block)
                content = block.lstrip("#").strip()
                child = ParentNode(f"h{level}", text_to_children(content))
                child_list.append(child)
            case BlockType.CODE:
                lines = block.split("\n")
                code_content = "\n".join(lines[1:-1]) + "\n"

                text_node = TextNode(code_content, TextType.TEXT)
                html_node = text_node_to_html_node(text_node)
                
                code_node = ParentNode("code", [html_node])
                pre_node = ParentNode("pre", [code_node])
                child_list.append(pre_node)
            case BlockType.QUOTE:
                clean_lines = []
                for line in block.split("\n"):
                    if line.startswith(">"):
                        clean_lines.append(line.lstrip(">").strip())
                    else:
                        clean_lines.append(line.strip())
                clean_content = "\n".join(clean_lines)
                
                child = ParentNode("blockquote", text_to_children(clean_content))
                parent.children.append(child)
            case BlockType.ULIST:
                lines = split_lines(block, BlockType.ULIST)
                child = ParentNode("ul", lines)
                child_list.append(child)
            case BlockType.OLIST:
                lines = split_lines(block, BlockType.OLIST)
                child = ParentNode("ol", lines)
                child_list.append(child) 
            case _:
                raise Exception("Invalid block type")
                
    parent.children.extend(child_list)
    return parent

def split_lines(block, block_type):
    lines = block.split("\n")
    children = []
    for line in lines:
        if not line.strip():
            continue
            
        if block_type == BlockType.ULIST:
            content = line.lstrip("- ").strip()
        elif block_type == BlockType.OLIST:
            content = re.sub(r"^\d+\.\s*", "", line).strip()
        else:
            content = line.strip()
            
        # Create li element with processed content
        li_node = ParentNode("li", text_to_children(content))
        children.append(li_node)
        
    return children

def hashtag_level(hashtag):
    count = 0
    for char in hashtag:
        if char == "#":
            count += 1
        else:
            break

    return min(max(count, 1), 6)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_block_type(block):
    lines = block.split("\n")

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    list_of_blocks = []
    markdown = markdown.strip()
    blocks = re.split(r"\n{2,}", markdown)
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            lines = [line.strip() for line in stripped_block.splitlines()]
            cleaned_block = "\n".join(lines)
            list_of_blocks.append(cleaned_block)
    return list_of_blocks