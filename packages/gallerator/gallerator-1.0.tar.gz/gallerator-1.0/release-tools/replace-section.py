#!/usr/bin/env/python3

import sys
from pathlib import Path

"""
Usage:

# If you have sponge from moreutils

cat source.txt | $0 section_name replacement | sponge source.txt

# else

cat source.txt | $0 section_name replacement > source-new.txt
"""

def replace(orig: str, section: str, replacement: str):
    lines = orig.rstrip().split("\n")
    output_lines = []
    inside_section = False
    for line in lines:
        if f'/replace-section:{section}' in line:
            inside_section = False
        elif f'replace-section:{section}' in line:
            inside_section = True
            output_lines.append(line)
            output_lines.append(replacement)
        if not inside_section:
            output_lines.append(line)
    return "\n".join(output_lines)

def main():
    [section, replacement] = sys.argv[1:]
    input = sys.stdin.read()
    print(replace(input, section, replacement))

if __name__ == "__main__":
    main()