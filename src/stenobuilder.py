#!/usr/bin/env python3
from util import *
from pyx.metapost.path import (
    beginknot,
    endknot,
    smoothknot,
    roughknot,
    tensioncurve,
    controlcurve,
    line,
)
import pyx
import math

from path_expression_parser import create_path_expression_parser

from collections import defaultdict

class KeyBasedDefaultDict(defaultdict):
    def __missing__(self, key):
        if key in ('path', 'glyph'):
            value = []
        elif key == 'tag':
            value = set()
        elif key == 'variable':
            value = {}
        else:
            value = KeyBasedDefaultDict()

        self[key] = value
        return value

    def __repr__(self):
            return dict(self).__repr__()

class ShorthandDefBuilder:
    def __init__(self):
        self.pool = KeyBasedDefaultDict()

    def char(self, name):
        return ShorthandCharBuilder(self, name)

    def build(self):
        return self.pool

class ShorthandCharBuilder:
    def __init__(self, parent, name):
        self.pool = KeyBasedDefaultDict()
        self.name = name
        self.parent = parent

    def _flush(self):
        self.parent.pool['character'][self.name] = self.pool

    def char(self, name):
        self._flush()
        return self.parent.char(name)

    def tag(self, *tags):
        self.pool["tag"].update(tags)
        return self

    def glyph(self, key):
        return ShorthandGlyphBuilder(self, key)

    def build(self):
        self._flush()
        return self.parent.build()

class ShorthandGlyphBuilder:
    def __init__(self, parent, key):
        self.gdef = KeyBasedDefaultDict()
        self.parent = parent
        self.key = key
        self.pool = {
            'key': key,
            'path': [],
            'dx': 0,
            'dy': 0,
            'ascent': 0,
            'top': 0,
            'bottom': 0,
            'left': 0,
            'right': 0,
        }

    def _flush(self):
        self.parent.pool['glyph'].append(self.gdef)

    def char(self, name):
        self._flush()
        return self.parent.char(name)

    def tag(self, *tags):
        self.gdef["tag"].update(tags)
        return self

    def path(self, path):
        self.pool["path"].append(path)
    #    #self._glyph["path"].append(path)
        return self

    #def dot(self, path):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    #TODO create_dot_glyph
    #    self._glyph.append(path)
    #    return self

    #def pathd(self, *pathd):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph["path"].extend(path)
    #    return self

    #def dx(self, dx):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.dx = dx

    #def dy(self, dy):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.dy = dy

    #def ascent(self, ascent):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.ascent = ascent

    #def top(self, top):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.top = top

    #def bottom(self, bottom):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.bottom = bottom

    #def left(self, left):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.left = left

    #def right(self, right):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    self._glyph.right = right

    def build(self):
        self._flush()
        return self.parent.build()


class ShorthandItemBuilder:
    def __init__(self):
        self.pool = KeyBasedDefaultDict()
        self._char_name = None
        self._char = None
        self._glyph = None

    def char(self, name):
        self._char_name = name
        self._glyph = None
        self._char = self.pool["character"][name]
        return self

    def variable(self, name, value):
        self.pool["variable"][name] = value
        return self

    def glyph(self, glyph):
        self._char["glyph"].append(glyph)
        return self

    def path(self, path):
        assert self._glyph is not None, "Target glyph is not detected"
        #TODO create_glyph
        self._char["path"].append(create_glyph(path))
        #self._glyph["path"].append(path)
        return self

    def dot(self, path):
        assert self._glyph is not None, "Target glyph is not detected"
        #TODO create_dot_glyph
        self._glyph.append(path)
        return self

    def pathd(self, *pathd):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph["path"].extend(path)
        return self

    def dx(self, dx):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.dx = dx

    def dy(self, dy):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.dy = dy

    def ascent(self, ascent):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.ascent = ascent

    def top(self, top):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.top = top

    def bottom(self, bottom):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.bottom = bottom

    def left(self, left):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.left = left

    def right(self, right):
        assert self._glyph is not None, "Target glyph is not detected"
        self._glyph.right = right

    def tag(self, *tags):
        if self._glyph is not None:
            self._glyph["tag"].update(tags)
        else:
            self._char["tag"].update(tags)
        return self


    def build(self):
        return self.pool


if __name__ == '__main__':
    builder = ShorthandDefBuilder()

    vdict = builder.pool['variable']
    parser = create_path_expression_parser(vdict)
    set_path_expression_parser(parser)
    res = (
        builder
        .char("A")
        .tag("a")
        .tag("el4")
        .glyph("el4")
        .path("O{-30} .. {90}4E")
        #.variable("a_head_angle", -30)
        #.glyph(create_glyph("O{a_head_angle} .. {90}4E", "@head_er8[1]"))

        .char("I")
        .tag("i")
        .tag("er4")

    ).build()
    print(res)


