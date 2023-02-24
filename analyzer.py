import style_funcs, os


def analyze_file(path):
     """Analyze file and print errors."""
     with open(path, encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            style_funcs.check_for_length(i, line, path)
            style_funcs.check_for_indentation(i, line, path)
            style_funcs.check_for_semicolon(i, line, path)
            style_funcs.check_space_before_comment(i, line, path)
            style_funcs.check_todo(i, line, path)
            style_funcs.check_lines_between_functions(i, path)
            style_funcs.check_declaration_spaces(i, line, path)
            style_funcs.check_class_name(i, line, path)
            style_funcs.check_function_name(i, line, path)


def analyze_directory(path):
    """Analyze all files in directory and subdirectories."""
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and file != "tests.py":
                analyze_file(os.path.join(root, file))


def main(path):
    """Check if path is file or directory."""
    if os.path.isfile(path):
        analyze_file(path)
    elif os.path.isdir(path):
        analyze_directory(path)