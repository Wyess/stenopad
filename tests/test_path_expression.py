#!/usr/bin/env python3

from path_expression_parser import parse_path_expression as parse

import unittest

class PathExpressionTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDowon(self):
        pass

    def test_empty_string(self):
        res = parse('')
        self.assertEqual(res, [])

    def test_unit_line(self):
        res = parse('(0, 0) -- (1, 0)')[0][0]
        exp = 'normpath([normsubpath([normline_pt(0, 0, 1, 0)])])'
        self.assertEqual(str(res), exp)

    def test_basic_curve(self):
        res = parse('(0, 0){0} .. (1, 0)')[0][0]
        exp = 'normpath([normsubpath([normcurve_pt(0, 0, 0.333333, 0, 0.666667, 0, 1, 0)])])'
        self.assertEqual(str(res), exp)


if __name__ == '__main__':
    unittest.main()
