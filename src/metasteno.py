#!/usr/bin/env python3

from math import radians as rad
from cmath import rect
from numbers import Integral, Real, Complex
import copy
from enum import Enum

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
            #setattr(clone, key, value)
            object.__setattr__(clone, key, value)
        return clone

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

            case _:
                raise SyntaxError(other)

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

    def _create_segment(self, pt1, pt2, is_end=False):
        match pt2.connected_from:
            case Op.LINE2:
                knot = (smoothknot, endknot)[is_end](pt2.x, pt2.y)
                return line(), knot
                
            case Op.LINE3:
                knot = (smoothknot, endknot)[is_end](pt2.x, pt2.y)
                return line(keepangles=True), knot

            case Op.CURVE:
                if is_end:
                    if pt2.left_angle is None:
                        angle = None
                        curl = 1
                    elif pt2.left_angle.imag != 0:
                        angle = None
                        curl = pt2.left_angle.imag
                    else:
                        angle = pt2.left_angle
                        curl = 1
                    knot = endknot(pt2.x, pt2.y,
                            angle=angle, curl=curl)
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

            segs.extend(
                self._create_segment(
                    elems[i-1], elems[i], is_end
                )
            )
        return pyx.metapost.path.path(segs)

    def resolve(self):
        elems = list(self)
        return self.create_metapost_path(elems).returnSVGdata()
    """
    beginknot,
    endknot,
    smoothknot,
    roughknot,
    tensioncurve,
    controlcurve,
    line,
    """

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

def save_debug_html(metasteno_expr, points_list, svg_path_d, filename="debug.html"):
    # 💡 スマホの画面幅でも見やすいようにCSSを調整したHTMLテンプレート
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MetaSteno Debugger</title>
    <style>
        body {{ font-family: sans-serif; background: #121212; color: #e0e0e0; padding: 10px; margin: 0; }}
        h3 {{ color: #00ffcc; margin-bottom: 5px; font-size: 14px; }}
        pre {{ background: #1e1e1e; padding: 8px; border-radius: 4px; overflow-x: auto; font-size: 12px; border: 1px solid #333; }}
        .canvas-container {{ background: #fff; border-radius: 8px; padding: 10px; text-align: center; margin-top: 15px; }}
        svg {{ max-width: 100%; height: auto; background: #fafafa; }}
    </style>
</head>
<body>

    <h3>1. Input Expression</h3>
    <pre>{metasteno_expr}</pre>

    <h3>2. Processed Points</h3>
    <pre>""" + "\n".join([str(p) for p in points_list]) + f"""</pre>

    <h3>3. Generated SVG Path</h3>
    <pre>{svg_path_d}</pre>

    <h3>4. Visualized Output</h3>
    <div class="canvas-container">
        <svg width="300" height="200" viewBox="-50 -50 200 200" xmlns="http://www.w3.org/2000/svg">
            <path d="{svg_path_d}" fill="none" stroke="#4a90e2" stroke-width="2" stroke-linecap="round"/>
            </svg>
    </div>

</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

z = Point

pyx.unit.set(defaultunit="pt")

path = "z[0]@{2j}>> {4j}@z[1, 1]@{5j} >> {3j}@z[2, 0]"
print(path)
print(eval(path).resolve())
print(pyx.metapost.path.path(
    [
        beginknot(0, 0, curl=2),
        tensioncurve(),
        roughknot(1, 1, lcurl=4, rcurl=5),
        tensioncurve(),
        endknot(2, 0, curl=3)
    ]
).returnSVGdata())
