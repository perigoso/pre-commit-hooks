#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import argparse
import difflib
import re
from functools import partial
from typing import Sequence

HEXNUM_SUFFIX_RE = r'(?<!\w)0x[0-9a-f]+u?(?!\w)'
NUM_SUFFIX_RE = r'(?<!\w)[0-9]+u(?!\w)'


def match_fix_suffix(match_object, lower_suffix: bool = True) -> str:
    string = match_object.group(0)
    suffix = string[-1]

    if suffix in ['u', 'U']:
        suffix = 'u' if lower_suffix else 'U'

        return string[:-1] + suffix

    return string


def check_unsigned_suffix(filename: str, edit_in_place: bool = False, lower_suffix: bool = False) -> int:
    with open(filename) as f:
        contents = f.read()

    match_callback = partial(match_fix_suffix, lower_suffix=lower_suffix)

    replace_count = 0

    new_contents, hex_replace_count = re.subn(
        HEXNUM_SUFFIX_RE, match_callback, contents, flags=re.IGNORECASE,
    )
    replace_count += hex_replace_count

    new_contents, num_replace_count = re.subn(
        NUM_SUFFIX_RE, match_callback, new_contents, flags=re.IGNORECASE,
    )
    replace_count += num_replace_count

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
        '--lower-suffix', action='store_true', help='unsigned suffix in lower case (default: upper)',
    )
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= check_unsigned_suffix(
            filename, args.edit_in_place, args.lower_suffix,
        )

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
