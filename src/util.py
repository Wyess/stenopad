import pyx
from operator import itemgetter
from path_expression_parser import parse_path_expression
import math

def cat(names, pdict):
    return "&".join(itemgetter(*names)(pdict))

path_expression_parser = None
def set_path_expression_parser(parser):
    global path_expression_parser
    path_expression_parser = parser

def create_bbox(paths):
    bbox = sum([path.bbox() for path in paths], start=pyx.bbox.empty())
    u = pyx.unit.length(1)
    return {
        "top": -bbox.top() / u,
        "bottom": -bbox.bottom() / u,
        "left": bbox.left() / u,
        "right": bbox.right() / u,
    }

def create_paths(paths):
    u = pyx.unit.length(1)
    return [{"d": path.returnSVGdata(), "length": path.arclen() / u} for path in paths]

def get_dp(paths, post_offset):
    u = pyx.unit.length(1)
    dp = paths[-1].atend()
    return {
        'dx': dp[0] / u + post_offset[0],
        'dy': -dp[1] / u - post_offset[1]
    }

def create_glyphs(code, keys, ascents, post_offsets, tags=None):
    path_groups = path_expression_parser.parse(code)
    glyphs = []
    for i, path_group in enumerate(path_groups):
        if i == len(keys):
            break
        glyph = {
            'key': keys[i],
            'ascent': ascents[i],
            'path': create_paths(path_group),
            **get_dp(path_group, post_offsets[i]),
            **create_bbox(path_group),
        }
        if tags and tags[i] is not None:
            glyph['tag'] = tags[i]
        glyphs.append(glyph)

    return glyphs

def create_glyph(code, key='default', ascent=0, post_offset=(0, 0), tag=None):
    return create_glyphs(code, [key], [ascent], [post_offset], [tag])[0]

def create_ligature(code, keys, ascents):
    path_groups = path_expression_parser.parse(code)
    glyphs = []
    for i, path_group in enumerate(path_groups):
        if i == len(keys):
            break
        glyph = {
            'key': keys[i],
            'ascent': ascents[i],
            'path': create_paths(path_group),
            **get_dp(path_group),
            **create_bbox(path_group),
        }
        glyphs.append(glyph)

    return glyphs

def polar(r, th):
    rad = math.radians(th)
    return r * math.cos(rad), r * math.sin(rad)
