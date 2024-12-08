import re
import sys


def inspect_fstring(file_path):
    # Regular expression to find f-strings
    fstring_pattern = re.compile(r'f["\'].*?["\']')

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):
        matches = fstring_pattern.findall(line)

        if line.count('"') > 2 or line.count("'") > 2:
            for fstring in matches:
                # Check if there are nested quotes of the same type
                if (fstring.count('"') > 1 and fstring.count("'") == 0) or (fstring.count("'") > 1 and fstring.count('"') == 0):
                    print(f"Line {line_number}: {fstring}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        inspect_fstring(file_path)
