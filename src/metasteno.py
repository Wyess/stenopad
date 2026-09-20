#!/usr/bin/env python3

from __future__ import annotations
from math import (
    radians as rad,
    copysign,
    atan2,
    degrees,
)
from cmath import (
    rect,
    phase,
)
from numbers import Integral, Real, Complex
import copy
from enum import Enum
from dataclasses import dataclass, replace
from reference import Reference
import operator

from scale_angle import scale_angle

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

    def resolve(self, pool=None):
        if pool is None:
            pool = {}

        def _v(val):
            if isinstance(val, Reference):
                return val.resolve(pool)
            return val

        resolved_elem = replace(
            self.elem,
            x=_v(self.elem.x),
            y=_v(self.elem.y),
            right_angle=_v(self.elem.right_angle),
            right_tension=_v(self.elem.right_tension),
            left_angle=_v(self.elem.left_angle),
            left_tension=_v(self.elem.left_tension),
            next_left_angle=_v(self.elem.next_left_angle),
            next_left_tension=_v(self.elem.next_left_tension)
        )
        if self.prev is None:
            resolved_prev = None
        else:
            resolved_prev = self.prev.resolve(pool)

        return replace(
            self,
            elem=resolved_elem,
            prev=resolved_prev
        )

    def get_head_angle(self):
        # TODO: straight lines and implicit angles
        top = self.top()
        if top.elem.right_angle is not None:
            return top.elem.right_angle

    def get_tail_angle(self):
        # TODO: straight lines and implicit angles
        return self.elem.left_angle

    def __matmul__(self, other):
        match other:
            case set() as s:
                angle = s.pop()
                if self.elem.connected_from != Op.CURVE:
                    left_angle = None
                    right_angle = angle
                elif self.elem.left_angle is None:
                    left_angle = angle
                    right_angle = None
                else:
                    left_angle = self.elem.left_angle
                    right_angle = angle

                return replace(
                    self,
                    elem=replace(
                        self.elem,
                        right_angle=right_angle,
                        left_angle=left_angle
                    )
                )

            case Point() as p:
                x, y = p.x, p.y
                top = self.top()
                dx, dy = x - top.elem.x, y - top.elem.y
                return self + Point(dx, dy)

            case _:
                return NotImplemented

    def __rshift__(self, other):
        match other:
            case Point() as p:
                if p.left_angle is None:
                    left_angle = self.elem.next_left_angle
                else:
                    left_angle = p.left_angle
                left_tension = self.elem.next_left_tension
                return Path(
                    elem=replace(p,
                        left_angle=left_angle,
                        left_tension=left_tension,
                        connected_from=Op.CURVE
                    ),
                    prev=self
                )

            case set() as s if len(s) == 1:
                elem = replace(
                    self.elem,
                    next_left_angle=s.pop()
                )
                return replace(self, elem=elem)

            case Complex() as t:
                t1 = t.real
                t2 = t.imag or None
                elem = replace(
                    self.elem,
                    right_tension=t1,
                    next_left_tension=t2
                )
                return replace(self, elem=elem)

            case (Real(), Real()) as t:
                elem = replace(
                    self.elem,
                    right_tension=t[0],
                    next_left_tension=t[1]
                )
                return replace(self, elem=elem)

            case Path() as p:
                others = list(p)
                cur = p
                while cur.prev is not None:
                    cur = cur.prev
                cur = Path(
                    elem=replace(
                        others[0],
                        connected_from=Op.CURVE
                    ),
                    prev=self)
                for elem in others[1:]:
                    cur = Path(elem=elem, prev=cur)
                return cur

            case _:
                return NotImplemented

    def __neg__(self):
        others = list(self)
        cur = Path(
            elem=replace(
                others[0],
                neg_count=others[0].neg_count + 1
            )
        )
        for elem in others[1:]:
            cur = Path(elem=elem, prev=cur)
        return cur

    def __sub__(self, other):
        match other:
            case Path() as p if p.top().elem.neg_count in (1, 2):
                others = list(other)
                idx = p.top().elem.neg_count - 1
                op = (Op.LINE2, Op.LINE3)[idx]
                cur = Path(
                    elem=replace(
                        others[0],
                        connected_from=op
                    ),
                    prev=self
                )
                for elem in others[1:]:
                    cur = Path(
                        elem=elem,
                        prev=cur
                    )
                return cur

            case Point() as p if p.neg_count in (1, 2):
                idx = p.neg_count - 1
                op = (Op.LINE2, Op.LINE3)[idx]
                sign = 1 - (p.neg_count % 2) * 2
                cur = Path(
                    elem=replace(
                        p,
                        connected_from=op,
                        x=sign * p.x,
                        y=sign * p.y,
                    ),
                    prev=self
                )
                return cur

            case _:
                print(p)
                return NotImplemented

    def __and__(self, other):
        match other:
            case Path() as p:
                others = list(p)
                cur = replace(
                    self,
                    elem=replace(
                        self.elem,
                        right_angle=others[0].right_angle
                    )
                )
                dx, dy = self.elem.x, self.elem.y
                for node in others[1:]:
                    if node.is_relative or node.arc_pos is not None:
                        cur = Path(
                            elem=node,
                            prev=cur,
                        )
                    else:
                        cur = Path(
                            elem=replace(
                                node,
                                x=node.x + dx,
                                y=node.y + dy,
                            ),
                            prev=cur,
                        )

                return cur

            case _:
                return NotImplemented

    def __add__(self, other):
        match other:
            case Point() as p:
                dx, dy = p.x, p.y
                cur = None
                for node in self:
                    if (
                        node.is_relative or
                        node.arc_pos is not None
                    ):
                        cur = Path(
                            elem=node,
                            prev=cur,
                        )
                    else:
                        cur = Path(
                            elem=replace(
                                node,
                                x=node.x + dx,
                                y=node.y + dy,
                            ),
                            prev=cur,
                        )
                return cur

            case _:
                return NotImplemented

    def __mul__(self, other):
        match other:
            case Real() as r:
                cur = None
                for node in self:
                    cur = Path(
                        elem=replace(
                            node,
                            x=node.x * r,
                            y=node.y * r,
                        ),
                        prev=cur,
                    )
                return cur

            case (Real(), Real(), Real()) as t:
                sx, sy, angle = t
                th = rad(angle)

                cur = None
                for node in self:
                    x=node.x * sx
                    y=node.y * sy
                    z = complex(x, y) * rect(1, th)
                    if node.left_angle is None:
                        langle = None
                    else:
                        langle = scale_angle(
                            sx,
                            sy,
                            node.left_angle
                        ) + angle
                    if node.right_angle is None:
                        rangle = None
                    else:
                        rangle = scale_angle(
                            sx,
                            sy,
                            node.right_angle
                        ) + angle
                    cur = Path(
                        elem=replace(
                            node,
                            x=z.real,
                            y=z.imag,
                            left_angle=langle,
                            right_angle=rangle,
                        ),
                        prev=cur,
                    )
                return cur

            case _:
                return NotImplemented

    def top(self):
        cur = self
        while cur.prev is not None:
            cur = cur.prev
        return cur

    def __iter__(self):
        nodes = []
        current = self

        while current is not None:
            nodes.append(current.elem)
            current = current.prev

        for node in reversed(nodes):
            yield node

    def __reversed__(self):
        current = self

        while current is not None:
            yield current
            current = current.prev

    def line(self, x1, y1, x2, y2):
        cp1_x = x1 + (x2 - x1) / 3.0
        cp1_y = y1 + (y2 - y1) / 3.0

        cp2_x = x1 + 2.0 * (x2 - x1) / 3.0
        cp2_y = y1 + 2.0 * (y2 - y1) / 3.0

        return pyx.metapost.path.controlcurve(
            (cp1_x, cp1_y),
            (cp2_x, cp2_y)
        )

    def _create_segment(self, pt1, pt2, pt3):
        is_end = pt3 is None
        match pt2.connected_from:
            case Op.LINE2:
                line_seg = line()
                if is_end:
                    return line_seg, endknot(pt2.x, pt2.y)
                else:
                    return line_seg, roughknot(pt2.x, pt2.y, rangle=pt2.right_angle)

            case Op.LINE3:
                line_seg = self.line(
                    pt1.x, pt1.y,
                    pt2.x, pt2.y
                )
                if is_end:
                    return line_seg, endknot(pt2.x, pt2.y)
                else:
                    return line_seg, roughknot(pt2.x, pt2.y)
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
                    knot = endknot(
                        pt2.x,
                        pt2.y,
                        angle=angle,
                        curl=curl
                    )
                elif pt3.connected_from != Op.CURVE:
                    if pt2.left_angle is None:
                        lcurl = 1
                        langle = None
                    elif pt2.left_angle.imag != 0:
                        lcurl = pt2.left_angle.imag
                        langle = None
                    else:
                        lcurl = 1
                        langle = pt2.left_angle
                    knot = roughknot(
                        pt2.x,
                        pt2.y,
                        langle=langle,
                        lcurl=lcurl
                    )
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

                    knot = roughknot(
                        pt2.x,
                        pt2.y, 
                        langle=langle,
                        lcurl=lcurl,
                        rangle=rangle,
                        rcurl=rcurl
                    )

                if pt1.right_tension is None:
                    tn1 = 1.0
                else:
                    tn1 = pt1.right_tension
                tn2 = pt2.left_tension
                return (
                    tensioncurve(
                        ltension=tn1,
                        rtension=tn2
                    ),
                    knot
                )

            case _:
                raise ValueError(pt2.connected_from)

    def create_metapost_path(self, elems=None):
        if elems is None:
            elems = list(self)
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
                idx = i + elems[i].arc_idx
                assert idx > 0, f"arc_idx is out of bounds {idx=}"
                subpath = self.create_metapost_path(elems[:idx + 1])
                arc_sign = copysign(1.0, arc_pos)
                if arc_sign < 0:
                    p = subpath.at(subpath.end() + arc_pos)
                else:
                    p = subpath.at(arc_pos)
                u = pyx.unit.length(1)
                new_elem = replace(
                    elem,
                    x=elems[i].x + p[0] / u,
                    y=elems[i].y + p[1] / u
                )
            elif elems[i].is_relative:
                new_elem = replace(
                    elem,
                    x=elem.x + x,
                    y=elem.y + y
                )
            else:
                new_elem = elem

            x = new_elem.x 
            y = new_elem.y
            elems[i] = new_elem
            if is_end:
                new_segs = self._create_segment(
                    elems[i - 1],
                    elems[i],
                    None
                )
            else:
                new_segs = self._create_segment(
                    elems[i - 1],
                    elems[i],
                    elems[i + 1]
                )
            segs.extend(new_segs)
        return pyx.metapost.path.path(segs)

    def returnSvgData(self):
        elems = list(self)
        mpath = self.create_metapost_path(elems)
        return mpath.returnSVGdata()

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
    arc_idx: int = -1
    is_relative: bool = False

    def __post_init__(self):
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

            case slice(
                start=Real() as r,
                stop=Real() as deg,
                step=None
            ) as s:
                th = rad(deg)
                z = rect(r, th)
                return Point(z)

            case slice(
                start=None,
                stop=Real() as deg,
                step=None
            ) as s:
                r = 1.0
                th = rad(deg)
                z = rect(r, th)
                return Point(z)

            case (
                Real() as x,
                slice(
                    start=Real() as y,
                    stop=Real() as deg,
                    step=None
                ) as s
            ):
                th = rad(deg)
                z = complex(x, y) * rect(1, th)
                return Point(z)

            case Reference() as r:
                return r.apply(Point)

            case _:
                raise TypeError(key)

    def resolve(self, pool):
        def _v(val):
            if isinstance(val, Reference):
                return val.resolve(pool)
            return val

        return replace(
            self,
            x=_v(self.x),
            y=_v(self.y),
            right_angle=_v(self.right_angle),
            right_tension=_v(self.right_tension),
            left_angle=_v(self.left_angle),
            left_tension=_v(self.left_tension),
            next_left_angle=_v(self.next_left_angle),
            next_left_tension=_v(self.next_left_tension)
        )

    def __matmul__(self, other):
        match other:
            case (Real() as len_, Integral() as idx):
                return replace(
                    self,
                    arc_pos=len_,
                    arc_idx=idx
                )

            case Real() as len_:
                return replace(self, arc_pos=len_)

            case set() as s if len(s) == 1:
                return replace(
                    self,
                    right_angle=s.pop()
                )

            case _:
                return NotImplemented

    def __rmatmul__(self, other):
        match other:
            case set() as s if len(s) == 1:
                return replace(
                    self,
                    left_angle=s.pop()
                )

            case _:
                return NotImplemented

    def __rshift__(self, other):
        return Path(elem=self, prev=None) >> other

    def __pos__(self):
        return replace(self, is_relative=True)

    def __neg__(self):
        return replace(
            self,
            neg_count=self.neg_count + 1,
            x=-self.x,
            y=-self.y
        )

    def __sub__(self, other):
        match other:
            case Point() as p if p.neg_count == 0:
                return replace(
                    self,
                    x=self.x - p.x,
                    y=self.y - p.y
                )

            case Point() as p if p.neg_count in (1, 2):
                idx = p.neg_count - 1
                op = (Op.LINE2, Op.LINE3)[idx]
                sign = 1 - (p.neg_count % 2) * 2
                return Path(
                    elem=replace(
                        p,
                        connected_from=op,
                        x=sign * p.x,
                        y=sign * p.y
                    ),
                    prev=Path(elem=self, prev=None)
                )

            case _:
                return NotImplemented

