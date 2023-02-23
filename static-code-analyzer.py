import sys, os, re

# Stylistic issues
style_issues = {
    "001": "Too long",
    "002": "Indentation is not a multiple of 4",
    "003": "Unnecessary semicolon after a statement",
    "004": "Less than two spaces before inline comments",
    "005": "TODO found",
    "006": "More than two blank lines preceding a code line",
    '007': "Too many spaces after '{0}'",
    "008": "Class name '{0}' should be written in CamelCase",
    "009": "Function name '{0}' should be written in snake_case"
}


def check_for_length(index, string, path):
    """Check if line is longer than 79 characters."""
    if len(string.strip()) > 79:
        print_error(index, 0, path)


def check_for_indentation(index, string, path):
    """Check if indentation is not a multiple of 4."""

    if string.startswith((" ")) and (len(string) - len(string.lstrip(" "))) % 4 != 0:
        print_error(index, 1, path)


def check_for_semicolon(index, string, path):
    """Check if there is an unnecessary semicolon after a statement."""

    code = string.split("#")[0]
    if code.strip().endswith(';'):
        print_error(index, 2, path)


def check_space_before_comment(index, string, path):
    """Check if there are less than two spaces before inline comments."""
    
    if string.__contains__("#") and not string.strip().startswith("#"):
        text = string.split("#")[0]
        if len(text) - len(text.rstrip(" ")) != 2:
            print_error(index, 3, path)


def check_todo(index, string, path):
    """Check if TODO is found in comment."""

    if string.__contains__("#"):
        comment = string.split("#", 1)[-1].strip().lower()
        if "todo" in comment:
            print_error(index, 4, path)


def check_lines_between_functions(index, path):
    """Check if there are more than two blank lines preceding a code line."""
    print_error(index, 5, path)


def check_declaration_spaces(index, string, path):
    """Check if declaration has correct # of spaces."""

    declaration = is_declaration(string)
    pattern = r"(class\s{2,}\w+)|(def\s{2,}\w+)"
    if declaration and re.match(pattern, string.strip()):
        code = list(style_issues.keys())[6]
        msg = style_issues[code].format(declaration)
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_class_name(index, string, path):
    """Check if class name is written in CamelCase."""

    declaration = is_declaration(string)
    is_camel_case = string != string.lower() and string != string.upper() and "_" not in string

    if declaration == "class" and not is_camel_case:
        name = re.match(r"(class\s+)(\w+)", string).group(2)
        code = list(style_issues.keys())[7]
        msg = style_issues[code].format(name)
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_function_name(index, string, path):
    """Check if function name is written in snake_case."""
    declaration = is_declaration(string)
    is_snake_case = string == string.lower()


    if declaration == "function" and not is_snake_case:
        name = re.match(r"(\s*def\s+)(\w+)", string).group(2)
        code = list(style_issues.keys())[8]
        msg = style_issues[code].format(name)
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def is_declaration(string):
    """Check if line is a declaration."""
    if string.strip().startswith("def"):
        return "function"
    elif string.strip().startswith("class"):
        return "class"
    else:
        return False


def print_error(index, msg_index, path):
        code = list(style_issues.keys())[msg_index]
        msg = style_issues[code]
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def is_correct_length(num_args):
    """Check if correct number of arguments."""
    if num_args == 2:
        return
    else:
        print("Program requires one argument: path to file or directory")


def get_path():
    """Get path from stdin."""
    path = sys.argv[1]
    if not os.path.exists(path):
        print("File does not exist")
        sys.exit(1)
    return path


def analyze_file(path):
     """Analyze file and print errors."""
     with open(path, encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # check_for_length(i, line, path)
            # check_for_indentation(i, line, path)
            # check_for_semicolon(i, line, path)
            # check_space_before_comment(i, line, path)
            # check_todo(i, line, path)

            # if line and lines[i].strip() == '' and lines[i-1].strip() == '' and lines[i-2].strip() == '':
            #     check_lines_between_functions(i+1, path)
            
            # check_declaration_spaces(i, line, path)
            # check_class_name(i, line, path)
            check_function_name(i, line, path)


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


if __name__ == "__main__":
    # Check if correct number of arguments
    is_correct_length(len(sys.argv))
    
    # Get path from stdin
    path = get_path()

    # Check if path is file or directory
    main(path)
