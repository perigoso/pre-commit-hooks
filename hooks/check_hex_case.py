#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import argparse
import difflib
import re
from functools import partial
from typing import Sequence

HEXNUM_RE = r'0x[0-9a-f]+'


def match_fix_hex(match_object, upper_preffix: bool = False, upper_digits: bool = True) -> str:
    string = match_object.group(0)
    preffix = string[:2]
    digits = string[2:]

    preffix = preffix.upper() if upper_preffix else preffix.lower()
    digits = digits.upper() if upper_digits else digits.lower()

    return preffix + digits


def check_hex_case(filename: str, edit_in_place: bool = False, upper_preffix: bool = False, upper_digits: bool = True) -> int:
    with open(filename, encoding='utf-8') as f:
        contents = f.read()

    match_callback = partial(
        match_fix_hex, upper_preffix=upper_preffix, upper_digits=upper_digits,
    )

    new_contents, replace_count = re.subn(
        HEXNUM_RE, match_callback, contents, flags=re.IGNORECASE,
    )

    if replace_count != 0 and contents != new_contents:

        if edit_in_place:
            with open(filename, 'w') as f:
                f.write(new_contents)
        else:
            diff = difflib.unified_diff(
                contents.splitlines(), new_contents.splitlines(), fromfile=filename,
            )
            for line in diff:
                print(line)

        return 1

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--edit-in-place',
        action='store_true', help='fix include guards',
    )
    parser.add_argument(
        '--upper-prefix', action='store_true', help='hex prefix in upper case (default: lower)',
    )
    parser.add_argument(
        '--lower-digits', action='store_false', help='hex digits in lower case (default: upper)',
    )
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= check_hex_case(
            filename, args.edit_in_place,
            args.upper_prefix, args.lower_digits,
        )

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
