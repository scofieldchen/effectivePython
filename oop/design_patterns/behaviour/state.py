"""
状态模式(state pattern)

案例：解析XML
"""


class Node:
    def __init__(self, tag_name, parent=None):
        self.tag_name = tag_name
        self.parent = parent  # 父节点
        self.children = []  # 包含的子节点
        self.text = ""

    def __str__(self):
        if self.text:
            return f"{self.tag_name}: {self.text}"
        else:
            return self.tag_name


class Parser:
    def __init__(self, parse_string):
        self.parse_string = parse_string
        self.root = None
        self.current_node = None
        self.state = FirstTag()

    def process(self, remaining_string):
        remaining = self.state.process(remaining_string, self)
        if remaining:
            self.process(remaining)  # 递归
    
    def start(self):
        self.process(self.parse_string)


class FirstTag:
    def process(self, remaining_string, parser):
        idx_start_tag = remaining_string.find("<")
        idx_end_tag = remaining_string.find(">")
        tag_name = remaining_string[idx_start_tag+1:idx_end_tag]
        root = Node(tag_name)
        parser.root = parser.current_node = root
        parser.state = ChildNode()  # 将状态切换为ChildNode
        return remaining_string[idx_end_tag+1:]


class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()
        if stripped.startswith("</"):
            parser.state = CloseTag()
        elif stripped.startswith("<"):
            parser.state = OpenTag()
        else:
            parser.state = TextNode()
        return stripped


class OpenTag:
    def process(self, remaining_string, parser):
        idx_start_tag = remaining_string.find("<")
        idx_end_tag = remaining_string.find(">")
        tag_name = remaining_string[idx_start_tag+1:idx_end_tag]
        node = Node(tag_name, parser.current_node)
        parser.current_node.children.append(node)
        parser.current_node = node
        parser.state = ChildNode()
        return remaining_string[idx_end_tag+1:]


class CloseTag:
    def process(self, remaining_string, parser):
        idx_start_tag = remaining_string.find("<")
        idx_end_tag = remaining_string.find(">")
        assert remaining_string[idx_start_tag+1] == "/"
        tag_name = remaining_string[idx_start_tag+2:idx_end_tag]
        assert tag_name == parser.current_node.tag_name
        parser.current_node = parser.current_node.parent
        parser.state = ChildNode()
        return remaining_string[idx_end_tag+1:].strip()


class TextNode:
    def process(self, remaining_string, parser):
        idx_start_tag = remaining_string.find("<")
        text = remaining_string[:idx_start_tag]
        parser.current_node.text = text
        parser.state = ChildNode()
        return remaining_string[idx_start_tag:]
