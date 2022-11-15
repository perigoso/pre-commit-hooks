#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>
from __future__ import annotations

import unittest

from hooks.check_accidental_assignment import check_accidental_assignment
from tests.test_cases_check_accidental_assignment import test_cases


class TestCheckAccidentalAssignment(unittest.TestCase):

    def test_check_accidental_assignment(self):
        failed = False

        for test_name, expected, args, input in test_cases:
            print(f'Running test: {test_name} ... ', end='')

            with open('tempfile', 'w') as f:
                f.write(input)

            result = check_accidental_assignment(
                'tempfile', quiet=True, **args,
            ) == 0

            if result != expected:
                failed = True
                print('FAIL')
            else:
                print('PASS')

        self.assertEqual(failed, False)


if __name__ == '__main__':
    unittest.main()
