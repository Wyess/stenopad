#!/usr/bin/env python3

from __future__ import annotations
from math import radians as rad
from cmath import rect
from numbers import Integral, Real, Complex
import copy
from enum import Enum
from dataclasses import dataclass, replace
from reference import Reference

import pyx
from pyx.metapost.path import (
    beginknot,
    endknot,
    smoothknot,
    roughknot,
    tensioncurve,
    controlcurve,
    line,
)
pyx.unit.set(defaultunit="pt")


class Op(Enum):
    LINE2 = 0
    LINE3 = 1
    CURVE = 2

class CoordMode(Enum):
    ABS = 0
    REL = 1

@dataclass(frozen=True, slots=True)
class Path:
    elem: Point
    prev: Path | None = None

    def resolve_references(self, pool):
        def _v(val):
            if type(val).__name__ == "Reference":
                return val.resolve(pool)
            return val

        resolved_elem = replace(
            self.elem,
            x=_v(self.elem.x), y=_v(self.elem.y),
            right_angle=_v(self.elem.right_angle), right_tension=_v(self.elem.right_tension),
            left_angle=_v(self.elem.left_angle), left_tension=_v(self.elem.left_tension),
            next_left_angle=_v(self.elem.next_left_angle), next_left_tension=_v(self.elem.next_left_tension)
        )

        resolved_prev = self.prev.resolve_references(pool) if self.prev is not None else None

        return replace(self, elem=resolved_elem, prev=resolved_prev)

    def __matmul__(self, other):
        match other:
            case set() as s:
                return replace(self, elem=replace(self.elem, right_angle=s.pop()))

            case _:
                raise SyntaxError(other)

    def __rshift__(self, other):
        match other:
            case Point() as p:
                if p.left_angle is None:
                    left_angle = self.elem.next_left_angle
                else:
                    left_angle = p.left_angle
                left_tension = self.elem.next_left_tension
                return Path(elem=replace(p, left_angle=left_angle, left_tension=left_tension, connected_from=Op.CURVE), prev=self)

            case set() as s if len(s) == 1:
                elem = replace(self.elem, next_left_angle=s.pop())
                return replace(self, elem=elem)

            case Complex() as t:
                t1 = t.real
                t2 = None if t.imag == 0 else t.imag
                elem = replace(self.elem, right_tension=t1, next_left_tension=t2)
                return replace(self, elem=elem)

            case (Real(), Real()) as t:
                elem = replace(self.elem, right_tension= t[0], next_left_tension=t[1])
                return replace(self, elem=elem)

            case Path() as p:
                others = p.to_list()
                cur = p
                while cur.prev is not None:
                    cur = cur.prev
                cur = Path(elem=replace(others[0], connected_from=Op.CURVE), prev=self)
                for elem in others[1:]:
                    cur = Path(elem=elem, prev=cur)
                return cur

            case _:
                raise SyntaxError(other)

    def __neg__(self):
        others = self.to_list()
        cur = Path(elem=replace(others[0], neg_count=others[0].neg_count+1))
        for elem in others[1:]:
            cur = Path(elem=elem, prev=cur)
        return cur

    def __sub__(self, other):
        others = other.to_list()
        match other:
            case Path() as p if 1 <= p.top().elem.neg_count <= 2:
                if p.top().elem.neg_count == 1:
                    cur = Path(elem=replace(others[0], connected_from=Op.LINE2), prev=self)
                elif p.top().elem.neg_count == 2:
                    cur = Path(elem=replace(others[0], connected_from=Op.LINE3), prev=self)
                else:
                    raise SyntaxError(other)
            case _:
                raise SyntaxError(other)
        for elem in others[1:]:
            cur = Path(elem=elem, prev=cur)
        return cur

    def top(self):
        cur = self
        while cur.prev is not None:
            cur = cur.prev
        return cur

    def to_list(self):
        nodes = []
        current = self

        while current is not None:
            nodes.append(current.elem)
            current = current.prev

        return list(reversed(nodes))

    def __reversed__(self):
        current = self

        while current is not None:
            yield current
            current = current.prev

    def make_linear_segment(self, x1, y1, x2, y2):
        cp1_x = x1 + (x2 - x1) / 3.0
        cp1_y = y1 + (y2 - y1) / 3.0

        cp2_x = x1 + 2.0 * (x2 - x1) / 3.0
        cp2_y = y1 + 2.0 * (y2 - y1) / 3.0

        return pyx.metapost.path.controlcurve((cp1_x, cp1_y), (cp2_x, cp2_y))

    def _create_segment(self, pt1, pt2, pt3, is_end=False):
        match pt2.connected_from:
            case Op.LINE2:
                knot = (roughknot, endknot)[is_end](pt2.x, pt2.y)
                return line(), knot

            case Op.LINE3:
                knot = (roughknot, endknot)[is_end](pt2.x, pt2.y)
                return self.make_linear_segment(pt1.x, pt1.y, pt2.x, pt2.y), knot
                #return line(keepangles=True), knot

            case Op.CURVE:
                if is_end:
                    if pt2.left_angle is None:
                        if pt2.right_angle is None:
                            angle = None
                            curl = 1
                        elif pt2.right_angle.imag != 0:
                            angle = None
                            curl = pt2.right_angle.imag
                        else:
                            angle = pt2.right_angle
                            curl = 1
                    elif pt2.left_angle.imag != 0:
                        angle = None
                        curl = pt2.left_angle.imag
                    else:
                        angle = pt2.left_angle
                        curl = 1
                    knot = endknot(pt2.x, pt2.y,
                            angle=angle, curl=curl)
                elif pt3.connected_from != Op.CURVE:
                    knot = roughknot(pt2.x, pt2.y)
                elif (pt2.left_angle is None 
                      and pt2.right_angle is None):
                    knot = smoothknot(pt2.x, pt2.y)
                else:
                    if pt2.left_angle is None:
                        lcurl = 1
                        langle = None
                    elif pt2.left_angle.imag != 0:
                        lcurl = pt2.left_angle.imag
                        langle = None
                    else:
                        lcurl = 1
                        langle = pt2.left_angle

                    if pt2.right_angle is None:
                        rcurl = None
                        rangle = None
                    elif pt2.right_angle.imag != 0:
                        rcurl = pt2.right_angle.imag
                        rangle = None
                    else:
                        rcurl = None
                        rangle = pt2.right_angle

                    knot = roughknot(pt2.x, pt2.y, 
                            langle=langle, lcurl=lcurl,
                            rangle=rangle, rcurl=rcurl)
                tn1 = 1.0 if pt1.right_tension is None else pt1.right_tension
                tn2 = pt2.left_tension
                return tensioncurve(ltension=tn1, rtension=tn2), knot

            case _:
                raise ValueError(pt2.connected_from)

    def create_metapost_path(self, elems):
        x, y = elems[0].x, elems[0].y
        if elems[0].right_angle is None:
            angle = None
            curl = 1
        elif elems[0].right_angle.imag != 0:
            angle = None
            curl = elems[0].right_angle.imag
        else:
            angle = elems[0].right_angle
            curl = 1
        segs = [
            beginknot(
                elems[0].x, elems[0].y,
                angle=angle, curl=curl
            )
        ]
        for i, elem in enumerate(elems[1:], start=1):
            is_end = (i == len(elems) - 1)
            if elems[i].arc_pos is not None:
                arc_pos = elems[i].arc_pos
                # TODO: Use the index also
                subpath = self.create_metapost_path(elems[:i])
                p = subpath.at(subpath.end() + arc_pos)
                new_elem = replace(elem, x=elems[i].x +p[0] / pyx.unit.length(1), y=elems[i].y + p[1] / pyx.unit.length(1))
            elif elems[i].is_relative:
                new_elem = replace(elem, x=elem.x + x, y=elem.y + y)
            else:
                new_elem = elem

            x = new_elem.x 
            y = new_elem.y
            elems[i] = new_elem
            if is_end:
                new_segs = self._create_segment(
                    elems[i-1], elems[i], None, is_end
                )
            else:
                new_segs = self._create_segment(
                    elems[i-1], elems[i], elems[i+1], is_end
                )
            segs.extend(new_segs)
        return pyx.metapost.path.path(segs)

    def resolve(self):
        elems = self.to_list()
        return self.create_metapost_path(elems).returnSVGdata()
        #return self

