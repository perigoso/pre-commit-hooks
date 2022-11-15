#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import argparse
from typing import Sequence


def check_accidental_assignment(filename: str) -> int:
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= check_accidental_assignment(filename)

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
