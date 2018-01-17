import sys
import markdown_catalog_generator_core as core


print_file = None

def print_node_tree(node, is_first, is_last, parent_line_count):
    tables = ''
    for index, value in enumerate(parent_line_count):
        if value:
            tables += '丨\t'
        elif index:
            tables += '\t'
    if is_first:
        print(tables, file=print_file)
    else:
        print(tables + '丨', file=print_file)
    print(tables + ('└  ' if is_last else '├  ') + node.head_content, file=print_file)
    length = len(node.sub_nodes) - 1
    for index, sub_node in enumerate(node.sub_nodes):
        temp_line_count = parent_line_count.copy()
        temp_line_count.append(0 if is_last else 1)
        print_node_tree(sub_node, index == 0, index == length, temp_line_count)


def handle_md_file(file_path):
    root_node = core.handle_md_file(file_path)
    if root_node:
        print(file=print_file)
        print("Tree " + file_path, file=print_file)
        length = len(root_node.sub_nodes) - 1
        for index, node in enumerate(root_node.sub_nodes):
            print_node_tree(node, index == 0, index == length, [0])


def handle_except(file_path):
    print(file_path + " is invalid!", file=print_file)


def set_print_file(file=None):
    global print_file
    print_file = file

def start_print(file_path):
    if not file_path:
        print("You have to specify one markdown file path at least!", file=print_file)
        sys.exit(1)
    try:
        handle_md_file(file_path)
    except FileNotFoundError:
        handle_except(file_path)
    print(file=print_file)
