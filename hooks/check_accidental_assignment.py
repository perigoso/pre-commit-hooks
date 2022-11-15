#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import argparse
from typing import Sequence

LINE_INDEX = 0
CHAR_INDEX = 1


def capture_match(lines: list[str], start: tuple[int, int], end: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int], str, str]:
    content = ''

    keyword = lines[start[LINE_INDEX]][:start[CHAR_INDEX]-1].split()
    if keyword:
        keyword = keyword.pop().strip()
    else:
        keyword = ''

    if start[LINE_INDEX] == end[LINE_INDEX]:
        content = lines[start[LINE_INDEX]][start[CHAR_INDEX]:end[CHAR_INDEX]]
    else:
        content = lines[start[LINE_INDEX]][start[CHAR_INDEX]:]

        for line_no in range(start[LINE_INDEX] + 1, end[LINE_INDEX]):
            content += lines[line_no]

        content += lines[end[LINE_INDEX]][:end[CHAR_INDEX]]

    return (start, end, content, keyword)


def find_parens(lines: list[str]) -> list[tuple[tuple[int, int], tuple[int, int], str, str]]:
    parens = []

    start = (0, 0)
    end = (0, 0)
    depth = 0

    for line_no, line in enumerate(lines):
        for index, char in enumerate(line):
            if char == '(':
                if depth == 0:
                    start = (line_no, index + 1)
                depth += 1

            elif char == ')':
                depth -= 1
                if depth == 0:
                    end = (line_no, index)
                    parens.append(capture_match(lines, start, end))

    return parens


def check_parens_content(string: str, keyword: str, strict: bool = False) -> bool:
    if keyword not in ['if', 'while', 'switch', 'for'] and not strict:
        return True

    if keyword == 'for':
        # special case for for loops
        # only check the middle part of the for loop, where the assignment is not allowed
        string = string.split(';')[1]

    inside_string = False

    # check for assignment
    for index, char in enumerate(string):
        if char == '"':
            inside_string = not inside_string
            continue

        if not inside_string and char == '=':
            if index != 0:
                preciding_char = string[index-1]
                if preciding_char in ['=', '!']:
                    # not an assignment
                    continue
                elif preciding_char in ['>', '<']:
                    # special case for >>=, <<=
                    if index > 1:
                        pre_preciding_char = string[index-2]
                        if pre_preciding_char == preciding_char:
                            # <<= / >>= assignment detected
                            return False
                    # not an assignment
                    continue

            if index < len(string) - 1:
                succeding_char = string[index+1]
                if succeding_char in ['=']:
                    # not an assignment
                    continue

            # assignment detected
            return False

    return True


def red_text(text: str) -> str:
    return f'\033[31m{text}\033[0m'


def check_accidental_assignment(filename: str, strict: bool) -> int:
    with open(filename) as f:
        contents = f.read()

    lines = contents.splitlines()

    retv = 0

    for (start, end, string, keyword) in find_parens(lines):
        if not check_parens_content(string, keyword, strict):
            print(
                f'{filename}:{start[LINE_INDEX]+1}:{start[CHAR_INDEX]+1}: {red_text("error:")} accidental assignment:')
            print(f'{start[LINE_INDEX]+1:5d} | {lines[start[LINE_INDEX]][:start[CHAR_INDEX]]}{red_text(string)}{lines[end[LINE_INDEX]][end[CHAR_INDEX]:]}')
            retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument(
        '--strict', action='store_true', help='strictly check, i.e. check for assignment in all parentheses found, default is to check on if/while/for/switch',
    )
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= check_accidental_assignment(filename, args.strict)

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
