import sys, os, re


def is_declaration(string):
    """Check if line is a declaration."""
    if string.strip().startswith("def"):
        return "function"
    elif string.strip().startswith("class"):
        return "class"
    else:
        return False
    

def is_correct_length(num_args):
    """Check if correct number of arguments."""
    if num_args == 2:
        return
    else:
        print("Program requires one argument: path to file or directory")


def is_camel_case(s):
    # Check if the string has any uppercase letters
    if not any(c.isupper() for c in s):
        return False
    # Check if the string matches the camel case pattern
    pattern = r'^[A-Z][a-z]+([A-Z][a-z]*)*$'
    return re.match(pattern, s) is not None


def get_path():
    """Get path from stdin."""
    path = sys.argv[1]
    if not os.path.exists(path):
        print("File does not exist")
        sys.exit(1)
    return path


def print_error(style_issues, index, msg_index, path, name=None):
        code = list(style_issues.keys())[msg_index]
        msg = style_issues[code].format(name) if name else style_issues[code]
        print(f"{path}: Line {index}: S{code} {msg}")