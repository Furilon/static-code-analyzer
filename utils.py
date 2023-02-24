import sys, os

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


def get_path():
    """Get path from stdin."""
    path = sys.argv[1]
    if not os.path.exists(path):
        print("File does not exist")
        sys.exit(1)
    return path