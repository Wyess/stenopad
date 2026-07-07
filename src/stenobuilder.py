#!/usr/bin/env python3

from dependency_resolver import resolve_dependencies, Reference
from dataclasses import dataclass, field, asdict, is_dataclass, fields
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
from metasteno import Point as z, Path, Point

from path_expression_parser import create_path_expression_parser

from collections import defaultdict

class KeyBasedDefaultDict(defaultdict):
    def __missing__(self, key):
        if key == 'glyph':
            value = []
        elif key == 'tag':
            value = set()
        elif key == 'path':
            value = {}
        elif key == 'dictionary':
            value = {}
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

    def path(self, name, path):
        self.pool["path"][name] = path
        return self

    def variable(self, name, val):
        self.pool["variable"][name] = val
        return self

    def word(self, index, *chars):
        self.pool["dictionary"][index] = [*chars]
        return self

    def _convert_paths_in_glyph(self, glyph_data):
        """引数で渡されたグリフデータ（辞書）内の path を SVG 文字列に置換するヘルパー"""
        if glyph_data and 'path' in glyph_data:
            glyph_data['path'] = [
                p.resolve() if type(p).__name__ == "Path" else p
                for p in glyph_data['path']
            ]

    def build(self):
        #return self.pool
        resolved_result = resolve_dependencies(self.pool)
        for char_key, char_content in resolved_result.get('character', {}).items():

            if 'default_glyph' in char_content and char_content['default_glyph'] is not None:
                self._convert_paths_in_glyph(char_content['default_glyph'])

            if 'glyphs' in char_content and isinstance(char_content['glyphs'], list):
                for sub_glyph in char_content['glyphs']:
                    self._convert_paths_in_glyph(sub_glyph)

        return resolved_result




class ShorthandCharBuilder:
    def __init__(self, parent, name):
        #self.pool = KeyBasedDefaultDict()
        self._char = Character(name)
        self.name = name
        self.parent = parent

    def _flush(self):
        #self.parent.pool['character'][self.name] = self.pool
        self.parent.pool['character'][self.name] = smart_asdict(self._char)

    def __getattr__(self, name):
        if hasattr(self.parent, name):
            def wrapper(*args, **kwargs):
                self._flush()
                return getattr(self.parent, name)(*args, **kwargs)
            return wrapper
        raise AttributeError(name)

    def tag(self, tag):
        self._char.tag.add(tag)
        return self

    def ascent(self, ascent):
        self._char.ascent = ascent
        return self

    def glyph(self, key="default"):
        return ShorthandGlyphBuilder(self, key)

    def append_glyph(self, glyph):
        if glyph.key == 'default':
            assert self._char.default_glyph is None, f"Default glyph is already set for <{self.name}>"
            self._char.default_glyph = glyph
        else:
            self._char.glyphs.append(glyph)


def smart_asdict(obj):
    if isinstance(obj, (Path, Point)):
        return obj

    if isinstance(obj, (list, tuple)):
        return type(obj)(smart_asdict(i) for i in obj)

    if isinstance(obj, dict):
        return {k: smart_asdict(v) for k, v in obj.items()}

    if is_dataclass(obj):
        return {f.name: smart_asdict(getattr(obj, f.name)) for f in fields(obj)}

    return obj


@dataclass(slots=True)
class Glyph:
    key: str
    path: list[str] = field(default_factory=list)
    tag: set[str] = field(default_factory=set)
    dx: float = 0.0
    dy: float = 0.0
    ascent: float = 0.0
    top: float = 0.0
    bottom: float = 0.0
    left: float = 0.0
    right: float = 0.0

@dataclass(slots=True)
class Character:
    name: str
    ascent: float = 0.0
    tag: set[str] = field(default_factory=set)
    default_glyph: Glyph | None = None
    glyphs: list[Glyph] = field(default_factory=list)

class ShorthandGlyphBuilder:
    def __init__(self, parent, key):
        self.pool = KeyBasedDefaultDict()
        self.parent = parent
        self.key = key
        self._glyph = Glyph(key)

    def _flush(self):
        self.parent.append_glyph(self._glyph)

    def __getattr__(self, name):
        if hasattr(Glyph, name):
            def wrapper(val):
                setattr(self._glyph, name, val)
                return self
            return wrapper
        if hasattr(self.parent, name):
            def func(*args, **kwargs):
                self._flush()
                return getattr(self.parent, name)(*args, **kwargs)
            return func
        raise AttributeError(name)

    def tag(self, tag):
        self._glyph.tag.add(tag)
        return self

    def path(self, path):
        self._glyph.path.append(path)
        return self

    #def dot(self, path):
    #    assert self._glyph is not None, "Target glyph is not detected"
    #    #TODO create_dot_glyph
    #    self._glyph.append(path)
    #    return self

    def pathd(self, *pathd):
        self._glyph.path.extend(path)
        return self

def ref(target: str):
    if target.startswith("$"):
        target = "variable." + target[1:]
    elif target.startswith("c."):
        target = "character." + target[2:]

    return Reference(target)

def vref(target: str):
    return Reference(f"variable.{target}")

def pref(target: str):
    return Reference(f"path.{target}")

if __name__ == '__main__':
    builder = ShorthandDefBuilder()

    res = (
        builder
        .char("A")
            .tag("a")
            .tag("el4")
            .ascent(0)
            .glyph()
                .path(pref("foo") >> {-90}@z[10, 11])
        .word("あ",  "A")

        .path('foo', z[0]@{vref("aha")} >> 1.1 >> {90}@z[4])
        .char("I")
            .tag("i")
            .tag("er4")
            .glyph()
        .char("U")

        .variable("iha", 30)
        .variable("aha", -30)
    ).build()
    print(res)


