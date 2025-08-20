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

    def test_parse_tension(self):
        code = "tension 1.2"
        res = Parser(code).parse_tension()
        self.assertEqual(res, ("TENSION", (1.2, 1.2)))

    def test_parse_tension2(self):
        code = "tension 1.2 and 1.5"
        res = Parser(code).parse_tension()
        self.assertEqual(res, ("TENSION", (1.2, 1.5)))
