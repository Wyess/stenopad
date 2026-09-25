#!/usr/bin/env python3

from dependency_resolver import resolve_dependencies, Reference
from dataclasses import dataclass, field, asdict, is_dataclass, fields
from metasteno import Point as z, Path, Point

import re
from collections import defaultdict
import pyx
from cmath import rect
from math import radians
from typing import Callable, Any

from pyx.metapost.path import (
    #beginknot,
    #endknot,
    smoothknot,
    #roughknot,
    tensioncurve,
    #controlcurve,
    #line,
)
from model2tags import model2tags

from waseda.waseda_lc import waseda_lc, path_lc_l_0

#print("pyx:", getattr(pyx, "__file__")


def constant_profile(c):
    assert 0 <= c <= 1.0
    return lambda t: c

def late_taper_profile(n=6):
    return lambda t: 1.0 - (t ** n)

def abrupt_taper_profile(threshold=0.8):
    return lambda t: 1.0 if t < threshold else 1.0 - (t - threshold) / (1.0 - threshold)

def bow_profile():
    return lambda t: math.sin(t * math.pi)

def linear_taper_profile():
    return lambda t: 1.0 - t


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

def cref(target: str):
    return Reference(f"character.{target}")

def aref(target: str):
    return Reference(f"character.{target}")["ascent"]

class ShorthandDefBuilder:
    def __init__(self):
        self.pool = KeyBasedDefaultDict()
    
    def root(self):
        return self

    def char(self, name, add_name_tag=True):
        return ShorthandCharBuilder(self, name, add_name_tag)

    def mark(self, name, add_name_tag=True):
        return ShorthandCharBuilder(self, name, add_name_tag, add_mark_tag=True)

    def path(self, name, path):
        self.pool["path"][name] = path
        return self

    def variable(self, **kwargs):
        for k, v in kwargs.items():
            self.pool["variable"][k] = v
        return self

    var = variable

    def word(self, index, *chars):
        self.pool["dictionary"][index] = chars
        return self

    def create_bbox(self, mpaths):
        bbox = sum(
            [mpath.bbox() for mpath in mpaths],
            start=pyx.bbox.empty()
        )
        u = pyx.unit.length(1)
        return {
            "top": -bbox.top() / u,
            "bottom": -bbox.bottom() / u,
            "left": bbox.left() / u,
            "right": bbox.right() / u,
        }

    def _convert_paths_in_glyph(self, glyph_data):
        try:
            mpaths = [
                p.create_metapost_path()
                for p in glyph_data.get('path', [])
            ]
        except:
            return

        if not mpaths:
            return

        if glyph_data["flick"]:
            # TODO: Exact rotation for 90*n degrees
            r = glyph_data["flick_len"]
            tan = mpaths[-1].tangent(mpaths[-1].end(), r)
            ex, ey = tan.atend()
        else:
            ex, ey = mpaths[-1].atend()

        u = pyx.unit.length(1)
        dx, dy = ex / u, ey / u
        glyph_data["dx"] += +dx
        glyph_data["dy"] += -dy
        glyph_data['path'] = [
            {
                'd': m.returnSVGdata(),
                'length': m.arclen() / u
            } for m in mpaths
        ]
        bbox = self.create_bbox(mpaths)
        glyph_data['top'] = bbox['top']
        glyph_data['bottom'] = bbox['bottom']
        glyph_data['left'] = bbox['left']
        glyph_data['right'] = bbox['right']

        if glyph_data["contour_func"] is not None:
            for m in mpaths:
                c = create_contour(m, taper_profile=glyph_data["contour_func"])
                glyph_data["clip_path"].append({"d": c.returnSVGdata()})
        del glyph_data["contour_func"]

        if len(glyph_data["tag"]) == 0:
            del glyph_data["tag"]

    def build(self):
        res = resolve_dependencies(self.pool)
        char_dict = res.get('character', {})

        for char in char_dict.values():
            glyph = char.get('default_glyph')
            if glyph:
                self._convert_paths_in_glyph(glyph)

            glyphs = char.get('glyphs', [])
            for glyph in glyphs:
                self._convert_paths_in_glyph(glyph)
        return res


