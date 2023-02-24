import utils
import re
import ast


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
    "009": "Function name '{0}' should be written in snake_case",
    "010": "Argument name '{0} should be written in snake_case",
    "011": "Variable name '{0}' should be written in snake_case",
    "012": "The default argument value is mutable",
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


def check_lines_between_functions(index, line, lines, path):
    """Check if there are more than two blank lines preceding a code line."""
    if line and lines[index].strip() == '' and lines[index-1].strip() == '' and lines[index-2].strip() == '':
        print_error(index+1, 5, path)


def check_declaration_spaces(index, string, path):
    """Check if declaration has correct # of spaces."""

    declaration = utils.is_declaration(string)
    pattern = r"(class\s{2,}\w+)|(def\s{2,}\w+)"
    if declaration and re.match(pattern, string.strip()):
        code = list(style_issues.keys())[6]
        msg = style_issues[code].format(declaration)
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_class_name(index, string, path):
    """Check if class name is written in CamelCase."""

    declaration = utils.is_declaration(string)
    is_camel_case = string != string.lower() and string != string.upper() and "_" not in string

    if declaration == "class" and not is_camel_case:
        name = re.match(r"(class\s+)(\w+)", string).group(2)
        code = list(style_issues.keys())[7]
        msg = style_issues[code].format(name)
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_function_name(index, string, path):
    """Check if function name is written in snake_case."""
    declaration = utils.is_declaration(string)
    is_snake_case = string == string.lower()


    if declaration == "function" and not is_snake_case:
        name = re.match(r"(\s*def\s+)(\w+)", string).group(2)
        code = list(style_issues.keys())[8]
        msg = style_issues[code].format(name)
        print(f"{path}: Line {index + 1}: S{code} {msg}")


def check_argument_name(index, string, path):
    """Check if argument name is written in snake_case."""
    pass


def check_variable_name(index, string, path):
    """Check if variable name is written in snake_case."""
    pass


def check_default_argument(index, string, path):
    """Check if the default argument value is mutable."""
    pass


def print_error(index, msg_index, path):
        code = list(style_issues.keys())[msg_index]
        msg = style_issues[code]
        print(f"{path}: Line {index + 1}: S{code} {msg}")