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
        .word("SEPARATOR", "・")
        .char("Null")
            .glyph()
                .path({'d': 'M2 -2v4h4v-4h-4l4 4', 'length': 0}) 
                .dx(8)
                .dy(0)
                .right(8)

        .char("Space")
            .glyph()
                .dx(4)
                .dy(0)

        .char("Newline")

        # @head_el4[0]: a
        .word("あ", "A")
        .var(aha=-30, atn=1.1, ata=90)
        .path('a', pref("a~")@{90})
        #.path("A:@head_er4", pref("a~")@{vref("iha")})
        .path('a~', z[0]@{-30} >> 1.1 >> z[4])

        .char("A")
            .model("el4")
            .glyph()
                .path("a")
            #.glyph("@head_er4[1]")
            #    .path("A:@head_er4")


        .word("あん", "An")
        .path('an', pref("a~")@{60})
        .char("An")
            .tag("el4f")
            .glyph()
                .path("an")
                .flick(2)

        # @head_er4[0]: i
        .word("い", "I")
        .var(iha=30)
        .path("i", pref("i~")@{-90})
        .path("i~", z[0]@{vref("iha")} >> 1.1 >> z[4])
        .char("I")
            .model("er4")
            .glyph()
                .path("i")

        .word("いん", "In")
        .path("in", pref("i") -- +z[2: 45])
        .char("In")
            .model("er4ne1f")
            .glyph()
                .path("in")
                .flick(2)

        # @head_s[0]: u
        .word("う", "U")
        .word("たい", "U")
        .path("u", z[0] -- z[-4j])
        .path("u.jog()", pref("u") -- +z[:70])
        .char("U")
            .ascent(2)
            .model("s4")
            .glyph()
                .path("u")
            .glyph("@head_s[1]")
                .path("u.jog()")

        .word("うう", "Uu")
        .word("うー", "Uu")
        .path("uu", pref("kei") * (1, 1, -90))
        .path("uu.@head_s[1]",
             path_lc_l_0(len_=4, angle=-90)
        )
        .char("Uu")
            .ascent("U")
            .model("s4cl1")
            .glyph()
                .path("uu")
            .glyph("@head_s[1]")
                .path("uu.@head_s[1]")

        .word("つ", "Tsu")
        .path("tsu", pref("kei") * (1, -1, -90))
        .char("Tsu")
            .ascent("U")
            .model("s4cr1")
            .glyph()
                .path("tsu")

        .word("ことです", "Kotodesu")
        .path("kotodesu", pref("ki") * (1, -1, -90))
        .char("Kotodesu")
            .ascent("Koto")
            .model("s8cr1")
            .glyph()
                .path("kotodesu")

        .word("てい", "Tei")
        .path("tei", pref("kei") * (1, -1, -120))
        .char("Tei")
            .ascent("O")
            .model("sw4cr1")
            .glyph()
                .path("tei")

        .word("つまら","Tsumara")
        .word("つまり","Tsumara")
        .word("つもり","Tsumara")
        .path("tsumara", pref("ku") * (1, -0.8, -120))
        .char("Tsumara")
            .ascent("Ta")
            .model("sw8cr4")
            .glyph()
                .path("tsumara")

        .word("えい", "Ei")
        .word("ええ", "Ei")
        .word("えー", "Ei")
        .path("ei", pref("kei") * (1, -1, -55))
        .char("Ei")
            .ascent("E")
            .model("se4cr1")
            .glyph()
                .path("ei")

        .word("とり", "Tori")
        .word("とれ", "Tore")
        .path("tori", pref("ki") * (1, 1, -90))
        .char("Tori")
            .ascent("Koto")
            .model("s8cl1")
            .glyph()
                .path("tori")

        .word("とる", "Toru")
        .word("とら", "Toru")
        .word("ことば", "Toru")
        .path("toru", pref("ku") * (1, 0.8, -90))
        .char("Toru")
            .ascent("Koto")
            .model("s8cl4")
            .glyph()
                .path("toru")

        .word("うん", "Un")
        .word("くん", "Un")
        .path("un", pref("u")@{60} >> +z[2: 45])
        .char("Un")
            .ascent("U")
            .model("s4ne1f")
            .glyph()
                .path("un")
                .flick(1.5)

        .word("にち", "Nichi")
        .char("Nichi")
            .ascent("U")
            .model("s4f")
            .glyph()
                .path("u")
                .flick(2)
        
        .word("こと", "Koto")
        .path("koto", z[0] -- z[-8j])
        .path("koto.jog()", pref("koto") -- +z[:70])
        .char("Koto")
            .ascent(4)
            .model("s8")
            .glyph()
                .path("koto")
            .glyph("@head_s[1]")
                .path("koto.jog()")

        .word("りつ", "Ritsu")
        .word("りち", "Ritsu")
        .word("たつ", "Ritsu")
        .char("Ritsu")
            .ascent("Koto")
            .model("s8f")
            .glyph()
                .path("koto")
                .flick(2)

        .word("れつ", "Retsu")
        .word("れち", "Retsu")
        .word("ず！", "Retsu")
        .path("retsu", z[0] -- z[-16j])
        .char("Retsu")
            .ascent(8)
            .model("s16f")
            .glyph()
                .path("retsu")
                .flick(2)

        .word("？れつ", "PosRetsu", "RetsuShort")
        .word("？れち", "PosRetsu", "RetsuShort")
        .char("RetsuShort")
            .ascent(4)
            .tag("xs8f")
            .tag("@head_s")
            .glyph()
                .path("koto")
                .flick(2)

        .char("PosRetsu")
            .glyph()
                .pos(-1.5, 1.5)

        # @head_se4[0]: e
        .word("え", "E")
        .path("e", z[0] -- z[4: -55])
        .path("e.jog()", pref("e") -- +z[:160 - 15])
        .char("E")
            .ascent(2)
            .model("se4")
            .glyph()
                .path("e")
            .glyph("@head_se[1]")
                .path("e.jog()")

        .word("せつ", "Setsu")
        .char("Setsu")
            .ascent("E")
            .model("se4f")
            .glyph()
                .path("e")
                .flick(2)

        .word("えん", "En")
        .path("en", pref("e")@{60} >> +z[2: 45])
        .char("En")
            .ascent("E")
            .model("se4ne1f")
            .glyph()
                .path("en")
                .flick(2)

        # @head_sw4[0]: o
        .word("お", "O")
        .path("o", z[0] -- z[-4: 60])
        .char("O")
            .ascent(2)
            .model("sw4")
            .glyph()
                .path("o")

        .word("おん", "On")
        .path("on", pref("o") -- +z[2: 30])
        .char("On")
            .ascent("O")
            .model("sw4ne1f")
            .glyph()
                .path("on")
                .flick(1.5)

        .word("しつ", "Shitsu")
        .word("つつ", "Shitsu")
        .word("ずつ", "Shitsu")
        .word("おら", "Shitsu")
        .word("おり", "Shitsu")
        .char("Shitsu")
            .ascent("O")
            .model("sw4f")
            .glyph()
                .path("o")
                .flick(1.5)

        .word("か", "Ka")
        .word("が", "Ka", "Dakuten")
        .path("ka", z[0] -- z[8])
        .path("ka.jog()", pref("ka") -- +z[:-160])
        .char("Ka")
            .model("e8")
            .glyph()
                .path("ka")
            .glyph("@head_e[1]")
                .path("ka.jog()")

        .word("こ", "Ko")
        .word("ご", "Ko", "Dakuten")
        .path("ko", z[0] -- z[16])
        .path("ko.jog()", pref("ko") -- +z[:-160])
        .char("Ko")
            .model("e16")
            .glyph()
                .path("ko")
            .glyph("@head_e[1]")
                .path("ko.jog()")

        .word("かい", "Kai")
        .word("がい", "Kai", "Dakuten")
        .path("kai", z[0] -- z[4])
        .path("kai.jog()", pref("kai") -- +z[:-160])
        .char("Kai")
            .model("e4")
            .glyph()
                .path("kai")
            .glyph("@head_e[1]")
                .path("kai.jog()")

        .word("日本", "Nihon")
        .path("nihon1", pref("kai"))
        .path("nihon2", pref("kai") @ z[0, -2])
        .path("nihon2.jog()", pref("kai.jog()") @ z[0, -2])
        .char("Nihon")
            .ascent(1)
            .tag("e4-e4")
            .tag("@head_e")
            .glyph()
                .path("nihon1")
                .path("nihon2")
            .glyph("@head_e[1]")
                .path("nihon1")
                .path("nihon2.jog()")

        .word("きん", "Kin")
        .char("Kin")
            .tag("e4f")
            .tag("@head_e")

            .glyph()
                .path("kai")
                .flick(3)

        .word("かり", "Kari")
        .char("Kari")
            .glyph()
                .path("ka")
                .flick(3)

        .word("ます", "Masu")
        .path("masu", z[0] -- z[25])
        .char("Masu")
            .glyph()
                .path("masu")
                .flick(3)

        # @head_ner16[0]: yo
        # pd["Yo"] = "O{70} .. tension 1.7 .. {0}(16: 45)"
        .word("よ", "Yo")
        .path("yo", z[0]@{90} >> 1.7 >> {0}@z[16: 45])
        .char("Yo")
            .ascent(-4)
            .tag("@head_ner16")
            .glyph()
                .path("yo")

        # @head_ner8[0]: ya
        # pd["Ya"] = "O{70} .. {0}(8: 40)"
        .word("や", "Ya")
        .path("ya", z[0]@{70} >> {0}@z[8: 40])
        .char("Ya")
            .ascent(-2)
            .tag("@head_ner8")
            .glyph()
                .path("ya")

        # @head_ner4[0]: yai
        .word("やい", "Yai")
        .path("yai", pref("ya") * 0.5)
        .char("Yai")
            .ascent(-2)
            .tag("@head_ner4")
            .glyph()
                .path("yai")

        # @head_ne25[0]: mashite
        .word("まして", "Mashite")
        .path("mashite", z[0] -- z[25: 40])
        .char("Mashite")
            .ascent(0)
            .tag("@head_ne25")
            .glyph()
                .path("mashite")
                .flick(2)

        # @head_ne16[0]: to
        .word("と", "To")
        .path("to", z[0] -- z[16: 40]) # 50deg
        .path("to_henki", z[0] -- z[-16: 60])
        .char("To")
            .ascent(-4)
            .model("ne16")
            .glyph()
                .path("to")
            .glyph("@tail_ne[-1]|@tail_e[-1]")
                .model("sw16")
                .path("to_henki")

        # @head_ne8[0]: cha
        # @head_ne8[0]: tahenki/sen2
        .word("ちゃ", "Cha")
        .path("cha", z[0] -- z[8: 22.5])
        .path("cha_henki", z[0] -- z[-8: 45])
        .char("Cha")
            .ascent(-2)
            .model("ne8")
            .glyph()
                .path("cha")
            .glyph("@head_ne[-1]")
                .model("sw8")
                .tag("cha_henki")
                .path("cha_henki")

        # @head_ne4[0]: koi
        .word("こい", "Koi")
        .word("こえ", "Koi")
        .word("こく", "Koi")
        .path("koi", z[0] -- z[4: 40]) # 30
        .char("Koi")
            .model("ne4")
            .ascent(0)
            .glyph()
                .path("koi")

        # @head_nel16[0]: so
        .word("そ", "So")
        .path("so~", z[0]@{30} >> 1.6 >> z[16: 45])
        .path("so", pref("so~")@{90})
        .path("so_henki~", z[0]@{-90} >> 1.6 >> z[16: -120])
        .path("so_henki", pref("so_henki~")@{180})
        .char("So")
            .model("nel16")
            .ascent(-4)
            .glyph()
                .path("so")
            .glyph("@head_e[-1]")
                .path("so_henki")

        # @head_nel8[0]: sa
        .word("さ", "Sa")
        .path("sa~", z[0]@{30} >> 1.3 >> z[8: 45])
        .path("sa", pref("sa~")@{90})
        .path("sa_henki~", z[0]@{-90} >> z[8: -120])
        .path("sa_henki", pref("sa_henki~")@{180})
        .char("Sa")
            .model("nel8")
            .ascent(-2)
            .glyph()
                .path("sa")
            .glyph("@head_e[-1]")
                .path("sa_henki")

        # @head_nel4[0]: soi
        .word("そい", "Soi")
        .word("そえ", "Soi")
        .path("soi~", z[0]@{30} >> z[4: 45])
        .path("soi", pref("soi~")@{90})
        .char("Soi")
            .ascent(-1)
            .model("nel4")
            .glyph()
                .path("soi")

        # @head_nel4[0]: soi
        .word("そこ", "Soko")
        .char("Soko")
            .ascent("Soi")
            .model("nel4f")
            .glyph()
                .path("soi")
                .flick(1.5)

        # @head_er25[0]: mashou
        .word("ましょう", "Mashou")
        .path("mashou", z[0]@{30} >> 1.3 >> {-30}@z[25])
        .char("Mashou")
            .model("er25f")
            .ascent(0)
            .glyph()
                .path("mashou")
                .flick(2)

        # @head_er16[0]: mo
        .word("も", "Mo")
        .path("mo~", z[0]@{30} >> 2.0 >> z[16])
        .path("mo", pref("mo~")@{-90})
        .char("Mo")
            .model("er16")
            .ascent(0)
            .glyph()
                .path("mo")

        # @head_er8[0]: ma
        .word("ま", "Ma")
        .path("ma~", z[0]@{30} >> 1.3 >> z[8])
        .path("ma", pref("ma~")@{-90})
        .char("Ma")
            .model("er8")
            .ascent(0)
            .glyph()
                .path("ma")

        # @head_el25[0]: naraba
        .word("ならば", "Naraba")
        .path("naraba", z[0]@{-30} >> 1.3 >> {30}@z[25])
        .char("Naraba")
            .ascent(0)
            .model("el25f")
            .glyph()
                .path("naraba")
                .flick(2)

        # @head_el16[0]: no
        .word("の", "No")
        .path("no~", z[0]@{-30} >> 2.0 >> z[16])
        .path("no", pref("no~")@{90})
        .char("No")
            .ascent(0)
            .model("el16")
            .glyph()
                .path("no")

        # @head_el8[0]: na
        .word("な", "Na")
        .path("na~", z[0]@{-30} >> 1.3 >> z[8])
        .path("na", pref("na~")@{90})
        .char("Na")
            .ascent(0)
            .model("el8")
            .glyph()
                .path("na")

        # @head_ser16[0]: ro
        .word("ろ", "Ro")
        .path("ro", z[0]@{-30} >> 1.5 >> {-120}@z[16: -60])
        .char("Ro")
            .ascent(8)
            .model("ser16")
            .glyph()
                .path("ro")

        # @head_ser8[0]: ra
        .word("ら", "Ra")
        .path("ra", z[0]@{-30} >> 1.2 >> {-120}@z[8: -60])
        .char("Ra")
            .ascent(4)
            .model("ser8")
            .glyph()
                .path("ra")

        # @head_ser4[0]: rai
        .word("らい", "Rai")
        .path("rai", z[0]@{-30} >> 1.2 >> {-120}@z[4: -60])
        .char("Rai")
            .ascent(2)
            .model("ser4")
            .glyph()
                .path("rai")


        # @head_se16[0]: subeki
        .word("すべき", "Subeki")
        .word("すべし", "Subeki")
        .path("subeki", z[0] -- z[16: -55])
        .path("subeki.jog()", pref("ketsu") -- +z[:160 - 15])
        .char("Subeki")
            .ascent(8)
            .model("se16")
            .glyph()
               .path("subeki")
            .glyph("@head_se[1]")
                .path("subeki.jog()")

        # @head_se8[0]: ketsu
        .word("けつ", "Ketsu")
        .path("ketsu", z[0] -- z[8: -40 - 15])
        .path("ketsu.jog()", pref("ketsu") -- +z[:160 - 15])
        .char("Ketsu")
            .ascent(4)
            .model("se8")
            .glyph()
               .path("ketsu")
            .glyph("@head_se[1]")
                .path("ketsu.jog()")
            

        # @head_se3[0]: shite
        .word("して", "Shite")
        .path("shite", z[0] -- z[3: -55])
        .path("shite.jog()", pref("shite") -- +z[:160-15])
        .char("Shite")
            .ascent(1)
            .model("se3")
            .glyph()
                .path("shite")
            .glyph("@head_se[1]")
                .path("shite.jog()")

        # @head_sel16[0]: ho
        .word("ほ", "Ho")
        .path("ho", z[0]@{-90} >> {0}@z[16: -60])
        .char("Ho")
            .ascent(8)
            .model("sel16")
            .glyph()
                .path("ho")

        # @head_sel8[0]: ha
        .word("は", "Ha")
        .path("ha", z[0]@{-90} >> {0}@z[8: -60])
        .char("Ha")
            .ascent(4)
            .model("sel8")
            .glyph()
                .path("ha")

        # @head_sel4[0]: hai
        .word("はい", "Hai")
        .path("hai", z[0]@{-90} >> {0}@z[4: -45])
        .char("Hai")
            .ascent(1)
            .model("sel4")
            .glyph()
                .path("hai")

        # @head_sr8[0]: sha
        .word("しゃ", "Sha")
        .path("sha~", z[0]@{-60} >> z[-8j])
        .path("sha", pref("sha~")@{-135})
        .char("Sha")
            .ascent(4)
            .tag("@head_sr8")
            .glyph()
                .path("sha")

        # @head_sl8[0]: kya
        .word("きゃ", "Kya")
        .path("kya~", z[0]@{-120} >> z[-8j])
        .path("kya", pref("kya~")@{-45})
        .char("Kya")
            .ascent(4)
            .tag("@head_sl8")
            .glyph()
                .path("kya")

        # @head_swr16[0]: sohenki
        # @head_swr8[0]: sahenki

        # @head_swr4[0]: node
        .word("ので", "Node")
        .path("node", z[0] >> {180}@z[-4: 45])
        .char("Node")
            .ascent(2)
            .model("swr4f")
            .glyph()
                .path("node")
                .flick(1.5)
            .glyph("@head_e[1]")
                .path("node")
                .flick(1.5)
                .offset(0, -1)
            .glyph("@head_er[1]")
                .path("node")
                .flick(1.5)
                .offset(0, -1.5)

        # @head_sw25[0]: masen
        .word("ません", "Masen")
        .path("masen", z[0] -- z[-25: 60])
        .char("Masen")
            .ascent(0)
            .model("sw25f")
            .glyph()
                .path("masen")
                .flick(2)

        # @head_sw16[0]: tohenki
        # @head_sw8[0]: ta
        # @head_sw8[0]: chahenki
        .word("た", "Ta")
        .path("ta", z[0] -- z[-8: 60])
        .path("ta_henki", z[0] -- z[8: 40])
        .path("ta_henki.jog", pref("ta_henki") -- +z[1: 240])
        .char("Ta")
            .ascent(4)
            .model("sw8")
            .glyph()
                .path("ta")
            .glyph("@tail_sw[-1].@head_ne[1]")
                .model("ne8")
                .tag("ta_henki")
                .path("ta_henki.jog")
            .glyph("@tail_sw[-1]")
                .model("ne8")
                .tag("ta_henki")
                .path("ta_henki")

        .word("せん２", "Sen2")
        .char("Sen2")
            .ascent(-2)
            .model("ne8f")
            .glyph()
                .path("ta_henki")
                .flick(2)

        .word("ち", "Chi")
        .path("chi", pref("ki") * (1, -1, -120))
        .path("chi_henki", pref("ki") * (1, 1, 40))
        .char("Chi")
            .ascent("Ta")
            .model("sw8cr1")
            .glyph()
                .path("chi")
            .glyph("@tail_sw[-1]")
                .path("chi_henki")

        # @head_swl16[0]: pu
        .word("ぷ", "Pu")
        .path("pu", z[0]@{-160} >> 1.5 >> {-85}@z[16: -120])
        .char("Pu")
            .ascent(8)
            .model("swl16")
            .glyph()
                .path("pu")

        .word("しき", "Shiki")
        .word("ひき", "Shiki")
        .char("Shiki")
            .ascent("Pu")
            .model("swl16f")
            .glyph()
                .path("pu")
                .flick(2)

        # @head_swl8[0]: hya
        .word("ひゃ", "Hya")
        .path("hya", z[0]@{-160} >> 1.5 >> {-70}@z[8: -120])
        .char("Hya")
            .ascent(4)
            .model("swl8")
            .glyph()
                .path("hya")

        .word("しく", "Shiku")
        .word("ひく", "Shiku")
        .char("Shiku")
            .ascent("Hya")
            .model("swl8")
            .glyph()
                .path("hya")
                .flick(2)

        # @head_swl4[0]: shii
        .word("しい", "Shii")
        .word("しー", "Shii")
        .word("ひい", "Shii")
        .word("ひー", "Shii")
        .path("shii", z[0]@{-160} >> 1.5 >> {-70}@z[4: -120])
        .char("Shii")
            .ascent(2)
            .model("swl4")
            .glyph()
                .path("shii")
                .flick(1)

        #  @head_uner16[0]: iwayuru
        .word("いわゆる", "Iwayuru")
        .word("よそ", "Iwayuru")
        .path("iwayuru~",
            path_horseshoe(
                len_=16,
                angle=-30,
                tension=1.6,
                rotation=-1,
                opening=4,
                head_angle=110
            )
        )
        .path("iwayuru", pref("iwayuru~")@{-110 - 30})
        .char("Iwayuru")
            .model("uner16")
            .ascent("Yo")
            .glyph()
                .path("iwayuru")

        # @head_uner8[0]: shima
        .word("しま", "Shima")
        .word("しむ", "Shima")
        .path("shima~",
            path_horseshoe(
                len_=8,
                angle=-30,
                tension=1.5,
                rotation=-1,
                opening=3,
                head_angle=110
            )
        )
        .path("shima", pref("shima~")@{-110 - 30})
        .char("Shima")
            .model("uner4")
            .ascent(-4)
            .glyph()
                .path("shima")

        # @head_uner4[0]: shimi
        .word("しみ", "Shimi")
        .word("しめ", "Shimi")
        .path("shimi~",
            path_horseshoe(
                len_=4,
                angle=-30,
                tension=1.5,
                rotation=-1,
                opening=2,
                head_angle=110
            )
        )
        .path("shimi", pref("shimi~")@{-110 - 30})
        .char("Shimi")
            .model("uner4")
            .ascent(-2)
            .glyph()
                .path("shimi")

        # @head_uer8[0]: saru
        .root()
        .path("saru~", pref("sai~") * 2)
        .path("saru", pref("saru~")@{180})

        # @head_uer4[0]: sai
        .word("さい", "Sai")
        .path("sai~", z[0]@{-10} >> z[2, -3] >> z[-4j])
        .path("sai", pref("sai~")@{180})
        .char("Sai")
            .ascent(2)
            .model("uer8")
            .glyph()
                .path("sai")

        # @head_uel8[0]: fa
        .word("ふぁ", "Fa")
        .path("fa", pref("wa") * 2)
        .char("Fa")
            .ascent(4)
            .model("uel8")
            .glyph()
                .path("fa")

        # @head_uel4[0]: wa
        # @head_sl4[0]: wa
        .word("わ", "Wa")
        .path("wa",
            z[0]@{-170} >> 1.4 >>
            z[-2.5, -2.5] >>
            {30}@z[0, -3.5]
        )
        .char("Wa")
            .tag("@head_uel4")
            .glyph()
                .path("wa")

        # @head_usl8[0]: kyar
        .word("きゃｒ", "Kyar")
        .path("kyar~",
            path_horseshoe(
                len_=8,
                angle=-10,
                tension=1.5,
                rotation=1,
                opening=3,
                head_angle=-110
            )
        )
        .path("kyar", pref("kyar~")@{110 - 10})
        .char("Kyar")
            .model("usl8")
            .ascent(4)
            .glyph()
                .path("kyar")

        # @head_uswl16[0]: pur
        .word("ぷｒ", "Pur")
        .word("あらゆる", "Pur")
        .path("pur~",
            path_horseshoe(
                len_=16,
                angle=-30,
                tension=1.6,
                rotation=1,
                opening=4,
                head_angle=-110
            )
        )
        .path("pur", pref("pur~")@{110 - 30})
        .char("Pur")
            .model("usw16")
            .ascent(8)
            .glyph()
                .path("pur")


        #: @head_uswl8[0]: par
        .word("ぱｒ", "Par")
        .path("par~",
            path_horseshoe(
                len_=8,
                angle=-30,
                tension=1.5,
                rotation=1,
                opening=3,
                head_angle=-110
            )
        )
        .path("par", pref("par~")@{110 - 30})
        .char("Par")
            .model("uswl8")
            .ascent(4)
            .glyph()
                .path("par")

        # @head_uswl4[0]: koso
        .word("こそ", "Koso")
        .path("koso~",
            path_horseshoe(
                len_=4,
                angle=-30,
                tension=1.5,
                rotation=1,
                opening=2,
                head_angle=-110
            )
        )
        .path("koso", pref("koso~")@{110 - 30})
        .char("Koso")
            .model("uswl4")
            .ascent(2)
            .glyph()
                .path("koso")

        # @head_oel4[0]: hodo
        .word("ほど", "Hodo")
        .path("hodo", 
            path_rice(
                len_=4,
                angle=0,
                head_angle=-20,
                tail_angle=20,
                width=1
            )
        )
        .char("Hodo")
            .ascent(0)
            .model("oel4")
            .glyph()
                .path("hodo")

        # @head_osel4[0]: eru
        .word("える", "Eru")
        .word("えｒ", "Eru")
        .word("えら", "Eru")
        .word("えり", "Eru")
        .word("えれ", "Eru")
        .word("えろ", "Eru")
        .path("eru", 
            path_rice(
                len_=4,
                angle=-60,
                head_angle=-20,
                tail_angle=20,
                width=1
            )
        )
        .char("Eru")
            .ascent(2)
            .model("osel4")
            .glyph()
                .path("eru")


        # @head_osl4[0]: kyuu
        .word("きゅう", "Kyuu")
        .path("kyuu", 
            path_rice(
                len_=4,
                angle=-90,
                head_angle=-20,
                tail_angle=20,
                width=1
            )
        )
        .char("Kyuu")
            .ascent(2)
            .model("osl4")
            .glyph()
                .path("kyuu")

        # @head_oswr4[0]: dogyo_o
        .word("お列変音", "DogyoO")
        .path("dogyo_o", 
            path_rice(
                len_=4,
                angle=-120,
                head_angle=20,
                tail_angle=-20,
                width=1
            )
        )
        .char("DogyoO")
            .ascent(2)
            .model("oswr4")
            .glyph()
                .path("dogyo_o")

        # @head_onwl4[0]: dogyo_e
        .word("え列変音", "DogyoE")
        .path("dogyo_e", 
            path_rice(
                len_=4,
                angle=120,
                head_angle=-20,
                tail_angle=20,
                width=1
            )
        )
        .char("DogyoE")
            .ascent(2)
            .model("onwl4")
            .glyph()
                .path("dogyo_e")

        # @head_oswl4[0]: kore
        .word("これ", "Kore")
        .word("この", "Kore")
        .path("kore", 
            path_rice(
                len_=4,
                angle=-120,
                head_angle=-20,
                tail_angle=20,
                width=1
            )
        )
        .char("Kore")
            .ascent(2)
            .model("oswl4")
            .glyph()
                .path("kore")

        # @head_cr4[0]: ai
        .word("あい", "Ai")
        .path("ai", z[0]@{180} >> {90}@z[-2, 2] >> {0}@z[0, 4] >> {-90}@z[2, 2] >> {180}@z[0])
        .char("Ai")
            .ascent(-2)
            .tag("cr4")
            .glyph()
                .path("ai")

        # @head_cr1[0]: koma
        .word("こま", "Koma")
        .path("koma", pref("ai") * 0.30)
        .char("Koma")
            .ascent(-2)
            .tag("cr2")
            .glyph()
                .path("koma")

#z[x, y, [-1.5, -2]]
    )

    builder = (
        builder.root()
        .char("PosTajuon")
            .glyph()
                .pos(0, 5)

        .mark("Dakuten")
            .glyph()
                .dot(4, -2)
            .glyph("e8[-1]")
                .dot(4, -2)
            .glyph("e16[-1]")
                .dot(8, -2)

    )
    builder = waseda_lc(builder)

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