def camel_to_snake(text):
    pattern = re.compile(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
    return pattern.sub('_', text).lower()


class ShorthandCharBuilder:
    def __init__(self, parent, name, add_name_tag=True, add_mark_tag=False):
        self._char = Character(name, default_glyph=Glyph("default"))
        self.name = name
        self.parent = parent
        if add_name_tag:
            self.tag(camel_to_snake(self.name))
        if add_mark_tag:
            self.tag("mark")

        self.is_default_glyph_set = False

    def _flush(self):
        #assert  self.name not in self.parent.pool['character'], f"{self.name} is already defined"
        if self.name in self.parent.pool['character']:
            self.parent.pool['character'][self.name]["tag"].update(self._char.tag)
            self.parent.pool['character'][self.name]["glyphs"].extend(smart_asdict(self._char.glyphs))
        else:
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

    def model(self, model):
        tags = model2tags(model)
        for tag in tags:
            self.tag(tag)
        return self

    def ascent(self, ascent):
        if isinstance(ascent, str):
            self._char.ascent = aref(ascent)
        else:
            self._char.ascent = ascent
        return self

    def glyph(self, key="default"):
        return ShorthandGlyphBuilder(self, key, ascent=self._char.ascent)

    def append_glyph(self, glyph):
        if glyph.key == 'default':
            assert not self.is_default_glyph_set, f"{self.name}: default glyph is already set"
            self._char.default_glyph = glyph
            self.is_default_glyph_set = True
        else:
            self._char.glyphs.append(glyph)


def smart_asdict(obj):
    if isinstance(obj, (Path, Point)):
        return obj

    if isinstance(obj, (list, tuple, set)):
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
    clip_path: list[str] = field(default_factory=list)
    contour_func: Callable | None = None
    tag: set[str] = field(default_factory=set)
    dx: float = 0.0
    dy: float = 0.0
    flick: bool = False
    flick_len: float = 0.0
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
    def __init__(self, parent, key, ascent=0):
        self.parent = parent
        self.key = key
        self._glyph = Glyph(key, ascent=ascent)

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

    def model(self, model):
        tags = model2tags(model)
        for tag in tags:
            self._glyph.tag.add(tag)
        return self

    def offset(self, x, y=0, a=None):
        # TODO: exact 90n rotations
        # Round to zero when too small?
        if a is not None:
            z = complex(x, y) * rect(1, radians(a))
            x, y = z.real, z.imag
        #x = max(x, 1e-3)
        #y = max(y, 1e-3)
        self._glyph.dx += +x
        self._glyph.dy += -y
        return self

    def flick(self, r=1, profile_func=late_taper_profile()):
        self._glyph.contour_func = profile_func
        self._glyph.flick = True
        self._glyph.flick_len = r
        return self


    def path(self, path):
        if isinstance(path, str):
            self._glyph.path.append(pref(path))
        else:
            self._glyph.path.append(path)
        return self

    def pos(self, x, y=None):
        if y is None:
            x, y = x.real, x.imag
        self._glyph.path.append({'d': f'M0 0', 'length': 0})
        self._glyph.dx = +x
        self._glyph.dy = -y
        self._glyph.ascent = 0
        self._glyph.top = y
        self._glyph.bottom = y
        self._glyph.left = x
        self._glyph.right = x
        return self

    def dot(self, x, y=None, r=0.08):
        path = (
            z[x, y + r]@{0} >>
            z[x + r, y] >>
            z[x, y - r] >>
            z[x - r, y] >>
            {0}@z[x, y + r]
        )
        return self.path(path)

    def width(self, profile_func):
        self._glyph.contour_func = profile_func
        return self

    def pathd(self, *pathd):
        self._glyph.path.extend(path)
        return self

#0.425197
def create_contour(pyx_path, steps=20, max_width=0.45/2.0, taper_profile=linear_taper_profile()):
    total_length = pyx_path.arclen()
    pts1 = []
    pts2 = []

    for i in range(steps + 1):
        current_len = total_length * (i / steps)
        t = pyx_path.arclentoparam(current_len)

        w = max_width * taper_profile(i / steps)
        tan = pyx_path.tangent(t, w)
        ex, ey = tan.atend()
        x, y = tan.atbegin()
        tx, ty = ex - x, ey - y

        nx, ny = -ty, tx
        x_end = x + nx
        y_end = y + ny
        pts1.append((x_end, y_end))

        nx2, ny2 = ty, -tx
        x_end2 = x + nx2
        y_end2 = y + ny2
        pts2.append((x_end2, y_end2))

    me = [smoothknot(*pts1[0])]

    for pt in pts1[1:]:
        me.append(tensioncurve())
        me.append(smoothknot(*pt))

    for pt in pts2[::-1]:
        me.append(tensioncurve())
        me.append(smoothknot(*pt))

    tan = pyx_path.tangent(0, max_width)
    end = tan.atend()
    me.append(tensioncurve())
    me.append(smoothknot(-end[0], -end[1]))
    me.append(tensioncurve())

    return pyx.metapost.path.path(me)

def path_horseshoe(len_=4, angle=-30, tension=1.5, rotation=-1, opening=2, head_angle=110):
    return (
        z[0]@{head_angle + angle} >>
        tension >>
        {angle}@z[
            len_,
            rotation * opening / 2:
            -90 * rotation + angle
        ] >>
        tension >>
        z[opening: angle]
    )

def path_rice(len_=4, angle=0, head_angle=-20, tail_angle=20, width=1):
    #.path("hodo", z[0]@{-20} >> {0}@z[3, -0.5] >> {90}@z[4, 0] >> {180}@z[3, 0.5] >> {180 + 20}@z[0])
    rotation = 1 if tail_angle >= head_angle else -1
    half_width = width / 2 * rotation
    return (
        z[0]@{head_angle + angle} >>
        {angle}@z[len_ * 0.75, -half_width: angle] >>
        {rotation * 90 + angle}@z[len_: angle] >>
        {180 + angle}@z[len_ * 0.75, half_width: angle] >>
        {180 + tail_angle + angle}@z[0]
    )


if __name__ == '__main__':
    builder = ShorthandDefBuilder()

    builder = (
        builder

        .var(iha=30)
        .word("a", "a")
        .path("A:@head_er4", pref("a~")@{vref("iha")})
        .path('a~', z[0]@{-30} >> 1.1 >> z[4])

        .char("A")
            .glyph()
                .path("A:@head_er4")
    )

    res = builder.build()

    del res["path"]
    del res["variable"]
    trie = {}
    for key in res["dictionary"]:
        node = trie
        for char in key:
            node = node.setdefault(char, {})
        node['word'] = key
    res["trie"] = trie
    res = {"waseda": res}

    import json

    def default(obj):
        if isinstance(obj, set):
            return {key: None for key in obj}
        raise TypeError(f'Cannot serialize object of {type(obj)}')
    j = json.dumps(res, default=default, ensure_ascii=False)
    with open("waseda.json", "w") as f:
        f.write(j)


