#!/usr/bin/env python3

import unittest
from path_expression_parser import parse_path_expression, move

def export_paths(paths):
    path_lists = []
    buf = []
    for path in paths:
        buf.append(path['path_split'][0])
        if len(path['path_split']) > 1:
            path_lists.append(buf)
            path_lists.extend([[p] for p in path['path_split'][1:-1]])
            buf = [path['path_split'][-1]]
    if buf:
        path_lists.append(buf)

    for i, paths in enumerate(path_lists):
        x, y = paths[0].atbegin()
        path_lists[i] = [move(path, -x, -y) for path in paths]

    return path_lists

def export(paths):
    ret = []
    buf = []
    for path in paths:
        if len(path) == 1:
            buf.append(path)
        else:
            buf.append(path[0])
            ret.append(buf)
            ret.extend([[c] for c in path[1:-1]])
            buf = [path[-1]]
    if buf:
        ret.append(buf)
    return ret

class ExporterTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        self.assertEqual(export([]), [])

    def test_single(self):
        self.assertEqual(export(['a']), [['a']])

    def test_single_split2(self):
        self.assertEqual(export(['ab']), [['a'], ['b']])

    def test_single_split3(self):
        self.assertEqual(export(['abc']), [['a'], ['b'], ['c']])

    def test_path_expr_1(self):
        code = "O -- E"
        paths = parse_path_expression(code)
        ret = export_paths(paths)
        self.assertEqual(len(ret), 1)
        self.assertEqual(len(ret[0]), 1)

    def test_path_expr_2(self):
        code = "O -- +4E 2S -- ++4E"
        paths = parse_path_expression(code)
        ret = export_paths(paths)
        print(ret[0][0].returnSVGdata())
        print(ret[0][1].returnSVGdata())
        self.assertEqual(len(ret), 1)
        self.assertEqual(len(ret[0]), 2)

    def test_path_expr_1_split(self):
        code = "O -- ++4E & O -- +8S"
        paths = parse_path_expression(code)
        ret = export_paths(paths)
        print(ret[0][0].returnSVGdata())
        print(ret[1][0].returnSVGdata())
        self.assertEqual(len(ret), 2)
        self.assertEqual(len(ret[0]), 1)
        self.assertEqual(len(ret[1]), 1)

    def test_path_expr_2_split(self):
        code = "O -- +4E 2S -- ++4E & O--4S"
        paths = parse_path_expression(code)
        ret = export_paths(paths)
        self.assertEqual(len(ret), 2)
        self.assertEqual(len(ret[0]), 2)
        self.assertEqual(len(ret[1]), 1)

if __name__ == '__main__':
    unittest.main()
