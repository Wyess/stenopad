#!/usr/bin/env python3

import unittest
from glyph import create_ligature_keys

class TestLigatureKeys(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_3_char_ligature(self):
        keys = ["ya", "shihenki", "head_e"]
        lig_keys = create_ligature_keys(keys)
        self.assertEqual(lig_keys, ['shihenki[1].head_e[2]', 'ya[-1].head_e[1]', 'ya[-2].shihenki[-1]'])

if __name__ == '__main__':
    unittest.main()
