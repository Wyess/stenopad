#from key_parser import parse as parse_key
from glyph_selector_parser import parse_glyph_selector
import logging
import random

logger = logging.getLogger(__name__)

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
        self.glyph = self.char['default_glyph']
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
        return 'mark' in self.tag

    @property
    def is_space(self):
        return 'space' in self.tag

    @property
    def is_newline(self):
        return 'newline' in self.tag

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
    def tag(self):
        try:
            return self.sh['character'][self.name]['tag']
        except KeyError:
            return {}

    @property
    def glyphs(self):
        try:
            return self.sh['character'][self._name]['glyphs']
        except KeyError:
            print('except KeyError:')
            return []

    def select_glyph(self):
        for glyph in self.glyphs:
            if parse_glyph_selector(glyph['key'], self):
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

    def create_path_element(self, time_s=0, to_animate=False, speed_mm_per_s=20, to_generate_keyframe=False, target_s=0):
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
        elif to_generate_keyframe:
            for path, length in zip(self.paths, self.lengths):
                #style_attr = f'"{self.get_style_to_animate(length)}"'
                duration_s = length / speed_mm_per_s 
                style_attr = f'"{self.get_dashoffset_style(time_s, length, duration_s, target_s)}"'
                
                #animate = self.create_animate_element(time_s, length, speed_mm_per_s)
                path_elem += f'<path d="{path["d"]}" {clip_path_attr} {mask_attr} style={style_attr}></path>'
                time_s += duration_s
        else:
            paths = "".join([path['d'] for path in self.paths])
            style_attr = f"stroke: #000000; stroke-width: 0.425;"
            path_elem += f'<path d="{paths}" {clip_path_attr} {mask_attr} style="{style_attr}"/>'

        path_elem = self.wrap_element_in_g_element(path_elem)
        return path_elem, time_s

    def get_style_to_animate(self, length):
        dash = length
        gap = dash + 0.1
        offset = dash 
        return f'stroke-dasharray:{dash} {gap}; stroke-dashoffset:{offset};'

    def get_dashoffset_style(self, begin_s, length_mm, duration_s, target_s=0):
        dash = length_mm
        gap = dash + 0.25
        if length_mm == 0:
            offset = 0
        else:
            offset = length_mm * max(0, min(1, (begin_s + duration_s - target_s) / duration_s))
        return f'stroke-dasharray:{dash} {gap}; stroke-dashoffset:{offset};'

    def create_animate_element(self, begin_s, length_mm, speed_mm_per_s=None, duration_s=None):
        return f'<animate attributeName="stroke-dashoffset" values="{length_mm};0" dur="{length_mm/speed_mm_per_s}s" begin="{begin_s}s" fill="freeze"/>'

    def wrap_element_in_g_element(self, elem):
        return  f"<g transform='translate({self.x} {self.y})'>{elem}</g>"
