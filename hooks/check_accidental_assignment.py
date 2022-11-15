#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import argparse
from typing import Sequence

LINE_INDEX = 0
CHAR_INDEX = 1


def find_parens(lines: list[str]) -> None: # yields (start, end, string, keyword) -> list[tuple[tuple[int, int], tuple[int, int], str, str]]

    start = (0, 0)
    end = (0, 0)
    depth = 0

    inside_cpp_comment = False
    inside_string = False
    match = ''

    # iterate over character over lines
    line_enum = enumerate(lines)
    for line_no, line in line_enum:
        char_enum = enumerate(line)
        for index, char in char_enum:

            # check for comments
            if inside_cpp_comment:
                if char == '*' and index < len(line) - 1:
                    if line[index+1] == '/':
                        # end of cpp comment
                        inside_cpp_comment = False
                        next(char_enum) # skip next char (the '/'), prevent from being added to match
                continue

            if char == '/' and index < len(line) - 1:
                if line[index+1] == '/':
                    # skip c comment
                    break
                if line[index+1] == '*':
                    # cpp comment start
                    inside_cpp_comment = True
                    next(char_enum) # skip next char (the '*') prevent early comment end
                    continue

            # check for strings
            if char == '"':
                inside_string = not inside_string
                continue

            if inside_string:
                continue

            # search for parentheses
            if char == '(':
                if depth == 0:
                    # start of parentheses
                    match = ''
                    start = (line_no, index + 1)
                else:
                    match += char
                depth += 1
                continue

            elif char == ')' and depth > 0:
                depth -= 1
                if depth == 0:
                    # end of parentheses
                    end = (line_no, index)

                    # get keyword
                    keyword = lines[start[LINE_INDEX]][:start[CHAR_INDEX]-1].split()
                    if keyword:
                        keyword = keyword.pop().strip()
                    else:
                        keyword = ''

                    # append to list
                    yield (start, end, match, keyword)

                else:
                    match += char
                continue

            if depth > 0:
                match += char

        if depth > 0:
            match += '\n'


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


def check_accidental_assignment(filename: str, strict: bool = False, ignore_keywords: list[str] | None = None, quiet: bool = False) -> int:
    with open(filename) as f:
        contents = f.read()

    lines = contents.splitlines()

    retv = 0

    for (start, end, string, keyword) in find_parens(lines):
        if ignore_keywords and keyword in ignore_keywords:
            continue

        if not check_parens_content(string, keyword, strict):
            if not quiet:
                line_no = start[LINE_INDEX] + 1
                char_no = start[CHAR_INDEX] + 1

                pre_stub = lines[start[LINE_INDEX]][:start[CHAR_INDEX]]
                post_stub = lines[end[LINE_INDEX]][end[CHAR_INDEX]:]

                if start[LINE_INDEX] == end[LINE_INDEX]:
                    content_stub = lines[start[LINE_INDEX]][start[CHAR_INDEX]:end[CHAR_INDEX]]
                else:
                    content_stub = lines[start[LINE_INDEX]][start[CHAR_INDEX]:] + '\n'
                    for line in lines[start[LINE_INDEX]+1:end[LINE_INDEX]]:
                        content_stub += line + '\n'
                    content_stub += lines[end[LINE_INDEX]][:end[CHAR_INDEX]]

                print(
                    f'{filename}:{line_no}:{char_no}: {red_text("error:")} assignment inside parentheses:')
                print(f'{line_no:5d} | {pre_stub}{red_text(content_stub)}{post_stub}')
            retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--strict', action='store_true', help='strictly check, i.e. check for assignment in all parentheses found, default is to check on if/while/for/switch',
    )
    parser.add_argument(
        '--quiet', action='store_true', help='quiet, no prints',
    )
    parser.add_argument('-s', '--skip-keywords', nargs='+',
                        help='keywords preciding parentheses to ignore')
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= check_accidental_assignment(
            filename, args.strict, args.skip_keywords)

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
