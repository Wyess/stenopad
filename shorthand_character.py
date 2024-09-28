from key_parser import parse as parse_key
from text_parser import parse as parse_text
from more_itertools import pairwise, split_after, partitions
import math
import logging
import random

#from load_xml import Shorthand, BBox, Glyph, Character as CharacterBase, Path, load_dict_xml

logger = logging.getLogger(__name__)

class Context:
    def __init__(self, x=0, y=0, reference_line=0, right=0, margin=5):
        self.x = x
        self.y = y
        self.reference_line = reference_line
        self.right = right
        self.margin = margin

class Line:
    def __init__(self, chars=None):
        self.chars = chars if chars else []

    @property
    def clauses(self):
        return split_after(self.chars, lambda c: c.is_space)

class Bbox:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.width = right - left
        self.height = bottom - top

    def __str__(self):
        return f"{self.left} {self.top} {self.width} {self.height}"

class String:
    def __init__(self, text, sh=None, fixed_viewbox=True):
        self.text = text
        self.sh = sh
        self.chars = self.get_chars(text)
        self.connect()
        self.select_glyphs()
        bbox = self.layout()
        self.svg_template = f"""<svg
            id="svg_root"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            version="1.1"
            viewBox="{'0 0 200 100' if fixed_viewbox else bbox}"
            width="{200 if fixed_viewbox else bbox.width}mm"
            height="{100 if fixed_viewbox else bbox.height}mm"
            preserveAspectRatio="xMinYMin meet"
            data-text=""
            transform="scale(1, 1)"
            transform-origin="center"
            style="fill: none; stroke: rgb(0, 0, 0); stroke-width: 0.425197; stroke-linecap: round; stroke-linejoin: round; stroke-miterlimit: 4; stroke-opacity: 1; background-color: #f0e68c;"
        >{{}}</svg>"""

    def get_chars(self, text):
        chars = []
        for word in parse_text(text):
            for parts in partitions(word):
                subwords = ["".join(part) for part in parts]
                if all([subword in self.sh['dictionary'] for subword in subwords]):
                    for subword in subwords:
                        for char_name in self.sh['dictionary'][subword]['chars']:
                            chars.append(Character(char_name, self.sh))
                    break
            else:
                chars.append(Character('Null', self.sh))
        return chars

    def connect(self):
        base = None
        for char in self.chars:
            char.prev = base
            if char.is_marker:
                continue
            elif base:
                base.next = char
            base = char

    def __str__(self):
        return self.create_path_elements()[0]

    def __repr__(self):
        return f"String({'self.text'})"

    def __split(self):
        return [Line(char_list) for char_list in split_after(self.chars, lambda c: c.is_newline)]

    def set_position(self, cntx, char):
        if char.prev is None:
            cntx.x = max(cntx.right - char.left, 0)
            cntx.y = max(cntx.reference_line - char.ascent, 0)

        char.set_pos(cntx.x, cntx.y)
        if char.is_space:
            try:
                cntx.x = cntx.right + char.dx - char.next.left
            except (IndexError, AttributeError):
                cntx.x += char.dx
            try:
                cntx.y = cntx.reference_line + char.dy - char.next.ascent
            except (IndexError, AttributeError):
                cntx.y = cntx.reference_line + char.dy
            cntx.right = cntx.x
        elif char.is_newline:
            try:
                cntx.right = cntx.margin - char.next.left
            except (IndexError, AttributeError):
                pass
            cntx.reference_line += char.dy
            cntx.x = cntx.right
            try:
                cntx.y = cntx.reference_line - char.next.ascent
            except (IndexError, AttributeError):
                cntx.y = cntx.reference_line

        elif char.is_marker:
            try:
                char.set_pos(char.prev.x, char.prev.y)
            except AttributeError:
                pass
        else:
            cntx.x, cntx.y = char.exit
            cntx.right = max(cntx.right, char.x + char.right)

    def correct_left_and_top(self, lines, margin=5):
        for line in lines:
            left_min = min([char.x + char.left for char in line.chars])
            xoffset = margin - left_min if left_min < 0 else 0
            for char in line.chars:
                char.set_pos(char.x + xoffset, char.y)

        top_min = min([char.y + char.top for char in self.chars])
        yoffset = margin - top_min if top_min < 0 else 0
        for char in self.chars:
            char.set_pos(char.x, char.y + yoffset)

    def correct_inter_line(self, lines, margin=5):
        for upper_line, lower_line in pairwise(lines):
            bottom = max([char.y + char.bottom for char in upper_line.chars], default=0)
            top = min([char.y + char.top for char in lower_line.chars], default=bottom)
            if bottom <= top:
                continue
            yoffset = bottom - top + margin
            for char in lower_line.chars:
                char.set_pos(char.x, char.y + yoffset)

    def correct_inter_clause(self, lines, margin=0):
        for line in lines:
            for left_clause, right_clause in pairwise(line.clauses):
                left_clause_right = max([char.x + char.right for char in left_clause], default=0)
                right_clause_left = min([char.x + char.left for char in right_clause], default=left_clause_right)
                if left_clause_right <= right_clause_left:
                    continue
                xoffset = left_clause_right - right_clause_left + margin
                for char in right_clause:
                    char.set_pos(char.x + xoffset, char.y)

    def layout(self, right=5, reference_line=20, margin=5):
        if len(self.chars) == 0:
            return Bbox(0, 0, 0, 0)

        cntx = Context(reference_line=reference_line, right=right)

        for char in self.chars:
            self.set_position(cntx, char)

        lines = self.__split()
        self.correct_inter_line(lines, margin=margin)
        self.correct_inter_clause(lines, margin=0)
        self.correct_left_and_top(lines, margin=margin)

        left = math.floor(min([char.x + char.left for char in self.chars])) - margin
        right = math.ceil(max([char.x + char.right for char in self.chars])) + margin
        top = math.floor(min([char.y + char.top for char in self.chars])) - margin
        bottom = math.ceil(max([char.y + char.bottom for char in self.chars])) + margin

        return Bbox(left, right, top, bottom)

    def create_path_elements(self, to_animate=False, speed_mm_per_s=20):
        path_text = ""
        marker_text = ""
        time_s = 0
        for char in self.chars:
            new_elem, time_s = char.create_path_element(time_s=time_s, to_animate=to_animate, speed_mm_per_s=speed_mm_per_s)

            if char.is_marker:
                marker_text += new_elem
            elif char.is_space:
                path_text += marker_text
                marker_text = ""
            else:
                path_text += new_elem
        if marker_text != "":
            path_text += marker_text
        return self.svg_template.format(path_text), time_s

    def select_glyphs(self):
        char_names = [char.name for char in self.chars]
        new_char_names = [char.select_glyph() for char in self.chars]
        count = 0

        while new_char_names != char_names:
            char_names = new_char_names
            new_char_names = [char.select_glyph() for char in self.chars]
            assert count < 10, "Too many iterations in select_glyphs()"
            count += 1

