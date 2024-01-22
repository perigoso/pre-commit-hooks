#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import argparse
import re
from typing import Sequence


IFNOTDEF_PATTERN = b'#ifndef '  # b'#if !defined'
DEF_PATTERN = b'#define '
ENDIF_PATTERN = b'#endif'


def check_include_guard(filename: str, relative_to: str = None, edit_in_place: bool = False) -> int:
    include_guard = None
    include_guard_start = None
    include_guard_end = None
    need_fix = False

    # Read as binary so we can read byte-by-byte
    with open(filename, 'rb+', encoding='utf-8') as file_obj:

        i1, line1 = None, None
        for i2, line2 in enumerate(file_obj, start=1):

            if line1 is not None and include_guard_start is None:
                if line1.startswith(IFNOTDEF_PATTERN) and line2.startswith(DEF_PATTERN):
                    line1_include_guard = line1[len(IFNOTDEF_PATTERN):].strip()
                    line2_include_guard = line2[len(DEF_PATTERN):].strip()
                    if line1_include_guard == line2_include_guard:
                        include_guard = line1_include_guard
                        include_guard_start = i1

            if include_guard_start is not None:
                if line2.startswith(ENDIF_PATTERN):
                    include_guard_comment = b'/* ' + include_guard + b' */'
                    line2_include_guard_comment = line2[
                        len(
                            ENDIF_PATTERN,
                        ):
                    ].strip()
                    if line2_include_guard_comment != include_guard_comment:
                        need_fix = True
                    include_guard_end = i2

            line1 = line2
            i1 = i2

    if include_guard_start is None or include_guard_end is None:
        print(f'Unfixable: Include guard missing or malformed in {filename}')
        return 1

    new_include_guard = filename
    if relative_to is not None:
        new_include_guard = new_include_guard.split(relative_to)[-1].strip('/')
    new_include_guard = re.sub('[^a-zA-Z0-9]', '_', new_include_guard)
    new_include_guard = new_include_guard.upper()
    new_include_guard = bytes(new_include_guard, 'utf-8')

    if new_include_guard != include_guard or need_fix:
        # if edit_in_place:
        #     include_guard_comment = b'/* ' + include_guard + b' */'
        #     print(f'Fixing include guard {filename} {include_guard} -> {new_include_guard}')
        #     with open(filename, 'rb+') as file_obj:
        #         file_obj.seek(include_guard_start)
        #         file_obj.write(IFNOTDEF_PATTERN + new_include_guard)
        #         file_obj.seek(include_guard_start + 1)
        #         file_obj.write(DEF_PATTERN + new_include_guard)
        #         file_obj.seek(include_guard_end)
        #         file_obj.write(ENDIF_PATTERN + include_guard_comment)
        # else:
        print(
            f'Include guard {include_guard} does not match {new_include_guard}',
        )
        return 1

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--edit-in-place',
        action='store_true', help='fix include guards',
    )
    parser.add_argument(
        '-r', '--relative-path', type=str,
        default=None, help='relative path for include guard naming',
    )
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        if filename.endswith('.h'):
            retv |= check_include_guard(
                filename, args.relative_path, args.edit_in_place,
            )

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
