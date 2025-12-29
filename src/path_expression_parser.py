import pyx
import math
#from lark import Lark, Transformer
from path_expression_lark import Lark_StandAlone, Transformer
from point import Point
from path_elements import (
    PathKnot,
    PathJoinLine,
    PathJoinCurve,
    ArcPoint,
    DirectionSpecifierPair,
    DirectionSpecifierCurl,
    BasicPathJoin,
    create_pathitems,
)

pyx.unit.set(defaultunit="pt")

def polar(r, th):
    rad = math.radians(th)
    return r * math.cos(rad), r * math.sin(rad)

def moveto(normpath, pos=(0, 0)):
    x0, y0 = normpath.atbegin()
    dx, dy = -x0 + pos[0], -y0 + pos[1]
    return normpath.transformed(pyx.trafo.translate(dx, dy))


def move(normpath, dx, dy):
    return normpath.transformed(pyx.trafo.translate(dx, dy))


class PathExpressionTransformer(Transformer):
    _unary_op = {
        '+': lambda value: Point(*value, is_relative=True, to_update_pos=False) if isinstance(value, Point) else value,
        '-': lambda x: -x,
        '++': lambda x: x,
        '@': lambda x: x,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pen = Point(0, 0)
        self.vars = {
            "O": Point(0, 0),
            "I": Point(0, 1),
            "UP": Point(0, 1),
            "DOWN": Point(0, -1),
            "LEFT": Point(-1, 0),
            "RIGHT": Point(1, 0),
            "N": Point(0, 1),
            "E": Point(1, 0),
            "W": Point(-1, 0),
            "S": Point(0, -1),
            "NE": Point(*polar(1, 45)),
            "NW": Point(*polar(1, 135)),
            "SE": Point(*polar(1, -45)),
            "SW": Point(*polar(1, -135)),
            "NNE": Point(*polar(1, 60)),
            "NNW": Point(*polar(1, 120)),
            "ENE": Point(*polar(1, 30)),
            "WNW": Point(*polar(1, 150)),
            "SSE": Point(*polar(1, -60)),
            "SSW": Point(*polar(1, -120)),
            "ESE": Point(*polar(1, -30)),
            "WSW": Point(*polar(1, -150)),
        }

    def export_paths(self, paths_list):
        path_groups = []
        buf = []
        for paths in paths_list:
            buf.append(paths[0])
            if len(paths) > 1:
                path_groups.append(buf)
                path_groups.extend([[p] for p in paths[1:-1]])
                buf = [paths[-1]]
        if buf:
            path_groups.append(buf)

        for i, paths in enumerate(path_groups):
            if i == 0:
                continue
            x, y = paths[0].atbegin()
            path_groups[i] = [move(path, -x, -y) for path in paths]

        return path_groups

    def start(self, args):
        return self.export_paths(args)

    def path_expression(self, args):
        resolved_items = []
        split_times = []
        skip_next = False
        origin = Point(0, 0)

        for i, item in enumerate(args[2:-1], start=2):
            if not isinstance(item, PathKnot):
                continue
            ljoin, rjoin = args[i - 1], args[i + 1]
            if not isinstance(ljoin, PathJoinCurve):
                continue
            if not isinstance(rjoin, PathJoinCurve):
                continue
            if ljoin.rdir is None and isinstance(rjoin.ldir, DirectionSpecifierPair):
                ljoin.rdir = rjoin.ldir

        for i, item in enumerate(args):
            if skip_next:
                skip_next = False
                continue

            if isinstance(item, PathJoinCurve):
                if item.concatenate:
                    skip_next = True
                    origin = args[i - 1].point
                    if item.to_split:
                        split_times.append(i // 2 - len(split_times))
                    continue
            elif isinstance(item, PathKnot):
                if isinstance(item.point, ArcPoint):
                    item.resolve(resolved_items)
                    self.pen = item.point
                else:
                    if item.point.is_relative:
                        item.point = self.pen + item.point
                        if item.point.to_update_pos:
                            self.pen = item.point
                    else:
                        item.point = origin + item.point
                        self.pen = item.point
            resolved_items.append(item)

        pathitems = create_pathitems(resolved_items)
        path = pyx.metapost.path.path(pathitems)
        normpathparams = [pyx.normpath.normpathparam(path, 0, t) for t in split_times]
        return path.split(normpathparams)

    def path_knot(self, args):
        if isinstance(args[0], (Point, ArcPoint)):
            return PathKnot(args[0])
        elif isinstance(args[0], float):
            return PathKnot(Point(args[0], 0))
        raise NotImplementedError(f"{args=}")

    def path_join_line(self, args):
        return PathJoinLine()

    def path_join_line_tension_infinity(self, args):
        return PathJoinLine(keep_angle=True)

    def path_join_curve(self, args):
        ldir, basic_path_join, rdir = args
        return PathJoinCurve(ldir, basic_path_join, rdir)

    def direction_specifier_curl(self, args):
        raise NotImplementedError(f"{args=}")

    def direction_specifier_pair(self, args):
        lparen, direction, rparen = args

        if isinstance(direction, (float, int)):
            rad = math.radians(direction)
            return DirectionSpecifierPair(Point(math.cos(rad), math.sin(rad)))
        return DirectionSpecifierPair(direction)

    def basic_path_join_concatenate(self, args):
        to_split = args[0] == "&"
        return BasicPathJoin(concatenate=True, to_split=to_split)

    def basic_path_join_curve(self, args):
        return BasicPathJoin()

    def basic_path_join_curve_inflection_free(self, args):
        return BasicPathJoin(atleast=True)

    def basic_path_join_tension(self, args):
        ldots, tension, rdots = args
        return BasicPathJoin(tension=tension)

    def basic_path_join_controls(self, args):
        raise NotImplementedError(f"{args=}")

    def tension(self, args):
        ltension, rtension = args
        rtension = ltension if (rtension is None) else rtension
        return rtension, ltension

    def controls(self, args):
        raise NotImplementedError(f"{args=}")

    def atom(self, args):
        return args[0]

    def numeric_primary(self, args):
        if len(args) == 2:
            if args[0] == '+':
                return args[1]
            elif args[0] == '-':
                return -args[1]
        else:
            return args[0]

    def numeric_atom(self, args):
        return args[0]

    def scalar_multiplication_op(self, args):
        return args[0]

    def unary_op(self, args):
        return args[0]

    def primary_binop(self, args):
        return args[0]

    def secondary_binop(self, args):
        return args[0]

    def tertiary_binop(self, args):
        return args[0]

    def of_operator(self, args):
        return args[0]

    def unaryop_primary(self, args):
        op, value = args
        if op == "dir":
            if isinstance(value, float):
                rad = math.radians(value)
                return Point(math.cos(rad), math.sin(rad))
            elif isinstance(value, Point):
                r, deg = value
                rad = math.radians(deg)
                return Point(r * math.cos(rad), r * math.sin(rad))
        elif op == "@":
            arclength, subpath_index = value
            return ArcPoint(arclength, subpath_index)
        elif op == "++":
            x, y = value
            return Point(x, y, is_relative=True, to_update_pos=True)
        elif op == "+":
            if isinstance(value, Point):
                x, y = value
                return Point(x, y, is_relative=True, to_update_pos=False)
            else:
                return value
        elif op == "-":
            if value == 0:
                return -0.0
            else:
                return -value
        raise NotImplementedError(f"{args=}")

    def scalar_multiplied_primary(self, args):
        op, value = args
        if isinstance(value, (int, float)):
            return value + op
        return value * op

    def of_primary(self, args):
        op, param, of, target = args
        raise NotImplementedError(f"{args=}")

    def atom_primary(self, args):
        return args[0]

    def pair_primary(self, args):
        lparen, x, comma, y, rparen = args
        return Point(x, y)

    def atpair_primary(self, args):
        lparen, arclength, comma, path_index, rparen = args
        return ArcPoint(arclength, path_index)

    def polar_pair_primary(self, args):
        lparen, angle, colon, length, rparen = args
        rad = math.radians(angle)
        return Point(length * math.cos(rad), length * math.sin(rad))

    def secondary(self, args):
        if len(args) == 1:
            if isinstance(args[0], (Point, float, int, ArcPoint)):
                return args[0]
        raise NotImplementedError(f"{args=}")

    def tertiary(self, args):
        if len(args) == 1 and isinstance(args[0], (Point, float, int, ArcPoint)):
            return args[0]
        elif len(args) == 3:
            left, op, right = args
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
        raise NotImplementedError(f"{args=}")

    def expression(self, args):
        if len(args) == 1:
            if isinstance(args[0], (Point, float, int)):
                return args[0]
        raise NotImplementedError(f"{args=}")

    def number_or_fraction(self, args):
        numerator, denominator = args
        if denominator is None:
            return numerator
        elif denominator != 0.0:
            return numerator / denominator
        else:
            raise SyntaxError("Cannot divide by zero")

    def number(self, args):
        return float(args[0])

    def variable(self, args):
        varname = args[0]
        if varname in self.vars:
            return self.vars[varname]
        raise SyntaxError(f"Unknown variable {args[0]}")

def create_path_expression_parser(var_dict=None):
    tr = PathExpressionTransformer()
    if var_dict is not None:
        tr.vars |= var_dict
    #parser = Lark.open(
    #    "path_expression.lark",
    #    transformer=tr,
    #    parser="lalr",
    #)

    parser= Lark_StandAlone(transformer=tr)
    return parser

parser = create_path_expression_parser()

def parse_path_expression(code):
    return parser.parse(code)
        
