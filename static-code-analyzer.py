import sys
import os

# Stylistic issues
style_issues = {
    "001": "Too long",
    "002": "Indentation is not a multiple of 4",
    "003": "Unnecessary semicolon after a statement",
    "004": "Less than two spaces before inline comments",
    "005": "TODO found",
    "006": "More than two blank lines preceding a code line",
    '007': "Too many spaces after 'class'",
    "008": "Class name {0} should be written in CamelCase",
    "009": "Function name {0} should be written in snake_case"
}


def check_for_length(index, string, path):
    """Check if line is longer than 79 characters."""
    if len(string.strip()) > 79:
        code = list(style_issues.keys())[0]
        msg = style_issues[code]
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_for_indentation(index, string, path):
    """Check if indentation is not a multiple of 4."""
    if string.startswith((" ")) and (len(string) - len(string.lstrip(" "))) % 4 != 0:
        code = list(style_issues.keys())[1]
        msg = style_issues[code]
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_for_semicolon(index, string, path):
    """Check if there is an unnecessary semicolon after a statement."""
    code = string.split("#")[0]
    if code.strip().endswith(';'):
        code = list(style_issues.keys())[2]
        msg = style_issues[code]
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_space_before_comment(index, string, path):
    """Check if there are less than two spaces before inline comments."""
    if string.__contains__("#") and not string.strip().startswith("#"):
        text = string.split("#")[0]
        if len(text) - len(text.rstrip(" ")) != 2:
            code = list(style_issues.keys())[3]
            msg = style_issues[code]
            print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_todo(index, string, path):
    """Check if TODO is found in comment."""
    if string.__contains__("#"):
        comment = string.split("#", 1)[-1].strip().lower()
        if "todo" in comment:
            code = list(style_issues.keys())[4]
            msg = style_issues[code]
            print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_lines_between_functions(index, path):
        """Check if there are more than two blank lines preceding a code line."""
        code = list(style_issues.keys())[5]
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
        empty_line_counter = 0
        for i, line in enumerate(file):
            check_for_length(i, line, path)
            check_for_indentation(i, line, path)
            check_for_semicolon(i, line, path)
            check_space_before_comment(i, line, path)
            check_todo(i, line, path)

            if line in ['\r\n', '\n']:
                empty_line_counter += 1
            elif empty_line_counter > 2:
                        check_lines_between_functions(i, path)
                        empty_line_counter = 0


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
