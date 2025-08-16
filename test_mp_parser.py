#!/usr/bin/env python3

from mp_parser import Parser
import unittest

class MpParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_path_expression_empty(self):
        code = ""
        res = Parser(code).parse()
        self.assertEqual(res, [])

    def test_path_expression_origin(self):
        code = "(0, 0)"
        res = Parser(code).parse()
        self.assertEqual(res, [("KNOT", (0, 0))])
