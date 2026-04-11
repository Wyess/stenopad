#!/usr/bin/env python3

import unittest
from character import Character
from glyph_selector_parser import parse_glyph_selector

class GlyphSelectorTest(unittest.TestCase):
    sdict = {
        'character': {
            'ya': {
                'tag': {
                    'ya',
                    '@head_ner',
                },
                'glyph': [None],
            },
            'shihenki': {
                'tag': {
                    'shihenki',
                    '@head_swr',
                },
                'glyph': [None],
            },
            'ka': {
                'tag': {
                    'ka',
                    '@head_e',
                },
                'glyph': [None],
            },
        },
    }

    def setUp(self):
        pass

    def tearDow(self):
        pass

    def test_after(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
        ]
        res = parse_glyph_selector("shihenki[1]", chars, 0)
        self.assertTrue(res)

    def test_after_false(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
        ]
        res = parse_glyph_selector("sahenki[1]", chars, 0)
        self.assertFalse(res)

    def test_before(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
        ]
        res = parse_glyph_selector("ya[-1]", chars, 1)
        self.assertTrue(res)

    def test_before_false(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
        ]
        res = parse_glyph_selector("yo[-1]", chars, 1)
        self.assertFalse(res)

    def test_before_or_after(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
            Character('ka', self.sdict),
        ]
        res = parse_glyph_selector("yo[-1]|ka[1]", chars, 1)
        self.assertTrue(res)
        res = parse_glyph_selector("ya[-1]|ki[1]", chars, 1)
        self.assertTrue(res)
        res = parse_glyph_selector("ya[-1]|ka[1]", chars, 1)
        self.assertTrue(res)

    def test_before_or_after_false(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
            Character('ka', self.sdict),
        ]
        res = parse_glyph_selector("yo[-1]|ki[1]", chars, 1)
        self.assertFalse(res)
    
    def test_before_and_after(self):
        chars = [
            Character('ya', self.sdict),
            Character('shihenki', self.sdict),
            Character('ka', self.sdict),
        ]
        res = parse_glyph_selector( "ya[-1].@head_e[1]", chars, 1)
        self.assertTrue(res)

    def test_eos(self):
        chars = [Character('ya', self.sdict)]
        res = parse_glyph_selector("eos[1]", chars, 0)
        self.assertTrue(res)
        res = parse_glyph_selector("eos[0]", chars, 0)
        self.assertFalse(res)
        res = parse_glyph_selector("eos[-1]", chars, 0)
        self.assertFalse(res)

    def test_sos(self):
        chars = [Character('ya', self.sdict)]
        res = parse_glyph_selector("sos[-1]", chars, 0)
        self.assertTrue(res)
        res = parse_glyph_selector("sos[0]", chars, 0)
        self.assertFalse(res)
        res = parse_glyph_selector("sos[1]", chars, 0)
        self.assertFalse(res)

if __name__ == '__main__':
    unittest.main()
