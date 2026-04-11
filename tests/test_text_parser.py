#!/usr/bin/env python3

import unittest
from text_parser import parse_text

class TextParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_string(self):
        wdict = {
            'a': 'A'
        }
        text = ''
        res = parse_text(text, wdict)
        self.assertEqual(res, [])

    def test_char_in_dict(self):
        wdict = {
            'a': 'A'
        }
        text = 'a'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['A'])

    def test_char_not_in_dict(self):
        wdict = {
            'a': 'A'
        }
        text = 'b'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['Null'])

    def test_space(self):
        wdict = {
            'a': 'A'
        }
        text = 'a a'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['A', 'Space', 'A'])

    def test_trailing_space(self):
        wdict = {
            'a': 'A'
        }
        text = 'a   '
        res = parse_text(text, wdict)
        self.assertEqual(res, ['A'])

    def test_word_in_dict(self):
        wdict = {
            'word': 'W'
        }
        text = 'word'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['W'])

    def test_word_not_in_dict(self):
        wdict = {
            'word': 'W'
        }
        text = 'foo'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['Null'])

    def test_word_fallback_full(self):
        wdict = {
            'w': 'W',
            'o': 'O',
            'r': 'R',
            'd': 'D',
        }
        text = 'word'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['W', 'O', 'R', 'D'])

    def test_word_fallback_partial(self):
        wdict = {
            'w': 'W',
            'o': 'O',
            'r': 'R',
            #'d': 'D',
        }
        text = 'word'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['W', 'O', 'R', 'Null'])

    def test_separator(self):
        wdict = {
            'SEPARATOR': '/',
            '$slash': '/',
            'w': 'W',
            'o': 'O',
            'r': 'R',
            'd': 'D',
            'word': 'Word',
            'or': 'Or',
        }
        text = '/w/or//d/$slash/'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['W', 'Or', 'D', '/'])

    def test_multi_char_entry(self):
        wdict = {
            'word': ('W', 'O', 'R', 'D'),
        }
        text = 'word word'
        res = parse_text(text, wdict)
        self.assertEqual(res, ['W', 'O', 'R', 'D', 'Space', 'W', 'O', 'R', 'D'])

if __name__ == '__main__':
    unittest.main()
