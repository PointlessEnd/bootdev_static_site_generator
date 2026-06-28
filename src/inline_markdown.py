import re
from typing import Callable

from textnode import TextNode, TextType

def split_nodes_delimiter(
        old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError('invalid markdown, formatted section not closed')
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def _split_nodes_markdown(
    old_nodes: list[TextNode],
    extract_func: Callable[[str], list[tuple[str, str]]],
    text_type: TextType,
    markdown_func: Callable[[str, str], str]
):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        matches = extract_func(original_text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        for text, url in matches:
            markdown = markdown_func(text, url)
            sections = original_text.split(markdown, 1)
            if len(sections) != 2:
                raise ValueError('invalid markdown section')
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, text_type, url))
            original_text = sections[1]
        if original_text != '':
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    return _split_nodes_markdown(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        lambda alt, url: f'![{alt}]({url})'
    )

def split_nodes_link(old_nodes: list[TextNode]):
    return _split_nodes_markdown(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        lambda alt, url: f'[{alt}]({url})'
    )

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
