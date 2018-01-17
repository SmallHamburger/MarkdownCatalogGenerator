import markdown_catalog_generator_printer as printer
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("You have to specify one markdown file path at least!")
        sys.exit(1)
    skip_first = 0
    for file_path in sys.argv:
        if not skip_first:
            skip_first = 1
        else:
            with open(file_path + ".tree", "w") as file:
                printer.set_print_file(file)
                printer.start_print(file_path)
