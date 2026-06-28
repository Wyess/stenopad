#!/usr/bin/env python3

from math import radians as rad
from cmath import rect
from numbers import Integral, Real, Complex
import copy
from enum import Enum

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


class Path:
    def __init__(self, elem, prev=None):
        self.elem = elem
        self.prev = prev
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name, value):
        if getattr(self, "_initialized", False):
            raise AttributeError(f"{self.__class__.__name__}")
        super().__setattr__(name, value)

    def _replace(self, **changes):
        clone = copy.copy(self)
        for key, value in changes.items():
            object.__setattr__(clone, key, value)
        return clone

    def __matmul__(self, other):
        match other:
            case set() as s:
                return self._replace(elem=self.elem._replace(right_angle=s.pop()))

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
                return Path(elem=p._replace(left_angle=left_angle, left_tension=left_tension, connected_from=Op.CURVE), prev=self)

            case set() as s if len(s) == 1:
                elem = self.elem._replace(next_left_angle=s.pop())
                return self._replace(elem=elem)

            case Complex() as t:
                t1 = t.real
                t2 = None if t.imag == 0 else t.imag
                elem = self.elem._replace(right_tension=t1, next_left_tension=t2)
                return self._replace(elem=elem)

            case (Real(), Real()) as t:
                elem = self.elem._replace(right_tension= t[0], next_left_tension=t[1])
                return self._replace(elem=elem)

            case Path() as p:
                others = list(p)
                cur = p
                while cur.prev is not None:
                    cur = cur.prev
                cur = Path(elem=others[0]._replace(connected_from=Op.CURVE), prev=self)
                for elem in others[1:]:
                    cur = Path(elem=elem, prev=cur)
                return cur

            case _:
                raise SyntaxError(other)

    def __neg__(self):
        others = list(self)
        cur = Path(elem=others[0]._replace(neg_count=others[0].neg_count+1))
        for elem in others[1:]:
            cur = Path(elem=elem, prev=cur)
        return cur

    def __sub__(self, other):
        others = list(other)
        match other:
            case Path() as p if 1 <= p.top().elem.neg_count <= 2:
                if p.top().elem.neg_count == 1:
                    cur = Path(elem=others[0]._replace(connected_from=Op.LINE2), prev=self)
                elif p.top().elem.neg_count == 2:
                    cur = Path(elem=others[0]._replace(connected_from=Op.LINE3), prev=self)
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

    def __str__(self):
        return f"Path({self.elem},{self.prev})"

    def __iter__(self):
        nodes = []
        current = self

        while current is not None:
            nodes.append(current.elem)
            current = current.prev

        for el in reversed(nodes):
            yield el

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

        return pyx.metapost.path.controlcurve_pt((cp1_x, cp1_y), (cp2_x, cp2_y))

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
                new_elem = elem._replace(x=elems[i].x +p[0] / pyx.unit.length(1), y=elems[i].y + p[1] / pyx.unit.length(1))
            elif elems[i].is_relative:
                new_elem = elem._replace(x=elem.x + x, y=elem.y + y)
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
        elems = list(self)
        return self.create_metapost_path(elems).returnSVGdata()

class Point:
    def __init__(self, x=0, y=None):
        if y is None:
            self.x = x.real
            self.y = x.imag
        else:
            self.x = x
            self.y = y

        self.right_angle = None
        self.right_tension = None

        self.left_angle = None
        self.left_tension = None

        self.next_left_angle = None
        self.next_left_tension = None

        self.neg_count = 0
        self.connected_from = None
        self.ox = None
        self.oy = None
        self.arc_pos = None
        self.is_relative = False

        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name, value):
        if getattr(self, "_initialized", False):
            raise AttributeError(f"{self.__class__.__name__}")
        super().__setattr__(name, value)


    def _replace(self, **changes):
        clone = copy.copy(self)
        for key, value in changes.items():
            object.__setattr__(clone, key, value)
        return clone

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

    def __str__(self):
        items = [f"{k}={v}" for k, v in vars(self).items() if v is not None and not k.startswith("_")]
        return f"{self.__class__.__name__}({', '.join(items)})"

    __repr__ = __str__

    def __matmul__(self, other):
        match other:
            case (Real() as len_, int(index)):
                pass

            case Real() as len_:
                return self._replace(arc_pos=len_)

            case set() as s if len(s) == 1:
                return self._replace(right_angle=s.pop())

            case _:
                raise SyntaxError(other)

    def __rmatmul__(self, other):
        match other:
            case set() as s if len(s) == 1:
                return self._replace(left_angle=s.pop())

            case _:
                raise SyntaxError(other)

    def __rshift__(self, other):
        return Path(elem=self, prev=None) >> other

    def __pos__(self):
        return self._replace(is_relative=True)

    def __neg__(self):
        return self._replace(neg_count=self.neg_count + 1, x=-self.x, y=-self.y)

    def __sub__(self, other):
        match other:
            case Point() as p if p.neg_count == 0:
                return self._replace(x=x - p.x, y=y-p.y)

            case Point() as p if 1 <= p.neg_count <= 2:
                if p.neg_count == 1:
                    return Path(elem=p._replace(connected_from=Op.LINE2, x=-p.x, y=-p.y), prev=Path(elem=self, prev=None))
                elif p.neg_count == 2:
                    return Path(elem=p._replace(connected_from=Op.LINE3), prev=Path(elem=self, prev=None))

            case _:
                raise SyntaxError(other)