class Character:
    def __init__(self, name, sh):
        self._name = name
        self.prev = None
        self.next = None
        self.sh = sh
        try:
            self.char = sh['character'][name]
        except Exception as e:
            self.char = sh['character']['Null']
            print(e)
        self.glyph = self.char['glyph'][0]
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    @property
    def dx(self):
        return self.glyph['dx']

    @property
    def dy(self):
        return self.glyph['dy']

    @property
    def right(self):
        return self.glyph['right']

    @property
    def left(self):
        return self.glyph['left']

    @property
    def top(self):
        return self.glyph['top']

    @property
    def bottom(self):
        return self.glyph['bottom']

    @property
    def ascent(self):
        return self.glyph['ascent']

    @property
    def exit(self):
        return self.x + self.dx, self.y + self.dy 

    @property
    def name(self):
        return self.glyph.get('name', self._name)

    @property
    def is_marker(self):
        return self.char['mark']

    @property
    def is_space(self):
        return self.char['space']

    @property
    def is_newline(self):
        return self.char['newline']

    @property
    def path(self):
        return self.glyp.paths[0]

    @property
    def paths(self):
        return self.glyph['path']

    @property
    def clip_paths(self):
        return self.glyph.get('clip_path', [])

    @property
    def mask(self):
        return self.glyph.get('mask', [])

    @property
    def lengths(self):
        return [path['length'] for path in self.glyph['path']]

    @property
    def glyphs(self):
        try:
            return self.sh['character'][self._name]['glyph'][1:]
        except KeyError:
            return []

    def select_glyph(self):
        for glyph in self.glyphs:
            if parse_key(glyph['key'], self.sh['groups'], self):
                self.glyph = glyph
                return self.name

    def bak_create_path_element(self, time_s=0, to_animate=False, speed_mm_per_s=20):
        path_elem = ""
        if to_animate:
            if self.clip_paths:
                id_ = random.randint(0, 0x10000)
                path_elem = f'<clipPath id="{id_}"><path d="{"".join([clip_path["d"] for clip_path in self.clip_paths])}"/></clipPath>'
                clip_paths = f"clip-path='url(#{id_})'"
            else:
                clip_paths = f""

            if self.mask:
                id_ = random.randint(0, 0x10000)
                path_elem += f'<mask id="{id_}" maskUnits="userSpaceOnUse">'
                for i, mask in enumerate(self.mask):
                    path_elem += f'<path d="{mask["d"]}" style="stroke: none;" fill="{"white" if i == 0 else "black"}" />'
                path_elem += '</mask>'
                mask = f"mask='url(#{id_})'"
            else:
                mask = ''

            for path, length in zip(self.paths, self.lengths):
                style = self.get_style_to_animate(length)
                animate = self.create_animate_element(time_s, length, speed_mm_per_s)
                path_elem += f'<path d="{path["d"]}" {clip_paths} {mask} {style}>{animate}</path>'
                time_s += length / speed_mm_per_s 
        else:
            path_elem = ""
            if self.clip_paths:
                id_ = random.randint(0, 0x10000)
                path_elem = f'<clipPath id="{id_}"><path d="{"".join([clip_path["d"] for clip_path in self.clip_paths])}" /></clipPath>'
                clip_paths = f"clip-path='url(#{id_})'"
            else:
                clip_paths = ''

            if self.mask:
                id_ = random.randint(0, 0x10000)
                path_elem += f'<mask id="{id_}" maskUnits="userSpaceOnUse">'
                for i, mask in enumerate(self.mask):
                    path_elem += f'<path d="{mask["d"]}" style="stroke: none;" fill="{"white" if i == 0 else "black"}" />'
                path_elem += '</mask>'
                mask = f"mask='url(#{id_})'"
            else:
                mask = ''

            paths = "".join([path['d'] for path in self.paths])
            path_elem += f'<path d="{paths}" {clip_paths} {mask} style="stroke: #000000; stroke-width: 0.425;"/>'

        path_elem = self.wrap_element_in_g_element(path_elem)
        return path_elem, time_s

    def create_clip_path_elements(self):
        if self.clip_paths:
            id_ = random.randint(0, 0x10000)
            elem = f'<clipPath id="{id_}"><path d="{"".join([clip_path["d"] for clip_path in self.clip_paths])}"/></clipPath>'
            attr = f"clip-path='url(#{id_})'"
            return elem, attr
        else:
            return "", ""

    def create_mask_elements(self):
        if self.mask:
            id_ = random.randint(0, 0x10000)
            elem = f'<mask id="{id_}" maskUnits="userSpaceOnUse">'
            for i, mask in enumerate(self.mask):
                elem += f'<path d="{mask["d"]}" style="stroke: none;" fill="{"white" if i == 0 else "black"}" />'
            elem += '</mask>'
            attr = f"mask='url(#{id_})'"
            return elem, attr
        else:
            return "", ""

    def create_path_element(self, time_s=0, to_animate=False, speed_mm_per_s=20):
        path_elem = ""
        
        clip_path_elem, clip_path_attr = self.create_clip_path_elements()
        path_elem += clip_path_elem

        mask_elem, mask_attr = self.create_mask_elements()
        path_elem += mask_elem

        if to_animate:
            for path, length in zip(self.paths, self.lengths):
                style_attr = f'"{self.get_style_to_animate(length)}"'
                animate = self.create_animate_element(time_s, length, speed_mm_per_s)
                path_elem += f'<path d="{path["d"]}" {clip_path_attr} {mask_attr} style={style_attr}>{animate}</path>'
                time_s += length / speed_mm_per_s 
        else:
            paths = "".join([path['d'] for path in self.paths])
            style_attr = f"stroke: #000000; stroke-width: 0.425;"
            path_elem += f'<path d="{paths}" {clip_path_attr} {mask_attr} style="{style_attr}"/>'

        path_elem = self.wrap_element_in_g_element(path_elem)
        return path_elem, time_s

    def get_style_to_animate(self, length):
        #dash = math.ceil(length)
        dash = length
        gap = dash + 1
        offset = dash 
        return f'stroke-dasharray:{dash} {gap}; stroke-dashoffset:{offset};'

    def create_animate_element(self, begin_s, length_mm, speed_mm_per_s=None, duration_s=None):
        return f'<animate attributeName="stroke-dashoffset" values="{length_mm};0" dur="{length_mm/speed_mm_per_s}s" begin="{begin_s}s" fill="freeze"/>'

    def wrap_element_in_g_element(self, elem):
        return  f"<g transform='translate({self.x} {self.y})'>{elem}</g>"
