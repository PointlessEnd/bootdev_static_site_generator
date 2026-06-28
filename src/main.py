from textnode import TextNode, TextType


def main() -> None:
    test = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
    print(test)

main()