import re


class __TreeNode:
    def __init__(self, head_level, head_content):
        self.head_level = head_level
        self.head_content = head_content
        self.sub_nodes = []


def __handle_line(md_line):
    if not md_line or not md_line.startswith("#"):
        return 0, ""
    md_heads = re.split("(#+)", md_line.strip(), 1)
    return len(md_heads[1].strip()), md_heads[2].strip() if len(md_heads) >= 3 else ""


def __handle_head_level(node, level, content):
    new_node = __TreeNode(level, content)
    current_level = level - 1
    current_ite_times = 0
    current_node = node
    while current_level:
        current_ite_times += 1
        if not current_node.sub_nodes:
            current_node.sub_nodes.append(__TreeNode(current_ite_times, ""))
        current_node = current_node.sub_nodes[-1]
        current_level -= 1
    current_node.sub_nodes.append(new_node)



def handle_md_file(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as md_file:
        root_node = __TreeNode(0, "root")
        for line in md_file:
            head_level, head_content = __handle_line(line)
            if head_level:
                __handle_head_level(root_node, head_level, head_content)
        return root_node

