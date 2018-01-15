import sys
import re
import os


class TreeNode:
    def __init__(self, head_level, head_content):
        self.head_level = head_level
        self.head_content = head_content
        self.sub_nodes = []


def handle_line(md_line):
    if not md_line or not md_line.startswith("#"):
        return 0, ""
    md_heads = re.split("(#+)", md_line.strip(), 1)
    return len(md_heads[1].strip()), md_heads[2].strip() if len(md_heads) >= 3 else ""


def handle_head_level(node, level, content):
    new_node = TreeNode(level, content)
    current_level = level - 1
    current_ite_times = 0
    current_node = node
    while current_level:
        current_ite_times += 1
        if not current_node.sub_nodes:
            current_node.sub_nodes.append(TreeNode(current_ite_times, ""))
        current_node = current_node.sub_nodes[-1]
        current_level -= 1
    current_node.sub_nodes.append(new_node)


def print_node_tree(node, is_first, is_last, parent_line_count):
    tables = ''
    for index, value in enumerate(parent_line_count):
        if value:
            tables += '丨\t'
        elif index:
            tables += '\t'
    if is_first:
        print(tables)
    else:
        print(tables + '丨')
    print(tables + ('└  ' if is_last else '├  ') + node.head_content)
    length = len(node.sub_nodes) - 1
    for index, sub_node in enumerate(node.sub_nodes):
        temp_line_count = parent_line_count.copy()
        temp_line_count.append(0 if is_last else 1)
        print_node_tree(sub_node, index == 0, index == length, temp_line_count)


def handle_md_file(file_path):
    print()
    with open(file=file_path, mode="r", encoding="utf-8") as md_file:
        root_node = TreeNode(0, "root")
        for line in md_file:
            head_level, head_content = handle_line(line)
            if head_level:
                handle_head_level(root_node, head_level, head_content)
        print("Tree " + file_path)
        length = len(root_node.sub_nodes) - 1
        for index, node in enumerate(root_node.sub_nodes):
            print_node_tree(node, index == 0, index == length, [0])


def handle_except(file_path):
    print(file_path + " is invalid!", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You have to specify one markdown file path at least!", file=sys.stderr)
        sys.exit(1)
    skip_first = 0
    for file_path in sys.argv:
        if skip_first:
            try:
                '''如果要输出到文本，直接将注释掉的反注释就可以了'''
                # std_out = sys.stdout
                # file = open(file_path + '.tree', mode='w', encoding='utf-8')
                # sys.stdout = file
                handle_md_file(file_path)
            except FileNotFoundError:
                handle_except(file_path)
                # finally:
                # sys.stdout = std_out
                # file.close()
        else:
            skip_first = 1
    print()
