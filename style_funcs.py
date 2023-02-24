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
    "010": "Argument name '{0}' should be written in snake_case",
    "011": "Variable name '{0}' should be written in snake_case",
    "012": "The default argument value is mutable",
}

class ArgumentChecker(ast.NodeVisitor):
    """Check if argument name is written in snake_case."""

    def __init__(self, path):
        self.path = path

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            if arg.arg != arg.arg.lower():
                print_error(arg.lineno, 10, self.path, arg.arg)
        self.generic_visit(node)


class VariableChecker(ast.NodeVisitor):
    """Check if variable name is written in snake_case."""

    def __init__(self, path):
        self.path = path

    def visit_FunctionDef(self, node):
        for arg in node.body:
            if isinstance(arg, ast.Assign):
                for target in arg.targets:
                    if target.id != target.id.lower():
                        print_error(target.lineno, 11, self.path, target.id)
        self.generic_visit(node)


class DefaultArgumentChecker(ast.NodeVisitor):
    """Check if default argument value is mutable."""

    def __init__(self, path):
        self.path = path

    def visit_FunctionDef(self, node):
        if node.args.defaults:
            for default in node.args.defaults:
                if isinstance(default, ast.List) or isinstance(default, ast.Dict) or isinstance(default, ast.Set):
                    print_error(node.lineno, 11, self.path)
        self.generic_visit(node)


class ClassNameChecker(ast.NodeVisitor):
    """Check if class name is written in CamelCase."""

    def __init__(self, path):
        self.path = path

    def visit_ClassDef(self, node):
        if node.name != node.name.capitalize():
            print_error(node.lineno, 8, self.path, node.name)
        self.generic_visit(node)


class FunctionNameChecker(ast.NodeVisitor):
    """Check if function name is written in snake_case."""

    def __init__(self, path):
        self.path = path

    def visit_FunctionDef(self, node):
        if node.name != node.name.lower():
            print_error(node.lineno, 9, self.path, node.name)
        self.generic_visit(node)


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


def check_class_name(doc, path):
    """Check if class name is written in CamelCase."""
    ClassNameChecker(path).visit(ast.parse(doc))


def check_function_name(doc, path):
    """Check if function name is written in snake_case."""
    FunctionNameChecker(path).visit(ast.parse(doc))


def check_argument_name(doc, path):
    """Check if argument name is written in snake_case."""
    ArgumentChecker(path).visit(ast.parse(doc))


def check_variable_name(doc, path):
    """Check if variable name is written in snake_case."""
    VariableChecker(path).visit(ast.parse(doc))


def check_default_argument(doc, path):
    """Check if the default argument value is mutable."""
    DefaultArgumentChecker(path).visit(ast.parse(doc))


def print_error(index, msg_index, path, name=None):
        code = list(style_issues.keys())[msg_index]
        msg = style_issues[code]
        if name:
            msg = style_issues[code].format(name)
        print(f"{path}: Line {index + 1}: S{code} {msg}")