# float だけでなく、遅延評価オブジェクト（Expr / Reference）も受け取れるようにする
ValueType = float | complex | Reference | None

@dataclass(frozen=True, slots=True)
class Point:
    x: ValueType
    y: ValueType = None

    right_angle: ValueType = None
    right_tension: ValueType = None

    left_angle: ValueType = None
    left_tension: ValueType = None

    next_left_angle: ValueType = None
    next_left_tension: ValueType = None

    neg_count: int = 0
    connected_from: Op | None = None
    arc_pos: float | None = None
    is_relative: bool = False

    def __post_init__(self):
        #return
        if self.y is None:
            x = self.x.real
            y = self.x.imag
            object.__setattr__(self, "x", x)
            object.__setattr__(self, "y", y)

    def __class_getitem__(self, key):
        match key:
            case Complex() as z:
                return Point(z)

            case (Real(), Real()) as z:
                return Point(*z)

            case slice(start=Real(), stop=Real(),
                       step=None) as s:
                r = s.start
                th = rad(s.stop)
                z = rect(r, th)
                return Point(z)

            case (Real() as x,
                  slice(start=Real(), stop=Real(),
                        step=None) as s):
                y = s.start
                th = rad(s.stop)
                z = complex(x, y) * rect(1, th)
                return Point(z)

            case _:
                raise TypeError(key)

    def __matmul__(self, other):
        match other:
            case (Real() as len_, int(index)):
                pass

            case Real() as len_:
                return replace(self, arc_pos=len_)

            case set() as s if len(s) == 1:
                return replace(self, right_angle=s.pop())

            case _:
                raise SyntaxError(other)

    def __rmatmul__(self, other):
        match other:
            case set() as s if len(s) == 1:
                return replace(self, left_angle=s.pop())

            case _:
                raise SyntaxError(other)

    def __rshift__(self, other):
        return Path(elem=self, prev=None) >> other

    def __pos__(self):
        return replace(self, is_relative=True)

    def __neg__(self):
        return replace(self, neg_count=self.neg_count + 1, x=-self.x, y=-self.y)

    def __sub__(self, other):
        match other:
            case Point() as p if p.neg_count == 0:
                return replace(self, x=x - p.x, y=y-p.y)

            case Point() as p if 1 <= p.neg_count <= 2:
                if p.neg_count == 1:
                    return Path(elem=replace(p, connected_from=Op.LINE2, x=-p.x, y=-p.y), prev=Path(elem=self, prev=None))
                elif p.neg_count == 2:
                    return Path(elem=replace(p, connected_from=Op.LINE3), prev=Path(elem=self, prev=None))

            case _:
                raise SyntaxError(other)

