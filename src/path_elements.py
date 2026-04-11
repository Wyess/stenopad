from point import Point
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

def _tou(length):
    return length / pyx.unit.length(1)

def create_pathitems(pathelems):
    pathitems = []
    for i, elem in enumerate(pathelems):
        if isinstance(elem, PathKnot):
            ljoin = pathelems[i - 1] if (i > 0) else None
            rjoin = pathelems[i + 1] if (i + 1 < len(pathelems)) else None
            pathitems.append(elem.create_pathitem(ljoin, rjoin))
        elif isinstance(elem, (DirectionSpecifierPair, DirectionSpecifierCurl)):
            pass
        elif elem:
            pathitems.append(elem.create_pathitem())
    return pathitems


class PathKnot:
    def __init__(self, point):
        self.point = point

    def resolve(self, pathelems):
        if isinstance(self.point, ArcPoint):
            subpath_idx = self.point.subpath_index
            if subpath_idx < 0:
                subpath_idx += len(pathelems) // 2 - 1

            subpath_slice = slice(0, 3 + 2 * subpath_idx)
            assert 0 < subpath_slice.stop < len(pathelems)
            subpathelems = pathelems[subpath_slice]

            subpathitems = create_pathitems(subpathelems)
            subpath = pyx.metapost.path.path(subpathitems)

            arclen = self.point.arclength
            # Use copysign to treat -0.0 separate from +0.0
            if math.copysign(1.0, arclen) > 0:
                p = subpath.at(arclen)
            else:
                p = subpath.at(subpath.end() + arclen)
            self.point = Point(_tou(p[0]), _tou(p[1])) + self.point.offset

    def create_pathitem(self, ljoin=None, rjoin=None):
        if ljoin is None:
            assert rjoin is not None
            curl, angle = rjoin.get_leftknot_curl_angle(is_start=True)
            return beginknot(*self.point, curl, angle)

        if rjoin is None:
            assert ljoin is not None
            curl, angle = ljoin.get_rightknot_curl_angle(is_end=True)
            return endknot(*self.point, curl, angle)

        if isinstance(rjoin, DirectionSpecifierPair):
            return endknot(*self.point, angle=rjoin.get_angle())

        if isinstance(rjoin, DirectionSpecifierCurl):
            return endknot(*self.point, curl=rjoin.curl)

        lcurl, langle = ljoin.get_rightknot_curl_angle()
        rcurl, rangle = rjoin.get_leftknot_curl_angle()

        if all(param is None for param in (lcurl, rcurl, langle, rangle)):
            return smoothknot(*self.point)

        langle = rangle if (langle is None and rangle is not None) else langle
        lcurl = 1 if (lcurl is None and langle is None) else lcurl

        return roughknot(*self.point, lcurl, rcurl, langle, rangle)

    def __repr__(self):
        return f"<PathKnot({self.point})>"


class PathJoinLine:
    def __init__(self, keep_angle=False):
        self.keep_angle = keep_angle
        self.concatenate = False
        self.to_split = False

    def get_leftknot_curl_angle(self, is_start=None):
        return 1, None

    def get_rightknot_curl_angle(self, is_end=None):
        return 1, None

    def create_pathitem(self):
        return line(self.keep_angle)

    def __str__(self):
        return f"<PathJoinLine(keep_angle={self.keep_angle})>"

    def __repr__(self):
        return f"<PathJoinLine(keep_angle={self.keep_angle})>"

class PathJoinCurve:
    def __init__(self, ldir, basic_path_join, rdir):
        self.ldir = ldir
        self.basic_path_join = basic_path_join
        self.concatenate = basic_path_join.concatenate
        self.to_split = basic_path_join.to_split
        self.rdir = rdir

    def get_leftknot_curl_angle(self, is_start=False):
        if isinstance(self.ldir, DirectionSpecifierPair):
            return None, self.ldir.get_angle()
        elif isinstance(self.ldir, DirectionSpecifierCurl):
            return self.ldir.curl, None
        elif is_start:
            return 1.0, None 
        else:
            return None, None

    def get_rightknot_curl_angle(self, is_end=False):
        if isinstance(self.rdir, DirectionSpecifierPair):
            return None, self.rdir.get_angle()
        elif isinstance(self.rdir, DirectionSpecifierCurl):
            return self.rdir.curl, None
        elif is_end:
            return 1.0, None
        else:
            return None, None

    def create_pathitem(self):
        if self.basic_path_join.atleast:
            return tensioncurve(latleast=True, ratleast=True)

        if self.basic_path_join.tension is not None:
            ltension, rtension = self.basic_path_join.tension
            return tensioncurve(ltension=ltension, rtension=rtension)

        if self.basic_path_join.controls is not None:
            raise NotImplementedError(f"{self.basic_path_join.control.scontrols=}")

        return tensioncurve()

    def __repr__(self):
        return f"<PathJoinCurve({self.ldir}, {self.basic_path_join}, {self.rdir})>"


class ArcPoint:
    def __init__(self, arclength, subpath_index):
        self.arclength = arclength
        self.subpath_index = int(subpath_index)
        self.offset = Point(0, 0)

    def create_pathitem(self, pathitems):
        return None

    def __repr__(self):
        return (
            f"<ArcPoint({self.arclength}, {self.subpath_index}, offset={self.offset}>"
        )

    def __add__(self, other):
        if isinstance(other, Point):
            apt = ArcPoint(self.arclength, self.subpath_index)
            apt.offset = self.offset + other
            return apt

    def __radd__(self, other):
        if isinstance(other, Point):
            apt = ArcPoint(self.arclength, self.subpath_index)
            apt.offset = self.offset + other
            return apt


class DirectionSpecifierPair:
    def __init__(self, pair):
        self.pair = pair

    def get_angle(self):
        rad = math.atan2(self.pair.y, self.pair.x)
        return math.degrees(rad)

    def get_leftknot_curl_angle(self):
        return None, self.get_angle()

    def __repr__(self):
        return f"<DirectionSpecifierPair{self.pair})"


class DirectionSpecifierCurl:
    def __init__(self, curl):
        self.curl = curl

    def get_curl(self):
        return self.curl

    def get_leftknot_curl_angle(self):
        return self.curl, None

    def __repr__(self):
        return f"<DirectionSpecifierPair{self.pair})"

class BasicPathJoin:
    def __init__(
        self,
        concatenate=False,
        to_split=True,
        atleast=False,
        tension=None,
        controls=None,
    ):
        self.concatenate = concatenate
        self.to_split = to_split and concatenate
        self.atleast = atleast
        self.tension = tension if tension is not None else (1.0, 1.0)
        self.controls = controls

    def __repr__(self):
        return f"<BasicPathJoin(concatenate={self.concatenate}, to_split={self.to_split}, atleast={self.atleast}, tension={self.tension}, controls={self.controls})>"
