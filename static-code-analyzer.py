# Stylistic issues
style_issues = {
    "001": "Too long",
    "002": "Indentation is not a multiple of 4",
    "003": "Unnecessary semicolon after a statement",
    "004": "Less than two spaces before inline comments",
    "005": "TODO found",
    "006": "More than two blank lines preceding a code line",
}


def check_for_length(index, string):
    if len(string.strip()) > 79:
        code = list(style_issues.keys())[0]
        msg = style_issues[code]
        print(f"Line {index + 1}: S{code} {msg}")


def check_for_indentation(index, string):
    if string.startswith((" ")) and (len(string) - len(string.lstrip(" "))) % 4 != 0:
        code = list(style_issues.keys())[1]
        msg = style_issues[code]
        print(f"Line {index + 1}: S{code} {msg}")


def check_for_semicolon(index, string):
    code = string.split("#")[0]
    if code.strip().endswith(';'):
        code = list(style_issues.keys())[2]
        msg = style_issues[code]
        print(f"Line {index + 1}: S{code} {msg}")


def check_space_before_comment(index, string):
    if string.__contains__("#") and not string.strip().startswith("#"):
        text = string.split("#")[0]
        if len(text) - len(text.rstrip(" ")) != 2:
            code = list(style_issues.keys())[3]
            msg = style_issues[code]
            print(f"Line {index + 1}: S{code} {msg}")


def check_todo(index, string):
    if string.__contains__("#"):
        comment = string.split("#", 1)[-1].strip().lower()
        if "todo" in comment:
            code = list(style_issues.keys())[4]
            msg = style_issues[code]
            print(f"Line {index + 1}: S{code} {msg}")


def check_lines_between_functions(index):
        code = list(style_issues.keys())[5]
        msg = style_issues[code]
        print(f"Line {index + 1}: S{code} {msg}")


if __name__ == "__main__":
    # Get path from stdin
    # path = input()
    path = "./testdata.py"

    # open the file and give checks
    with open(path, encoding="utf-8") as file:
        empty_line_counter = 0
        for i, line in enumerate(file):
            check_for_length(i, line)
            check_for_indentation(i, line)
            check_for_semicolon(i, line)
            check_space_before_comment(i, line)
            check_todo(i, line)

            if line in ['\r\n', '\n']:
                empty_line_counter += 1
            elif empty_line_counter > 2:
                        check_lines_between_functions(i)
                        empty_line_counter = 0


            
                